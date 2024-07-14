
# Task 3

- [A) Brain Socket](#a-brain-socket)
- [B) CTF](#b-ctf)
  - [Binary Exploitation](#binary-exploitation)
  - [Forensics](#forensics)
  - [Web (SQL Injection)](#web-sql-injection)
  - [Reverse Engineering](#reverse-engineering)
  - [Cryptography](#cryptography)

# A) Brain Socket 
- Quiz Game is built using `socket` module in `python`
- `threading` is used for accepting multiple connections at the same time.
- Passwords are encrypted using `sha256` algorithm and stored securely in `MySQL` database.
- Server and database are dockerised with `Alpine` as base image and image is uploaded @[DockerHub](https://hub.docker.com/r/revanth7733/brain_socket)
- `mysql-connector-python` module is installed from `.tar.xz` file instead of installing it by `pip` to reduce image size.
- To persist the database, volume named `db` is created and mounted at `/var/lib/mysql`
## Dependencies
- `pyfiglet` and `colorama` are required for `client.py`. Install them by
```sh
pip install pyfiglet colorama
```
## Demo 

https://github.com/user-attachments/assets/7df5730a-e315-4224-a486-fb417531f8fd

# B) CTF

## Binary Exploitation
- This exploitation works by buffer overflow vulnerability of `gets` function.
- Program is compiled with all the protections turned off.

![sec](/samples/buffer_sec.png)

- Program is 64bit executable and symbols are not stripped.

![file](/samples/buffer_file.png)

- Offset of RSP register (Stack Pointer) is found manually in `pwndbg`

![offset](/samples/buffer_offset.png)

- Payload is created using `pwntools` library and flag is fetched.

![result](/samples/buffer_result.png)

## Forensics
- `encoded.txt` file is encoded with `base64` and hidden inside [delta.jpeg](/b/forensics/delta.jpeg) using `steghide`.
- Passphrase is `1234`

## Web (SQL Injection)
> __Environment :__ MySQL 8.2
- SQL Query in application :
```mysql
SELECT name FROM users WHERE uname = '$user' AND pass = '$pass'
```
- This is prone to injection. Application gets `name` from query and displays it on home page after successful login.
- Login for `admin` user can be bypassed by entering `admin' -- ` in the `username` field.
- With access to `information_schema`, list of tables can be obtained by `UNION` based injection.

![tables](/samples/sqli_tables.png)

- By knowing the name and number of columns, table data can be extracted. Number of columns can be calculated by `GROUP BY` method.

![extract](/samples/sqli_extract.png)

- By above methods, flag can be fetched.

![flag](/samples/sqli_flag.png)

- Images of Application : 

![login](/samples/sqli_login.png)

![home](/samples/sqli_home.png)

## Reverse Engineering 
- Program gets input string, calculates the value and prints the flag if value matches to value hardcoded in program.
- Static Analysis using Ghidra (if the source code is not known) :

![ghidra](/samples/reverse_ghidra.png)

- Actual string used to print the flag is `capture the flag`

![org](/samples/reverse_org.png)

- Using `z3-solver`, string is found as `/;0[SS*$#9>{"; 7|n,C|]sa5` which also matches the value.

![z3](/samples/reverse_z3.png)

- By changing the length constraint, different strings which matches the value can be found. Found strings are : 
```
9@dQI**!>?w9l-i'-le`C!&zP
@SjA<*JF:Sjr|ci|vd5
,X%_oBt3yuu"w% 9?t!u"A
39#Vx_TJr1RX|%xt|~&
```

## Cryptography 
- RSA is built using python.
- Message is encrypted with public key and decrypted with private key.
- Message is also signed and signature is verified.

![crypto](/samples/crypto.png)


