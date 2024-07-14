import socket
from sys import argv
from os import system, name
from getpass import getpass
from time import sleep
from hashlib import sha256
from pyfiglet import Figlet
from colorama import Fore, Style

# Heading text
figlet = Figlet(font='slant')
text = figlet.renderText('Brain Socket')
heading = f"{Fore.BLUE}{Style.BRIGHT}{text}"

# Setting background of terminal
if name == 'nt':
    system('color 0F')
else:
    system('setterm --background black')

# Colours
class c:
    RED = Fore.RED + Style.NORMAL
    WHITE = Fore.WHITE  + Style.NORMAL
    CYAN = Fore.CYAN  + Style.NORMAL
    GREEN = Fore.GREEN  + Style.NORMAL
    MAGENTA = Fore.MAGENTA  + Style.NORMAL
    BLUE = Fore.BLUE  + Style.NORMAL
    YELLOW = Fore.YELLOW  + Style.NORMAL
    BLACK = Fore.BLACK + Style.NORMAL

    BRIGHT_RED = Style.BRIGHT + Fore.RED  
    BRIGHT_BLUE = Style.BRIGHT + Fore.BLUE  
    BRIGHT_YELLOW = Style.BRIGHT + Fore.YELLOW  
    BRIGHT_GREEN = Style.BRIGHT + Fore.GREEN  
    BRIGHT_CYAN = Style.BRIGHT + Fore.CYAN   
    BRIGHT_WHITE = Style.BRIGHT + Fore.WHITE   
    BRIGHT_MAGENTA = Style.BRIGHT + Fore.MAGENTA  

# question class
class question:
    def __init__(self,ques):
        self.ques = ques
        self.opt = []
    def option(self,opt):
        self.opt.append(opt)

# class data
class dat:
    def __init__(self,inp,size,type,user):
        self.inp = inp
        self.size = size
        self.type = type
        self.user = user
    def ques(self,ques):
        self.ques = question(ques)

# header
def header():
    if name == 'nt':
        system('cls')
    else:
        system('clear')
    print(f"{heading}")

# index
def index(conn,data):
    print(c.BRIGHT_BLUE,"\n1) Login\n2) Create account")
    match input(f"{c.BRIGHT_WHITE}Option : "):
        case '1':
            header()
            user_login(conn,data)
        case '2':
            header()
            create_user(conn)
        case _:
            header()
            print(f"{c.BRIGHT_YELLOW}Enter valid option")
            index(conn,data)
    
# home 
def home(conn):
    print(f"{c.BRIGHT_BLUE}1) Answer questions\n2) Add question\n3) Leaderboard\n4) Log Out")
    kin = input(f"{c.BRIGHT_WHITE}Option : ")
    match kin :
        case '2':
            add_ques(conn)
        case '1':
            send(conn,"!$nq")
        case '3':
            send(conn,"!$nl")
        case '4':
            send(conn,"!$lo")
        case _:
            header()
            print(f"{c.BRIGHT_YELLOW}Enter valid option")
            home(conn)

# User login
def user_login(conn,data):
    print(f"{c.BRIGHT_GREEN}User Login")
    username = input(f"{c.BRIGHT_CYAN}Username : ")
    password = getpass("Password : ")
    hash = sha256()
    hash.update(password.encode('utf-8'))
    data.user = username
    send(conn, "!$u")
    send(conn, username)
    send(conn, "!$p")
    send(conn, hash.hexdigest())

# Creating new user
def create_user(conn):
    print(f"{c.BRIGHT_GREEN}Add User")
    username = input(f"{c.BRIGHT_CYAN}Username : ")
    password = getpass("New Password : ")
    password2 = getpass("Again : ")
    if password == password2:
        hash = sha256()
        hash.update(password.encode('utf-8'))
        send(conn, "!$au")
        send(conn, username)
        send(conn, "!$ap")
        send(conn, hash.hexdigest())
    else:
        print(f"{c.BRIGHT_RED}Passwords do not match")
        create_user(conn)

# Adding new question
def add_ques(conn):
    header()
    ques = input(f"{c.BRIGHT_CYAN}Question : ")
    send(conn,"!$aq")
    send(conn,ques)
    for i in range(1,5):
        opt = input(f"{c.BRIGHT_WHITE}Option {i} : ")
        send(conn,"!$oi")
        send(conn,opt)
    ans = input(f"{c.GREEN}Ans : ")
    while not ans.isdigit():
        print(f"{c.BRIGHT_YELLOW}Enter option no. for ans")
        ans = input(f"{c.GREEN}Ans : ")
    while int(ans) < 1 or int(ans) > 4:
        print(f"{c.BRIGHT_YELLOW}Enter option no. for ans")
        ans = input(f"{c.GREEN}Ans : ") 
    send(conn,"!$aa")
    send(conn,ans)

# Answering question
def ans_ques(conn,data):
    header()
    ques = data.ques
    print(f"{c.GREEN}Enter n for next, p for previous or h for home")
    print(f"{c.BRIGHT_CYAN}Question : {ques.ques}")
    for i in range(4):
        print(f"{c.BRIGHT_WHITE}{i+1}) {ques.opt[i]}")
    ans_con(conn)

# Answer constraints
def ans_con(conn):
    ans = input("Ans : ")
    match ans:
        case 'h':
            header()
            home(conn)
        case 'p'|'n':
            send(conn,"!$ai")
            send(conn,ans)
        case _:
            if ans.isdigit():
                if int(ans) > 0 and int(ans) < 5:
                    send(conn,"!$ai")
                    send(conn,ans)
                else:
                    print(f"{c.BRIGHT_YELLOW}Enter valid option")
                    ans_con(conn)
            else:
                print(f"{c.BRIGHT_YELLOW}Enter valid option")
                ans_con(conn)
    
# Data sending function
def send(conn,data):
    data = data.encode('utf-8')
    size = str(len(data))
    size += ((4 - len(size)) * ' ')
    conn.send(size.encode('utf-8'))
    conn.send(data)

# Service function
def service(conn, data):
    while True:
        if data.size == 0:
            data.size = int(conn.recv(4).decode('utf-8'))
        else:
            rcv = conn.recv(data.size).decode('utf-8')
            match data.type:
                case 0:
                    match rcv:
                        case "!$ms":
                            data.type = 1
                        case "!$ue":
                            print(f"{c.BRIGHT_RED}User already exists")
                            create_user(conn)
                        case "!$wl":
                            print(f"{c.BRIGHT_RED}Incorrect Username/Password")
                            user_login(conn,data)
                        case "!$tl":
                            header()
                            print(f"{c.BRIGHT_GREEN}Welcome {data.user}")
                            home(conn)
                        case "!$ua":
                            header()
                            print(f"{c.BRIGHT_WHITE}User Added")
                            user_login(conn,data)
                        case "!$qt":
                            header()
                            print(f"{c.BRIGHT_GREEN}Question Added")
                            home(conn)
                        case "!$qi":
                            data.type = 2
                        case "!$qn":
                            send(conn,"!$ds")
                            header()
                            print(f"{c.BRIGHT_YELLOW}No more questions!")
                            home(conn)
                        case "!$ca":
                            header()
                            print(f"{c.BRIGHT_GREEN}Correct answer!{c.BRIGHT_BLUE}\n1) Next Question\n2) Home")
                            match input(f"{c.BRIGHT_WHITE}Option : "):
                                case '1':
                                    header()
                                    send(conn,"!$nq")
                                case '2':
                                    send(conn,"!$ds")
                                    header()
                                    home(conn)
                        case "!$wa":
                            print(f"{c.BRIGHT_RED}Wrong answer! Try again")
                            ans_con(conn)
                        case "!$li":
                            header()
                            print(f"{c.BRIGHT_MAGENTA}Leaderboard")
                            data.type = 3
                        case "!$oi":
                            data.type = 4
                        case "!$lo":
                            data.user = ''
                            header()
                            print(f"{c.BRIGHT_YELLOW}Logged Out")
                            index(conn,data)
                        
                case 1:
                    print(f"{c.BRIGHT_GREEN}{rcv}")
                    data.type = 3
                case 2:
                    data.ques(rcv)
                    data.type = 0
                case 3:
                    if rcv == "!$lc":                            
                        input(f"{c.YELLOW}Press Enter to go Home")
                        header()
                        home(conn)
                        data.type = 0
                    elif rcv == "!$lp":
                        data.inp = '1'
                    elif data.inp == '1':
                        print(f"{c.BRIGHT_RED}{rcv}")
                        data.inp = ''
                    else:
                        print(f"{c.BRIGHT_WHITE}{rcv}")
                case 4:
                    data.ques.option(rcv)
                    if len(data.ques.opt) == 4:
                        ans_ques(conn,data)
                        del data.ques
                    data.type = 0

            data.size = 0

# Server config
if len(argv) == 1:
    host = '127.0.0.1'
    port = 7779
    print(c.BRIGHT_YELLOW,f"Connecting with default server configuration {host}:{port}")
elif len(argv) == 3:
    try:
        socket.inet_aton(argv[1])
        port = int(argv[2])
        if not (0 <= port <= 65535):
            raise ValueError
    except OSError:
        print(f"{c.BRIGHT_YELLOW}Enter a valid IPv4 address.")
        exit(1)
    except ValueError:
        print(f"{c.BRIGHT_YELLOW}Enter a valid port number (0-65535).")
        exit(1)
    host = argv[1]
    port = int(argv[2])
    print(f"{c.BRIGHT_YELLOW}Connecting with custom server configuration {host}:{port}")
else:
    print(f"{c.BRIGHT_GREEN}Usage: python client.py [host] [port]")    
sleep(0.5)

try:
    # Connection Socket 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    data = dat('', 0, 0,'')
    send(sock,"!$cc")
    header()
    index(sock,data)
    service(sock,data)
        
except KeyboardInterrupt:
    print(f"{c.BRIGHT_YELLOW}\nClosing")
    try:
        send(sock,"!$di")
    except (ConnectionRefusedError,BrokenPipeError) as error:
        pass

except (ConnectionRefusedError,BrokenPipeError) as error:
    print(f"{c.BRIGHT_RED}Server Offline")

finally:
    sock.close