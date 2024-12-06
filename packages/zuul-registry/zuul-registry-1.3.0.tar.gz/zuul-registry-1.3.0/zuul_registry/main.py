# Copyright 2019 Red Hat, Inc.
# Copyright 2021, 2024 Acme Gating, LLC
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import base64
import os
import sys
import logging
import cherrypy
import hashlib
import json
import typing
import functools
import yaml

from . import filesystem
from . import storage
from . import swift
from . import s3

import jwt

DRIVERS = {
    'filesystem': filesystem.Driver,
    'swift': swift.Driver,
    's3': s3.Driver,
}


class Authorization(cherrypy.Tool):
    log = logging.getLogger("registry.authz")
    READ = 'read'
    WRITE = 'write'
    AUTH = 'auth'

    def __init__(self, secret, users, public_url):
        self.secret = secret
        self.public_url = public_url
        self.rw = {}
        self.ro = {}
        self.anonymous_read = True

        for user in users:
            if user['access'] == self.WRITE:
                self.rw[user['name']] = user['pass']
            if user['access'] == self.READ:
                self.ro[user['name']] = user['pass']
                self.anonymous_read = False

        if self.anonymous_read:
            self.log.info("Anonymous read access enabled")
        else:
            self.log.info("Anonymous read access disabled")
        cherrypy.Tool.__init__(self, 'before_handler',
                               self.check_auth,
                               priority=1)

    def check(self, store, user, password):
        if user not in store:
            return False
        return store[user] == password

    def unauthorized(self, scope):
        # NOTE(mnaser): This is to workaround the following Docker CLI bug and
        #               should be removed once it is fixed:
        #
        #               https://github.com/docker/cli/issues/3161
        cherrypy.response.headers['Docker-Distribution-Api-Version'] = (
            'registry/2.0'
        )
        cherrypy.response.headers['www-authenticate'] = (
            'Bearer realm="%s/auth/token",scope="%s"' % (
                self.public_url, scope)
        )
        raise cherrypy.HTTPError(401, 'Authentication required')

    def check_auth(self, level=READ):
        auth_header = cherrypy.request.headers.get('authorization')
        if auth_header and 'Bearer' in auth_header:
            token = auth_header.split()[1]
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            if payload.get('level') in [level, self.WRITE]:
                self.log.debug('Auth ok %s', level)
                return
        self.log.debug('Unauthorized %s', level)
        self.unauthorized(level)

    def _get_level(self, scope):
        level = None
        if not isinstance(scope, list):
            scope = scope.split(' ')
        for resource_scope in scope:
            parts = resource_scope.split(':')
            if parts[0] == 'repository' and 'push' in parts[2]:
                level = self.WRITE
            if (parts[0] == 'repository' and 'pull' in parts[2]
                and level is None):
                level = self.READ
        if level is None:
            if self.anonymous_read:
                # No scope was provided, so this is an authentication
                # request; treat it as requesting 'write' access so
                # that we validate the password.
                level = self.WRITE
            else:
                level = self.READ
        return level

    @cherrypy.expose
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    def token(self, **kw):
        # If the scope of the token requested is for pushing an image,
        # that corresponds to 'write' level access, so we verify the
        # password.
        #
        # If the scope of the token is not specified, we treat it as
        # 'write' since it probably means the client is performing
        # login validation.  The _get_level method takes care of that.
        #
        # If the scope requested is for pulling an image, we always
        # grant a read-level token.  This covers the case where no
        # authentication credentials are supplied, and also an
        # interesting edge case: the docker client, when configured
        # with a registry mirror, will, bless it's little heart, send
        # the *docker hub* credentials to that mirror.  In order for
        # us to act as a a stand-in for docker hub, we need to accept
        # those credentials.
        auth_header = cherrypy.request.headers.get('authorization')
        level = self._get_level(kw.get('scope', ''))
        self.log.info('Authenticate level %s', level)
        if level == self.WRITE:
            self._check_creds(auth_header, [self.rw], level)
        elif level == self.READ and not self.anonymous_read:
            self._check_creds(auth_header, [self.rw, self.ro], level)
        # If we permit anonymous read and we're requesting read, no
        # check is performed.
        self.log.debug('Generate %s token', level)
        token = jwt.encode({'level': level}, 'secret', algorithm='HS256')
        return {'token': token,
                'access_token': token}

    def _check_creds(self, auth_header, credstores, level):
        # If the password is okay, fall through; otherwise call
        # unauthorized for the side effect of raising an exception.
        if auth_header and 'Basic' in auth_header:
            cred = auth_header.split()[1]
            cred = base64.decodebytes(cred.encode('utf8')).decode('utf8')
            user, pw = cred.split(':', 1)
            # Return true on the first credstore with the user, false otherwise
            if not next(filter(
                    lambda cs: self.check(cs, user, pw), credstores), False):
                self.unauthorized(level)
        else:
            self.unauthorized(level)


class RegistryAPI:
    """Registry API server.

    Implements the container registry protocol as documented in
    https://docs.docker.com/registry/spec/api/
    """
    log = logging.getLogger("registry.api")
    DEFAULT_NAMESPACE = '_local'
    # A list of content types ordered by preference.  Manifest lists
    # come first so that multi-arch builds are supported.
    CONTENT_TYPES = [
        'application/vnd.docker.distribution.manifest.list.v2+json',
        'application/vnd.oci.image.index.v1+json',
        'application/vnd.docker.distribution.manifest.v2+json',
        'application/vnd.oci.image.manifest.v1+json',
    ]

    def __init__(self, store, namespaced, authz, conf):
        self.storage = store
        self.authz = authz
        self.namespaced = namespaced
        self.conf = conf

    def get_namespace(self, repository):
        if not self.namespaced:
            return (self.DEFAULT_NAMESPACE, repository)
        parts = repository.split('/')
        return (parts[0], '/'.join(parts[1:]))

    def not_found(self):
        raise cherrypy.HTTPError(404)

    @cherrypy.expose
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    def version_check(self):
        self.log.info('Version check')
        return {'version': '1.0'}
        res = cherrypy.response
        res.headers['Distribution-API-Version'] = 'registry/2.0'

    @cherrypy.expose
    # By default CherryPy will try to encode the body/add a charset to
    # headers if the response type is text/*.  However, since it's
    # changing unicode things that may alter the body length, CherryPy
    # deletes the Content-Length so that the framework will
    # automatically re-caclulate it when the response is sent.
    #
    # This poses a problem for blob HEAD requests which return a blank
    # body -- we don't really have a Content-Type for a blank body so
    # it defaults to text/html and goes into the charset detection
    # path where the Content-Length set would get set to zero.
    # Clients handle this in different and confusing ways; doing
    # things sending back invalid manifests several steps later.
    #
    # Disabling the add_charset tool here is important to avoid this
    # behaviour and send a correct Content-Length.
    @cherrypy.config(**{'tools.encode.add_charset': False})
    def head_blob(self, repository, digest):
        namespace, repository = self.get_namespace(repository)
        size = self.storage.blob_size(namespace, digest)
        if size is None:
            self.log.info('Head blob %s %s %s not found',
                          namespace, repository, digest)
            return self.not_found()
        self.log.info('Head blob %s %s %s size %s',
                      namespace, repository, digest, size)
        res = cherrypy.response
        res.headers['Docker-Content-Digest'] = digest
        res.headers['Content-Length'] = str(size)
        return ''

    @cherrypy.expose
    @cherrypy.config(**{'response.stream': True})
    def get_blob(self, repository, digest, ns=None):
        # The ns parameter is supplied by some image clients (like the one
        # found in buildx). We specify it here so that cherrypy doesn't 404
        # when receiving that parameter, but we ignore it otherwise.
        namespace, repository = self.get_namespace(repository)
        self.log.info('Get blob %s %s %s', namespace, repository, digest)
        size, data_iter = self.storage.stream_blob(namespace, digest)
        if data_iter is None:
            return self.not_found()
        res = cherrypy.response
        res.headers['Docker-Content-Digest'] = digest
        res.headers['Content-Type'] = 'application/octet-stream'
        if size is not None:
            res.headers['Content-Length'] = str(size)
        return data_iter

    @cherrypy.expose
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    def get_tags(self, repository):
        namespace, repository = self.get_namespace(repository)
        self.log.info('Get tags %s %s', namespace, repository)
        tags = self.storage.list_tags(namespace, repository)
        return {'name': repository,
                'tags': [t.name for t in tags]}

    @cherrypy.expose
    @cherrypy.config(**{'tools.check_auth.level': Authorization.WRITE})
    def start_upload(self, repository, digest=None):
        orig_repository = repository
        namespace, repository = self.get_namespace(repository)
        method = cherrypy.request.method
        uuid = self.storage.start_upload(namespace)
        self.log.info('[u: %s] Start upload %s %s %s digest %s',
                      uuid, method, namespace, repository, digest)
        res = cherrypy.response
        res.headers['Location'] = '/v2/%s/blobs/uploads/%s' % (
            orig_repository, uuid)
        res.headers['Docker-Upload-UUID'] = uuid
        res.headers['Range'] = '0-0'
        res.headers['Content-Length'] = '0'
        res.status = '202 Accepted'

    @cherrypy.expose
    @cherrypy.config(**{'tools.check_auth.level': Authorization.WRITE})
    def upload_chunk(self, repository, uuid):
        orig_repository = repository
        namespace, repository = self.get_namespace(repository)
        self.log.info('[u: %s] Upload chunk %s %s',
                      uuid, namespace, repository)
        old_length, new_length = self.storage.upload_chunk(
            namespace, uuid, cherrypy.request.body)
        res = cherrypy.response
        res.headers['Location'] = '/v2/%s/blobs/uploads/%s' % (
            orig_repository, uuid)
        res.headers['Docker-Upload-UUID'] = uuid
        res.headers['Content-Length'] = '0'
        # Be careful to not be off-by-one, range starts at 0
        res.headers['Range'] = '0-%s' % (new_length - 1,)
        res.status = '202 Accepted'
        self.log.info(
            '[u: %s] Finish Upload chunk %s %s', uuid, repository, new_length)

    @cherrypy.expose
    @cherrypy.config(**{'tools.check_auth.level': Authorization.WRITE})
    def finish_upload(self, repository, uuid, digest):
        orig_repository = repository
        namespace, repository = self.get_namespace(repository)
        self.log.info('[u: %s] Upload final chunk %s %s digest %s',
                      uuid, namespace, repository, digest)
        old_length, new_length = self.storage.upload_chunk(
            namespace, uuid, cherrypy.request.body)
        self.log.debug('[u: %s] Store upload %s %s',
                       uuid, namespace, repository)
        self.storage.store_upload(namespace, uuid, digest)
        self.log.info('[u: %s] Upload complete %s %s digest %s',
                      uuid, namespace, repository, digest)
        res = cherrypy.response
        res.headers['Location'] = '/v2/%s/blobs/%s' % (orig_repository, digest)
        res.headers['Docker-Content-Digest'] = digest
        res.headers['Content-Range'] = '%s-%s' % (old_length, new_length)
        res.headers['Content-Length'] = '0'
        res.status = '201 Created'

    def _validate_manifest(self, namespace, request):
        body = request.body.read()
        content_type = request.headers.get('Content-Type')

        # Only v2 manifests are validated
        if (content_type !=
            'application/vnd.docker.distribution.manifest.v2+json'):
            return body

        data = json.loads(body)

        # We should not be missing a size in the manifest.  At one
        # point we did accept this but it turned out to be related to
        # zuul-registry returning invalid data in HEAD requests.
        if 'size' not in data['config']:
            msg = ('Manifest missing size attribute, can not create')
            raise cherrypy.HTTPError(400, msg)

        # Validate layer sizes
        for layer in data['layers']:
            digest = layer['digest']
            actual_size = self.storage.blob_size(namespace, digest)
            if 'size' not in layer:
                msg = ('Client push error: layer %s missing size ' % digest)
                raise cherrypy.HTTPError(400, msg)
            size = layer['size']
            if size == actual_size:
                continue
            msg = ("Manifest has invalid size for layer %s "
                   "(size:%d actual:%d)" % (digest, size, actual_size))
            self.log.error(msg)
            # We don't delete layers here as they may be used by
            # different images with valid manifests. Return an error to
            # the client so it can try again.
            raise cherrypy.HTTPError(400, msg)

        return body

    @cherrypy.expose
    @cherrypy.config(**{'tools.check_auth.level': Authorization.WRITE})
    def put_manifest(self, repository, ref):
        namespace, repository = self.get_namespace(repository)
        body = self._validate_manifest(namespace, cherrypy.request)
        hasher = hashlib.sha256()
        hasher.update(body)
        digest = 'sha256:' + hasher.hexdigest()
        self.log.info('Put manifest %s %s %s digest %s',
                      namespace, repository, ref, digest)
        self.storage.put_blob(namespace, digest, body)
        manifest = self.storage.get_manifest(namespace, repository, ref)
        if manifest is None:
            manifest = {}
        else:
            manifest = json.loads(manifest)
        manifest[cherrypy.request.headers['Content-Type']] = digest
        self.storage.put_manifest(
            namespace, repository, ref, json.dumps(manifest).encode('utf8'))
        res = cherrypy.response
        res.headers['Location'] = '/v2/%s/manifests/%s' % (repository, ref)
        res.headers['Docker-Content-Digest'] = digest
        res.status = '201 Created'

    @cherrypy.expose
    # see prior note; this avoids destroying Content-Length on HEAD requests
    @cherrypy.config(**{'tools.encode.add_charset': False})
    def get_manifest(self, repository, ref, ns=None):
        # The ns parameter is supplied by some image clients (like the one
        # found in buildx). We specify it here so that cherrypy doesn't 404
        # when receiving that parameter, but we ignore it otherwise.
        namespace, repository = self.get_namespace(repository)
        method = cherrypy.request.method
        headers = cherrypy.request.headers
        res = cherrypy.response
        self.log.info(
            '%s manifest %s %s %s', method, namespace, repository, ref)
        if ref.startswith('sha256:'):
            manifest = self.storage.get_blob(namespace, ref)
            if manifest is None:
                self.log.error('Manifest %s %s not found', repository, ref)
                return self.not_found()
            res.headers['Content-Type'] = json.loads(manifest)['mediaType']
            res.headers['Docker-Content-Digest'] = ref
            if method == 'HEAD':
                # HEAD requests just return a blank body with the size
                # of the manifest in Content-Length
                size = self.storage.blob_size(namespace, ref)
                res.headers['Content-Length'] = size
                return ''
            return manifest

        # looking up by tag
        manifest = self.storage.get_manifest(namespace, repository, ref)
        if manifest is None:
            manifest = {}
        else:
            manifest = json.loads(manifest)
        accept = [x.strip() for x in headers['Accept'].split(',')]
        # Resort content types by ones that we know about in our
        # preference order, followed by ones we don't know about in
        # the original order.
        content_types = ([h for h in self.CONTENT_TYPES if h in accept] +
                         [h for h in accept if h not in self.CONTENT_TYPES])
        for ct in content_types:
            if ct in manifest:
                self.log.debug('Manifest %s %s digest found %s',
                               repository, ref, manifest[ct])
                data = self.storage.get_blob(namespace, manifest[ct])
                if not data:
                    self.log.error(
                        'Blob %s %s not found', namespace, manifest[ct])
                    return self.not_found()
                res.headers['Content-Type'] = ct
                hasher = hashlib.sha256()
                hasher.update(data)
                self.log.debug('Retrieved sha256 %s', hasher.hexdigest())
                res.headers['Docker-Content-Digest'] = manifest[ct]
                if method == 'HEAD':
                    # See comment above about head response
                    res.headers['Content-Length'] = len(data)
                    return ''
                return data
        self.log.error('Manifest %s %s not found', repository, ref)
        return self.not_found()


class RegistryServer:
    log = logging.getLogger("registry.server")

    def __init__(self, config_path):
        self.log.info("Loading config from %s", config_path)
        self.conf = RegistryServer.load_config(
            config_path, os.environ)['registry']

        # TODO: pyopenssl?
        if 'tls-key' in self.conf:
            cherrypy.server.ssl_module = 'builtin'
            cherrypy.server.ssl_certificate = self.conf['tls-cert']
            cherrypy.server.ssl_private_key = self.conf['tls-key']

        driver = self.conf['storage']['driver']
        backend = DRIVERS[driver](self.conf['storage'])
        self.store = storage.Storage(backend, self.conf['storage'])

        authz = Authorization(self.conf['secret'], self.conf['users'],
                              self.conf['public-url'])

        route_map = cherrypy.dispatch.RoutesDispatcher()
        api = RegistryAPI(self.store,
                          False,
                          authz,
                          self.conf)
        cherrypy.tools.check_auth = authz

        route_map.connect('api', '/v2/',
                          controller=api, action='version_check')
        route_map.connect('api', '/v2/{repository:.*}/blobs/uploads/',
                          controller=api, action='start_upload')
        route_map.connect('api', '/v2/{repository:.*}/blobs/uploads/{uuid}',
                          conditions=dict(method=['PATCH']),
                          controller=api, action='upload_chunk')
        route_map.connect('api', '/v2/{repository:.*}/blobs/uploads/{uuid}',
                          conditions=dict(method=['PUT']),
                          controller=api, action='finish_upload')
        route_map.connect('api', '/v2/{repository:.*}/manifests/{ref}',
                          conditions=dict(method=['PUT']),
                          controller=api, action='put_manifest')
        route_map.connect('api', '/v2/{repository:.*}/manifests/{ref}',
                          conditions=dict(method=['GET', 'HEAD']),
                          controller=api, action='get_manifest')
        route_map.connect('api', '/v2/{repository:.*}/blobs/{digest}',
                          conditions=dict(method=['HEAD']),
                          controller=api, action='head_blob')
        route_map.connect('api', '/v2/{repository:.*}/blobs/{digest}',
                          conditions=dict(method=['GET']),
                          controller=api, action='get_blob')
        route_map.connect('api', '/v2/{repository:.*}/tags/list',
                          conditions=dict(method=['GET']),
                          controller=api, action='get_tags')
        route_map.connect('authz', '/auth/token',
                          controller=authz, action='token')

        conf = {
            '/': {
                'request.dispatch': route_map,
                'tools.check_auth.on': True,
            },
            '/auth': {
                'tools.check_auth.on': False,
            }
        }

        cherrypy.config.update({
            'global': {
                'environment': 'production',
                'server.max_request_body_size': 1e12,
                'server.socket_host': self.conf['address'],
                'server.socket_port': self.conf['port'],
            },
        })

        cherrypy.tree.mount(api, '/', config=conf)

    @staticmethod
    def load_config(path: str, env: typing.Dict[str, str]) -> typing.Any:
        """Replace path content value of the form %(ZUUL_ENV_NAME) with
           environment, then return the yaml load result"""
        with open(path) as f:
            return yaml.safe_load(functools.reduce(
                lambda config, env_item: config.replace(
                    f"%({env_item[0]})", env_item[1]),
                [(k, v) for k, v in env.items() if k.startswith('ZUUL_')],
                f.read()
            ))

    @property
    def port(self):
        return cherrypy.server.bound_addr[1]

    def start(self):
        self.log.info("Registry starting")
        cherrypy.engine.start()

    def stop(self):
        self.log.info("Registry stopping")
        cherrypy.engine.exit()
        # Not strictly necessary, but without this, if the server is
        # started again (e.g., in the unit tests) it will reuse the
        # same host/port settings.
        cherrypy.server.httpserver = None

    def prune(self, dry_run):
        self.store.prune(dry_run)


def main():
    parser = argparse.ArgumentParser(
        description='Zuul registry server')
    parser.add_argument('-c', dest='config',
                        help='Config file path',
                        default='/conf/registry.yaml')
    parser.add_argument('-d', dest='debug',
                        help='Debug log level',
                        action='store_true')
    parser.add_argument('--dry-run', dest='dry_run',
                        help='Do not actually delete anything when pruning',
                        action='store_true')
    parser.add_argument('command',
                        nargs='?',
                        help='Command: serve, prune',
                        default='serve')
    args = parser.parse_args()
    logformat = '%(asctime)s %(levelname)s %(name)s: %(message)s'
    if args.debug or os.environ.get('DEBUG') == '1':
        logging.basicConfig(level=logging.DEBUG, format=logformat)
        logging.getLogger("openstack").setLevel(logging.DEBUG)
        logging.getLogger("urllib3").setLevel(logging.DEBUG)
        logging.getLogger("requests").setLevel(logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO, format=logformat)
        logging.getLogger("openstack").setLevel(logging.INFO)
        logging.getLogger("urllib3").setLevel(logging.ERROR)
        logging.getLogger("requests").setLevel(logging.ERROR)
        cherrypy.log.access_log.propagate = False
    logging.getLogger("keystoneauth").setLevel(logging.ERROR)
    logging.getLogger("stevedore").setLevel(logging.ERROR)

    s = RegistryServer(args.config)
    if args.command == 'serve':
        s.start()
        cherrypy.engine.block()
    elif args.command == 'prune':
        s.prune(args.dry_run)
    else:
        print("Unknown command: %s", args.command)
        sys.exit(1)
