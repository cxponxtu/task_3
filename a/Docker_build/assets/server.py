import socket
import selectors
import mysql.connector
import os
import time
import signal

# Create db if not exists
def db_create():
    crr.execute("CREATE DATABASE IF NOT EXISTS brain_socket")
    crr.execute("USE brain_socket")
    crr.execute("CREATE TABLE IF NOT EXISTS users (id INT(255) NOT NULL AUTO_INCREMENT, PRIMARY KEY(id), uname VARCHAR(255), UNIQUE(uname), pass VARCHAR(255), point INT(255) DEFAULT 0)")
    crr.execute("CREATE TABLE IF NOT EXISTS question (id INT(255) NOT NULL AUTO_INCREMENT, PRIMARY KEY(id), uname VARCHAR(255), ques VARCHAR(255), ans INT(3), op1 VARCHAR(255), op2 VARCHAR(255), op3 VARCHAR(255), op4 VARCHAR(255))")
    db.commit()

# Creating new user
def create_user(conn,username,password):
    crr.execute(f"SELECT uname FROM users WHERE uname = '{username}'")
    db_user = crr.fetchall()
    if db_user:
        print(f"[{username}] User exists")
        send(conn,"!$ue")
    else:
        crr.execute(f"INSERT INTO users (uname, pass) VALUES ('{username}','{password}')")
        print(f"[{username}] User added")
        db.commit()
        crr.execute(f"CREATE TABLE {username} (qid INT(255), PRIMARY KEY (qid))")
        db.commit()
        send(conn,"!$ua")

# Validating user login
def user_login(username,password):
    crr.execute(f"SELECT pass FROM users WHERE uname = '{username}'")
    db_pass = crr.fetchall()
    if db_pass:
        if db_pass[0][0] == password:
            return 1
    else:
        return 0

# Adding new question
def add_ques(conn,data,ans):
    user = data.user
    ques = data.ques.ques
    crr.execute(f"INSERT INTO question (uname, ques, ans, op1, op2, op3, op4) VALUES ('{user}', '{ques}', '{ans}', '{data.ques.opt[0]}', '{data.ques.opt[1]}', '{data.ques.opt[2]}', '{data.ques.opt[3]}')")
    db.commit()
    crr.execute(f"SELECT id FROM question WHERE uname = '{user}' AND ques = '{ques}' AND ans = '{ans}'")
    id = crr.fetchall()
    crr.execute(f"INSERT INTO {user} VALUES ({id[0][0]})")
    db.commit()
    send(conn,"!$qt")

# Sneding question
def send_ques(conn,data):
    sql = ''
    for i in range(len(data.skip)):
        sql += f"AND id <> {data.skip[i]} "
    crr.execute(f"SELECT id,ques,op1,op2,op3,op4 from question WHERE id NOT IN (SELECT qid from {data.user}) {sql}")
    ques = crr.fetchall()
    if ques:
        send(conn,"!$qi")
        send(conn,ques[0][1])
        for i in range(2,6):
            send(conn,"!$oi")
            send(conn,ques[0][i])
        return ques[0][0]
    else:
        send(conn,"!$qn")
        return ''

# Checking ans
def ans_chk(conn,ans,data):
    crr.execute(f"SELECT ans FROM question WHERE id = {int(data.inp)}")
    crt_ans = crr.fetchall()
    match str(ans):
        case 'n':
            data.ski(int(data.inp))
            return 2
        case 'p':
            data.pre()
            return 2
        case _:
            if str(crt_ans[0][0]) == str(ans):
                send(conn,"!$ca")
                crr.execute(f"UPDATE users SET point = point + 5 WHERE uname = '{data.user}'")
                db.commit()
                crr.execute(f"INSERT INTO {data.user} VALUES ({int(data.inp)})")
                db.commit()
                print(f"[{data.user}] Question(id:{data.inp}) answered correct")
                return 1 
            else:
                send(conn,"!$wa")
                print(f"[{data.user}] Question(id:{data.inp}) answered wrong")
                return 0
    
# LeaderBoard
def leadb(conn,data):
    crr.execute("SELECT uname,point FROM users ORDER BY point DESC")
    lb = crr.fetchall()
    send(conn,"!$li")
    for i in range(len(lb)):
        if lb[i][0] == data.user:
            send(conn,"!$lp")
            send(conn,f"{i+1} --- {lb[i][0]} --- {lb[i][1]}")
        else:
            send(conn,f"{i+1} --- {lb[i][0]} --- {lb[i][1]}")
    send(conn,"!$lc")

# question class
class question:
    def __init__(self,ques):
        self.ques = ques
        self.opt = []

    def ans(self,ans):
        self.ans = ans
    def option(self,opt):
        self.opt.append(opt)

# data class
class dat:
    def __init__(self,addrs,inp,size,user,session,type):
        self.addrs = addrs
        self.inp = inp
        self.size = size
        self.user = user
        self.session = session
        self.type = type   
        self.skip = []
    def ques(self,ques):
        self.ques = question(ques)
    def ski(self,skip):
        self.skip.append(skip)
    def pre(self):
        if len(self.skip) > 0:
            self.skip.pop()

# Sending data
def send(conn,data):
    data = data.encode('utf-8')
    size = str(len(data))
    size += ((4 - len(size)) * ' ')
    conn.send(size.encode('utf-8'))
    conn.send(data)

# Adding new connection socket
def add_con(sock):
    conn, addrs = sock.accept()
    print(f"[CONNECTED] {addrs[0]}:{addrs[1]}")
    conn.setblocking(False)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = dat(addrs, "", 0, "", 0, 0)
    sel.register(conn, events, data=data)

# Service function
def service(key, mask):
    conn = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:       
        if data.size == 0:
            rcv = conn.recv(4)
            if rcv:                
                data.size = int(rcv.decode('utf-8'))
            else :
                sel.unregister(conn)
                conn.close()
                print(f"[DISCONNECTED] {data.addrs[0]}:{data.addrs[1]}")
        else:            
            rcv = conn.recv(data.size).decode('utf-8')
            match data.type:
                case 0:
                    match rcv:
                        case "!$u":
                            data.type = 1
                        case "!$p":
                            data.type = 2
                        case "!$au":
                            data.type = 3
                        case "!$ap":
                            data.type = 4
                        case "!$aq":
                            data.type = 5
                        case "!$aa":
                            data.type = 6
                        case "!$nq":
                            data.inp = send_ques(conn,data)
                        case "!$ai":
                            data.type = 7
                        case "!$oi":
                            data.type = 8
                        case "!$nl":
                            leadb(conn,data)
                        case "!$cc":
                            pass
                        case "!$lo":
                            data.session = 0
                            print(f"[{data.user}] Logged out")
                            data.user = ''
                            send(conn,"!$lo")
                        case "!$ds":
                            data.skip.clear()
                        case _:
                            print(rcv)

                case 1:
                    data.user = rcv
                    data.type = 0
                case 2:
                    data.session = user_login(data.user,rcv)
                    if data.session:
                        send(conn,"!$tl")
                        print(f"[{data.user}] Logged in")
                    else:
                        send(conn,"!$wl")
                        print(f"[{data.user}] Inncorrect credentials")
                    data.type = 0
                case 3:
                    data.user = rcv
                    data.type = 0
                case 4:
                    create_user(conn,data.user,rcv)
                    data.type = 0
                case 5:
                    if data.session:
                        data.ques(rcv)
                    data.type = 0
                case 6:
                    if data.session:
                        add_ques(conn,data,rcv)
                        print(f"[{data.user}] Question added")
                        del data.ques
                    data.type = 0
                case 7:                   
                    if data.session:                      
                        match ans_chk(conn,rcv,data):
                            case 1:
                                data.inp = ''
                            case 2:
                                data.inp = send_ques(conn,data)
                    data.type = 0
                case 8:
                    if data.session:
                        data.ques.option(rcv)
                    data.type = 0
                        
            data.size = 0

# Killer function
def killer(signum, frame):
    raise KeyboardInterrupt

# Connecting to db
def db_connect():
    print("\nConnecting to db")
    i = 0
    while i == 0:
        try:
            db = mysql.connector.connect(
                host=os.environ.get('MYSQL_HOST'),
                user=os.environ.get('MYSQL_USER'),
                password=os.environ.get('MYSQL_PASSWORD')
            )
            i = 1
            print("Connected")
            return db
        except (ConnectionRefusedError,mysql.connector.errors.InterfaceError,mysql.connector.errors.DatabaseError) as err:
            pass
        time.sleep(2)

try:
    # Handling Kill signal
    signal.signal(signal.SIGTERM,killer)

    # Getting host and port
    host=os.environ.get('SERVER_HOST')
    port=7779

    # DB connection and dataabse creation
    db = db_connect()
    crr = db.cursor()
    db_create()

    # Create listening socket
    print("Creating listening socket")
    sel = selectors.DefaultSelector()
    lisock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    lisock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lisock.bind((host, port))
    lisock.listen()
    lisock.setblocking(False)
    print(f"Listening on {host}:{port}")
    sel.register(lisock, selectors.EVENT_READ, data=None)

    # Main Selector Loop
    while True:
        operation = sel.select(timeout=None)
        for key, mask in operation :
            if key.data is None : 
                add_con(key.fileobj)
            else : 
                service(key, mask)
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nSIGTERM caught. Shutting down")

finally:
    # Closing listening socket
    if 'lisock' in locals():
        lisock.close()

    # Closing the selector
    if 'sel' in locals():
        to_close = [key.fileobj for key in sel.get_map().values() if key.fileobj is not lisock]
        # Close all connections
        for fileobj in to_close:
            print("Closing connection")
            sel.unregister(fileobj)
            fileobj.close()   
        sel.close()
    
    # Closing db connection
    if 'db' in locals():
        db.close()
    
