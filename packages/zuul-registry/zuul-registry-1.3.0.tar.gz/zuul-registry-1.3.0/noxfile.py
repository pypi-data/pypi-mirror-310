# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import nox


nox.options.error_on_external_run = True
nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = ["tests-3", "linters"]


@nox.session(python='3')
def tests(session):
    session.install('-r', 'requirements.txt',
                    '-r', 'test-requirements.txt')
    session.install('-e', '.')
    session.run('stestr', 'run', '--slowest', *session.posargs)


@nox.session(python='3')
def linters(session):
    session.install('flake8')
    session.run('flake8', *session.posargs)


@nox.session(python='3')
def venv(session):
    session.install('-r', 'requirements.txt',
                    '-r', 'test-requirements.txt')
    session.install('-e', '.')
    session.run(*session.posargs)
