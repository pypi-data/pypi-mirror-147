"""This module implements (or calls) qzone password encrypt algorithm."""

import base64
import binascii
import hashlib
import re
import struct
from abc import ABC, abstractmethod
from random import randint
from typing import Awaitable, Union

import rsa
from aiohttp import ClientSession

from ..type import CheckResult

LOGIN_JS = "https://qq-web.cdn-go.cn/any.ptlogin2.qq.com/v1.3.0/ptlogin/js/c_login_2.js"


class PasswdEncoder(ABC):
    def __init__(self, sess: ClientSession, passwd: str) -> None:
        self.sess = sess
        self._passwd = passwd

    def encode(self, r: CheckResult) -> Awaitable[str]:
        assert self._passwd, "password should not be empty"
        return self.getEncryption(r.salt, r.verifycode)

    async def login_js(self):
        async with self.sess.get(LOGIN_JS) as response:
            response.raise_for_status()
            return await response.text()

    @abstractmethod
    async def getEncryption(self, salt: str, verifycode: str) -> str:
        pass


class NodeEncoder(PasswdEncoder):
    """Encoder using original js code by communicating with local :program:`Node.js <node>` progress.
    Make sure this always work.
    """

    __env = None

    async def getEncryption(self, salt: str, verifycode: str) -> str:
        from jssupport.execjs import ExecJS, Partial

        if self.__env is None:
            js = await self.login_js()
            m = re.search(r"function\(module,exports,__webpack_require__\).*\}", js)
            assert m
            funcs = m.group(0)
            env = ExecJS()
            env.setup.append("var navigator = new Object; navigator.appName = 'Netscape'")
            env.setup.append(f"var a=[{funcs}]")
            env.setup.append("function n(k) {var t,e=new Object;return a[k](t,e,n),e}")
            env.setup.append(
                "function getEncryption(p,s,v){var t,e=new Object;return a[9](t,e,n),e['default'].getEncryption(p,s,v,undefined)}"
            )
            self.__env = env

        return (await self.__env(Partial("getEncryption", self._passwd, salt, verifycode))).strip()


class TeaEncoder(PasswdEncoder):
    """Pure python password encoder implementation using tea and rsa. (beta)

    .. code-block::txt
        :caption: LICENSE

        The MIT License

        Copyright (c) 2005 hoxide

        Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
        The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        QQ Crypt module.

    .. seealso:: https://github.com/LeoHuang2015/qqloginjs/blob/7d82f2f7d7363547763c40ce5d258d18989b9732/tea.py"""

    op = 0xFFFFFFFF
    delta = 0x9E3779B9
    rsaE = "e9a815ab9d6e86abbf33a4ac64e9196d5be44a09bd0ed6ae052914e1a865ac8331fed863de8ea697e9a7f63329e5e23cda09c72570f46775b7e39ea9670086f847d3c9c51963b131409b1e04265d9747419c635404ca651bbcbc87f99b8008f7f5824653e3658be4ba73e4480156b390bb73bc1f8b33578e7a4e12440e9396f2552c1aff1c92e797ebacdc37c109ab7bce2367a19c56a033ee04534723cc2558cb27368f5b9d32c04d12dbd86bbd68b1d99b7c349a8453ea75d1b2e94491ab30acf6c46a36a75b721b312bedf4e7aad21e54e9bcbcf8144c79b6e3c05eb4a1547750d224c0085d80e6da3907c3d945051c13c7c1dcefd6520ee8379c4f5231ed"
    rsaPublickey = int(rsaE, 16)
    rsaKey = rsa.PublicKey(rsaPublickey, int("10001", 16))

    def _xor(self, a, b):
        a1, a2 = struct.unpack(">LL", a[0:8])
        b1, b2 = struct.unpack(">LL", b[0:8])
        r = struct.pack(">LL", (a1 ^ b1) & self.op, (a2 ^ b2) & self.op)
        return r

    def _tea(self, v: bytes, t: bytes):
        o, r, a, l = struct.unpack(">LLLL", t[0:16])
        y, z = struct.unpack(">LL", v[0:8])
        s = 0
        for i in range(16):
            s += self.delta
            s &= self.op
            y += (z << 4) + o ^ z + s ^ (z >> 5) + r
            y &= self.op
            z += (y << 4) + a ^ y + s ^ (y >> 5) + l
            z &= self.op
        r = struct.pack(">LL", y, z)
        return r

    def encrypt(self, v: bytes, k: bytes) -> bytes:
        END_CHAR = b"\0"
        FILL_N_OR = 0xF8

        vl = len(v)
        filln = (8 - (vl + 2)) % 8 + 2
        fills = bytes(randint(0, 0xFF) for _ in range(filln))
        v = bytes([randint(0, FILL_N_OR) | (filln - 2)]) + fills + v + END_CHAR * 7
        assert len(v) % 8 == 0

        tr = to = o = b"\0" * 8
        r = b""
        for i in range(0, len(v), 8):
            o = self._xor(v[i : i + 8], tr)
            tr = self._xor(self._tea(o, k), to)
            to = o
            r += tr
        return r

    def _tx_md5(self, raw_str: Union[bytes, str]):
        if isinstance(raw_str, str):
            raw_str = raw_str.encode()
        return hashlib.md5(raw_str).hexdigest().upper()

    def _int2hex(self, ct: int):
        return hex(ct)[2:]

    def _fromhex(self, s: str):
        return bytes(bytearray.fromhex(s))

    def _hex2bytes(self, s: bytes):
        e = []
        for i in range(0, len(s), 2):
            try:
                e.append(int(s[i : i + 2]))
                continue
            except ValueError:
                pass
            try:
                e.append(int(s[i]))
            except ValueError:
                e.append(0)
        return bytes(e)

    async def getEncryption(self, salt: str, verifycode: str, md5_pwd: bool = False):
        # verifycode先转换为大写，然后转换为bytes
        l = binascii.b2a_hex(verifycode.upper().encode())

        # verifycode length
        c = self._int2hex(int(len(l) / 2)).encode()
        c = c.zfill(4)

        r = self._passwd
        if md5_pwd:
            r = self._tx_md5(self._passwd)
        r = r.encode()

        p = self._tx_md5(self._hex2bytes(r) + salt.encode())
        n = self.encrypt(r + binascii.b2a_hex(salt.encode()) + c + l, p.encode())

        r = self._int2hex(int(len(n) / 2)).encode()
        n = rsa.encrypt(self._hex2bytes(r.zfill(4) + n), self.rsaKey)

        return base64.b64encode(self._hex2bytes(n), b"*-").decode().replace("=", "_")
