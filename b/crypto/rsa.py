from hashlib import md5

p1 = 731397106325201488238427297281
p2 = 454438332450032843959787052451

# Finding gcd of two numbers
def gcd(a,b):
    while b != 0:
        a, b = b, a % b
    return a

# Finding e such that 1 < e < pi_n and gcd(e,pi_n) = 1
def e_find(pi_n):
    e = 3
    try:
        while e < pi_n:
            if gcd(e,pi_n) == 1:
                print (e)
            e += 2
    except KeyboardInterrupt:
        pass
    finally:
        return e

# Generating public key
def public_key(p1,p2):
    n = p1 * p2

    ### e can be found by following function but it takes some time
    ### Greater e can be used to increase security but slower encryption and decryption
    ### e = 169813117 .This is value generated by running the function for two minutes
    # pi_n = (p1-1)*(p2-1)
    # e = e_find(pi_n)

    e = 65537 # Most common value for e
    return (e,n)

# Generating private key
def private_key(e,p1,p2):
    pi_n = (p1-1)*(p2-1)
    d = pow(e,-1,pi_n)
    return (d,p1*p2)

# Encrypting the message using public key by coneverting it to bytes from string and then to integer
def encrypt(message,pub_key):
    message = int.from_bytes(message.encode(),'big')
    return pow(message,pub_key[0],pub_key[1])

# Decrypting the message using private key by converting it to bytes from integer and then to string
def decrypt(e_message,pri_key):
    message = pow(e_message,pri_key[0],pri_key[1])
    return message.to_bytes((message.bit_length() + 7) // 8, 'big').decode()

# Generating signature using private key
def sig_gen(message,pri_key):
    hash = md5()
    hash.update(message.encode())
    hash = int.from_bytes(hash.digest(),'big')
    return pow(hash,pri_key[0],pri_key[1])

# Verifying signature using public key
def sig_ver(message,sig,pub_key):
    hash = md5()
    hash.update(message.encode())
    hash = int.from_bytes(hash.digest(),'big')
    hash2 = pow(sig,pub_key[0],pub_key[1])
    print (f"Hash from signature: {hash}")
    print (f"Hash from received message: {hash2}")
    if hash == hash2:
        return True
    else:
        return False
    
# Finding the maximum size of the message that can be encrypted
def max_size(pub_key):
    n = pub_key[1]
    sbits = n.bit_length()
    sbytes = (sbits) // 8
    return (sbits,sbytes)
    
# Main
pub_key = public_key(p1,p2)
pri_key = private_key(pub_key[0],p1,p2)
print (f"Public key: {pub_key}")
print (f"Private key: {pri_key}")
size = max_size(pub_key)
print (f"Maximum size of message that can be encrypted: {size[1]} bytes or {size[0]} bits\n")

str1 = input("Enter the message to be encrypted : ")
e_message = encrypt(str1,pub_key)
print (f"Encrypted message: {e_message}")
print (f"Decrypted message: {decrypt(e_message,pri_key)}\n")

str2 = input("Enter the message to be signed : ")
sign = sig_gen(str2,pri_key)
print (f"Signature: {sign}")
str3 = input("Enter the message to be verified : ")
if sig_ver(str3,sign,pub_key):
    print ("Signature verified")
else:
    print ("Signature not verified")

