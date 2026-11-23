# Lua 5.2 bytecode disassembler (the game's compiled scripts), luac -l style with constants and upvalue names inline.
# usage: python tools/lua/luadis.py <file.lua> [function filter substring]
import struct, sys

OPS = ("MOVE LOADK LOADKX LOADBOOL LOADNIL GETUPVAL GETTABUP GETTABLE SETTABUP SETUPVAL SETTABLE NEWTABLE SELF ADD SUB "
       "MUL DIV MOD POW UNM NOT LEN CONCAT JMP EQ LT LE TEST TESTSET CALL TAILCALL RETURN FORLOOP FORPREP TFORCALL "
       "TFORLOOP SETLIST CLOSURE VARARG EXTRAARG").split()


class Reader:
    def __init__(self, d):
        self.d, self.p = d, 0

    def take(self, n):
        b = self.d[self.p:self.p + n]
        self.p += n
        return b

    def u8(self): return self.take(1)[0]
    def int(self): return struct.unpack(E + 'i', self.take(4))[0]
    def size(self): return struct.unpack(E + 'I', self.take(4))[0]  # size_t is 4 bytes on the 32-bit target (checked in header)

    def str(self):
        n = self.size()
        return self.take(n)[:-1].decode('utf-8', 'replace') if n else None


def function(r):
    f = {'line': r.int(), 'last': r.int(), 'params': r.u8(), 'vararg': r.u8(), 'stack': r.u8()}
    f['code'] = [struct.unpack(E + 'I', r.take(4))[0] for _ in range(r.int())]
    k = []
    for _ in range(r.int()):
        t = r.u8()
        k.append(None if t == 0 else bool(r.u8()) if t == 1 else struct.unpack(E + 'd', r.take(8))[0] if t == 3 else r.str())
    f['k'] = k
    f['protos'] = [function(r) for _ in range(r.int())]
    f['upvals'] = [(r.u8(), r.u8()) for _ in range(r.int())]
    f['source'] = r.str()
    f['lines'] = [r.int() for _ in range(r.int())]
    f['locals'] = [(r.str(), r.int(), r.int()) for _ in range(r.int())]
    f['upnames'] = [r.str() for _ in range(r.int())]
    return f


def kstr(v): return repr(v) if isinstance(v, str) else ('%g' % v if isinstance(v, float) else str(v))


def dump(f, path, flt):
    name = path
    if flt is None or flt in name or any(isinstance(v, str) and flt in v for v in f['k']):
        print('function %s (line %d-%d, %d params, %d stack)' % (name, f['line'], f['last'], f['params'], f['stack']))
        rk = lambda x: 'K' + kstr(f['k'][x - 256]) if x >= 256 else 'r%d' % x
        up = lambda i: f['upnames'][i] if i < len(f['upnames']) else 'U%d' % i
        for pc, ins in enumerate(f['code']):
            op, a, c, b, bx = ins & 63, (ins >> 6) & 255, (ins >> 14) & 511, ins >> 23, ins >> 14
            sbx = bx - 131071
            o = OPS[op] if op < len(OPS) else '?%d' % op
            if o in ('LOADK',): s = 'r%d = %s' % (a, kstr(f['k'][bx]))
            elif o == 'GETTABUP': s = 'r%d = %s[%s]' % (a, up(b), rk(c))
            elif o == 'SETTABUP': s = '%s[%s] = %s' % (up(a), rk(b), rk(c))
            elif o == 'GETTABLE': s = 'r%d = r%d[%s]' % (a, b, rk(c))
            elif o == 'SETTABLE': s = 'r%d[%s] = %s' % (a, rk(b), rk(c))
            elif o == 'SELF': s = 'r%d = r%d; r%d = r%d[%s]' % (a + 1, b, a, b, rk(c))
            elif o in ('ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'POW'): s = 'r%d = %s %s %s' % (a, rk(b), '+-*/%^'['ADD SUB MUL DIV MOD POW'.split().index(o)], rk(c))
            elif o in ('EQ', 'LT', 'LE'): s = 'if (%s %s %s) ~= %d then skip' % (rk(b), {'EQ': '==', 'LT': '<', 'LE': '<='}[o], rk(c), a)
            elif o in ('JMP', 'FORLOOP', 'FORPREP', 'TFORLOOP'): s = 'r%d -> %d' % (a, pc + 1 + sbx)
            elif o == 'GETUPVAL': s = 'r%d = %s' % (a, up(b))
            elif o == 'SETUPVAL': s = '%s = r%d' % (up(b), a)
            elif o == 'CLOSURE': s = 'r%d = closure #%d' % (a, bx)
            elif o == 'CALL': s = 'r%d(%s) -> %s' % (a, '...' if b == 0 else b - 1, 'multi' if c == 0 else c - 1)
            else: s = 'A%d B%d C%d' % (a, b, c)
            line = f['lines'][pc] if pc < len(f['lines']) else 0
            print('  %4d [%4d] %-9s %s' % (pc, line, o, s))
    for i, p in enumerate(f['protos']):
        dump(p, '%s/%d' % (path, i), flt)


d = open(sys.argv[1], 'rb').read()
assert d[:5] == b'\x1bLuaR', 'not Lua 5.2 bytecode'
E = '<'  # little-endian data, although the header's endianness byte says 0
assert d[7] == 4 and d[8] == 4 and d[9] == 4 and d[10] == 8, 'unexpected int/size_t/instruction/number sizes'
r = Reader(d)
r.p = 18
dump(function(r), 'main', sys.argv[2] if len(sys.argv) > 2 else None)
