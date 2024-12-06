# encoding: utf-8
"""SHA1PRNG在Python中的实现，与JAVA SecureRandom的生成结果保持一致。

// -----------------------------------------------
// 以下是使用JAVA SecureRandom生成伪随机序列的测试代码
// 注意：在随机种相同时，才会生成相同的随机序列
// -----------------------------------------------
import java.security.*; 
import java.util.*; 

class Main {
    public static void main(String[] args) {
        try {
            byte[] output = new byte[10];
            byte[] pwd = new byte[] { (byte)0x70, (byte)0x77, (byte)0x64 };
            SecureRandom random = SecureRandom.getInstance("SHA1PRNG");
            random.setSeed(pwd);
            for(int i=0; i<50; i++){
                random.nextBytes(output);
                System.out.println(HexFormat.of().formatHex(output));
            }
        } catch (NoSuchAlgorithmException e){
        }
    }
}
// -----------------------------------------------
// 以下是在种了为pwd时的前50组输出
// -----------------------------------------------
975b2cd4ff9ae554fe8a
d33168fbfc326d2021dd
25ad76226e84fecd44ec
8410ccdf0fc320aebe0a
9bdb251d6a1eaf62cba0
7bd707b603c87ed78d4b
7b41230345bea763d765
6eb65c474080455599a6
c6a0429b6ed9b927b50f
c39d476505ebe8e7ce16
fbe50b6a550322e4bca1
4dcb5109c0de5ca9e704
cbe78b1046c7352b169e
0185612ee00213a5333f
2b2ee782aa509f79fe9b
3f92911bdcf250d0129d
3960fbfc52281f5af14b
2b0b1c824db557898125
80c5e8d9a380a7369dd0
a85227a13e5aa84afb0c
ac0ea6a2aa933770b673
51d3f6bb454ef7806f46
60f98768834d1205696e
75f491485a56913bf415
20540ae17f66468d9f2e
38566dfc7e00e5a0be8d
51842708ba24c2092d66
4e8d71a7fa9ab473a854
88baf9a1b71f4726c7e2
e9082e6b5930d35744fb
0bba14eafa4aa2589a07
f2909e7b76d528409032
c6d6c4aa0d5e30ac0d33
d8950862edfa5b3347f7
79529e2098be91e7b9b2
04b0bbbfc7b092639144
d678d6af3188aecef436
654f9b2c1ab9896c340d
cc19e1564a68e484c2f5
34af1ed78b1c14010826
a174149923dfdfde8022
383d6dfd8ae931debc53
7883c16442772744885a
1252262cd4a61f87eb3d
c627078df3e7def3d809
24e1688e47e50c7a687d
c1af8efcaf3b6bfeb953
14d1bfadafd92786922b
582d90f5703f73cfabc3
d952c02e90c0729ae495
"""
import hashlib
from random import Random
from random import RECIP_BPF
from io import BytesIO
import binascii


class RandomBytesBasedPRNG(Random):
    """基于随机字节流的伪随机数生成器。

    参考了random.SystemRandom的实现。
    """

    VERSION = 1

    def randbytes(self, n):
        """Generate n random bytes."""
        raise NotImplementedError()

    def getstate(self):
        """Return internal state; can be passed to setstate() later."""
        raise NotImplementedError()

    def setstate(self, state):
        """Restore internal state from object returned by getstate()."""
        raise NotImplementedError()

    def random(self):
        """Get the next random number in the range 0.0 <= X < 1.0."""
        return (int.from_bytes(self.randbytes(7)) >> 3) * RECIP_BPF

    def getrandbits(self, k):
        """getrandbits(k) -> x.  Generates an int with k random bits."""
        if k < 0:
            raise ValueError("number of bits must be non-negative")
        numbytes = (k + 7) // 8  # bits / 8 and rounded up
        x = int.from_bytes(self.randbytes(numbytes))
        return x >> (numbytes * 8 - k)  # trim excess bits


class HASHPRNG(RandomBytesBasedPRNG):
    HASH = hashlib.sha1
    BLOCK_SIZE = 20

    def __init__(self, initiation: bytes):
        self.seed(initiation)

    def seed(self, x, **kwargs):
        self.state = self.HASH(x).digest()
        self.pos = self.BLOCK_SIZE

    def update_state(self):
        self.state = self.HASH(self.state).digest()
        self.pos = 0

    def randbytes(self, n):
        if n < 0:
            raise ValueError("negative argument not allowed")
        buffer = BytesIO()
        while n:
            if self.pos + n < self.BLOCK_SIZE:
                buffer.write(self.state[self.pos : self.pos + n])
                self.pos += n
                break
            else:
                buffer.write(self.state[self.pos :])
                n -= self.BLOCK_SIZE - self.pos
                self.update_state()
        return buffer.getvalue()

    def getstate(self):
        return (
            self.VERSION,
            (self.state, self.pos),
            None,
        )

    def setstate(self, state):
        self.state = state[1][0]
        self.pos = state[1][1]


class SHA1PRNG(HASHPRNG):
    HASH = hashlib.sha1
    BLOCK_SIZE = 20
