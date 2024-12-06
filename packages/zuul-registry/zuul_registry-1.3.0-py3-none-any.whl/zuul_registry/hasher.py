# Copyright 2024 Acme Gating, LLC
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

import base64

import sha256


class ResumableSha256:
    def __init__(self):
        self.hasher = sha256.sha256()
        self.buffer = b''

    def update(self, data):
        if self.buffer is None:
            raise Exception("Unable to update: hash is complete")
        if self.buffer:
            data = self.buffer + data
            self.buffer = b''
        extra_len = len(data) % 64
        if extra_len:
            self.buffer = data[-extra_len:]
            data = data[:-extra_len]
        self.hasher.update(data)

    def get_state(self):
        hstate = self.hasher.state
        return {
            'hash': base64.encodebytes(hstate[0]).decode('ascii'),
            'counter': hstate[1],
            'buffer': base64.encodebytes(self.buffer).decode('ascii'),
        }

    def set_state(self, state):
        hstate = (
            base64.decodebytes(state['hash'].encode('ascii')),
            state['counter'],
        )
        self.hasher.state = hstate
        self.buffer = base64.decodebytes(state['buffer'].encode('ascii'))

    def finish(self):
        if self.buffer:
            self.hasher.update(self.buffer)
        self.buffer = None

    def digest(self):
        self.finish()
        return self.hasher.digest()

    def hexdigest(self):
        self.finish()
        return self.hasher.hexdigest()
