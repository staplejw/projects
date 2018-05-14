import socket, sys, threading, json, time, optparse, os

def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True

def validate_port(x):
    if not x.isdigit():
        return False
    i = int(x)
    if i < 0 or i > 65535:
            return False
    return True

class Tracker(threading.Thread):
    def __init__(self, port, host='0.0.0.0'):
        threading.Thread.__init__(self)
        self.port = port
        self.host = host
        self.BUFFER_SIZE = 8192
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.users = {} # current connections  self.users[(ip,port)] = {'exptime': ----}
        self.files = {} # {'ip': ----,'port': ----,'mtime': ----}
        self.lock = threading.Lock()
        try:
            # YOUR CODE
            # Bind to address and port
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, self.BUFFER_SIZE)
            self.server.bind((self.host, self.port))

            
        except socket.error:
            print('Bind failed %s' % (socket.error))
            sys.exit()
        # YOUR CODE
        # listen for connections
        self.server.listen(1)

    def check_user(self):
        # - every second, iterate through the users and check to see if they are expired.
        # - if a user is expired, add them to the list of old users and add their files
        # to the list of old files. 
        # - then, use these lists to update the dictionaries (delete elements).
        while True:
            old_users = []
            old_files = []

            # acquire the lock before reading or writing self.users/self.files
            self.lock.acquire()
            for user, exp in self.users.iteritems():
                if exp['exptime'] < time.time():
                    old_users.append(user)
                    for filename, info in self.files.iteritems():
                        if (user[0] == info['ip']) and (user[1] == info['port']):
                            old_files.append(filename)

            
            for user in old_users:
                del self.users[user]

            for filename in old_files:
                del self.files[filename]
            # release the lock when done writing
            self.lock.release()

            # 
            time.sleep(1)
        
    # Ensure sockets are closed on disconnect
    def exit(self):
        self.server.close()

    def run(self):
        print('Waiting for connections on port %s' % (self.port))
        while True:
            # YOUR CODE
            # accept incoming connection and create a thread for receiving messages from FileSynchronizer
            conn, addr = self.server.accept()
            threading.Thread(target=self.proces_messages, args=(conn, addr)).start()

    def proces_messages(self, conn, addr):
        conn.settimeout(180.0)
        print 'Client connected with ' + addr[0] + ':' + str(addr[1])
        while True:
            # recive data
            data = ''
            while True:
                part = conn.recv(self.BUFFER_SIZE)
                data = data + part
                if len(part) < self.BUFFER_SIZE:
                    break
            # YOUR CODE
            # check if the received data is a json string and load the json string
            try:
                data_dic = json.loads(data)
            except ValueError as e:
                print(e)
            
            # sync and send files json data

            # acquire the lock before reading or writing to self.users/self.files
            self.lock.acquire()
            # if 'init' message
            if (len(data_dic) == 2):
                self.users[(addr[0], data_dic[u'port'])] = {'exptime' : time.time() + 180}
                for f in data_dic[u'files']:
                    self.files[f[u'name']] = {'ip' : addr[0], 'port' : data_dic[u'port'], 'mtime' : f[u'mtime']}
            # if 'keepalive' message
            elif (len(data_dic) == 1):
                self.users[(addr[0], data_dic[u'port'])] = {'exptime' : time.time() + 180}
            # release the lock when done writing
            self.lock.release()

            message = json.dumps(self.files)
            conn.send(message)
                      
        conn.close() # Close
        
if __name__ == '__main__':
    parser = optparse.OptionParser(usage="%prog ServerIP ServerPort")
    options, args = parser.parse_args()
    if len(args) < 1:
        parser.error("No ServerIP and ServerPort")
    elif len(args) < 2:
        parser.error("No  ServerIP or ServerPort")
    else:
        if validate_ip(args[0]) and validate_port(args[1]):
            server_ip = args[0]
            server_port = int(args[1])
        else:
            parser.error("Invalid ServerIP or ServerPort")
    tracker = Tracker(server_port,server_ip)
    tracker.start()
    # spawn a thread that is responsible for checking that users are alive
    threading.Thread(target=tracker.check_user).start()
