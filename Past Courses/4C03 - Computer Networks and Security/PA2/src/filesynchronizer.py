#!/usr/bin/python
#==============================================================================
#description     :This is the file synchronizer code
#usage           :python skeleton.py trackerIP trackerPort
#python_version  :2.7
#Authors         :Chenhe Li, Yongyong Wei, Rong Zheng, Justin Staples
#==============================================================================

from socket import *
from sys import *
from threading import *
from json import *
from time import *
from ssl import *
import subprocess
import os.path
import glob
import json
import optparse
import calendar

#Validate the IP address of the correct format
def validate_ip(s):
    """
    Arguments:
    s -- dot decimal IP address in string

    Returns:
    True if valid; False otherwise
    """

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

#Validate the port number is in range [0, 2^16-1]
def validate_port(x):
    """
    Arguments:
    x -- port number

    Returns:
    True if valid; False, otherwise
    """

    if not x.isdigit():
        return False
    i = int(x)
    if i < 0 or i > 65535:
            return False
    return True


#Get file info in the local directory (subdirectories are ignored)
#NOTE: Exclude files with .so, .py, .dll suffixes
def get_file_info():
    """
    Return: a JSON array of {"name":file,"mtime":mtime}

    """
    # YOUR CODE
    files = []
    # use bash commands to get the names of the local files and 
    # their modified times. feed this to output files. 
    command_1 = "ls -p | grep -v / > names.txt"
    command_2 = "ls -l -p | grep -v / > mtimes.txt"
    os.system(command_1)
    os.system(command_2)
    f = open("names.txt", "r")
    g = open("mtimes.txt", "r")
    names = f.readlines()
    mtimes = g.readlines()
    f.close()
    # open the new files and read the content, while updating the list
    # of dictionaries
    for i in range(len(names)):
        n = names[i].strip()
        if (not(n.endswith('.so')) and not(n.endswith('.py')) and not(n.endswith('.dll')) and n !='names.txt' and n != 'mtimes.txt'):
            files.append({})
            files[-1]["name"] = n
            temp = mtimes[i + 1].replace(names[i], '')
            temp = temp.strip()
            parts = temp.split(' ')
            l = len(parts)
            t = strptime("18 " + parts[l - 2] + " " + parts[l - 3] + " " + parts[l - 1].split(':')[0] + " " + parts[l - 1].split(':')[1], "%y %b %d %H %M")
            files[-1]["mtime"] = calendar.timegm(t)

    return files

#Check if a port is available
def check_port_avaliable(check_port):
    """
    Arguments:
    check_port -- port number

    Returns:
    True if valid; False otherwise
    """
    if str(check_port) in os.popen("netstat -na").read():
        return False
    return True

#Get the next available port by searching from initial_port to 2^16 - 1
#Hint: use check_port_avaliable() function
def get_next_avaliable_port(initial_port):
    """
    Arguments:
    initial_port -- the first port to check

    Return:
    port found to be available; False if no port is available.
    """
    # YOUR CODE
    # from the starting port to the max port, check each ones availability
    for i in range(initial_port, 65536):
        if (check_port_avaliable(i)):
            return i
    return False


class FileSynchronizer(Thread):
    def __init__(self, trackerhost,trackerport,port, host='0.0.0.0'):

        Thread.__init__(self)
        #Port for serving file requests
        self.port = port #YOUR CODE
        self.host = trackerhost #YOUR CODE

        #Tracker IP/hostname and port
        self.trackerhost = trackerhost #YOUR CODE
        self.trackerport = trackerport #YOUR CODE

        self.BUFFER_SIZE = 8192

        #Create a TCP socket to communicate with tracker
        self.client = socket(AF_INET, SOCK_STREAM)  #YOUR CODE
        self.client.settimeout(180)

        #Store the message to be sent to tracker. Initialize to Init message
        #that contains port number and local file info.
        self.msg = {"port" : self.port, "files" : get_file_info()} #YOUR CODE

        #Create a TCP socket to serve file requests
        self.server = socket(AF_INET, SOCK_STREAM) #YOUR CODE

        try:
            self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, self.BUFFER_SIZE)
            self.server.bind((self.host, self.port))
        except error:
            print('Bind failed %s' % (error))
            sys.exit()
        self.server.listen(10)

    # Not currently used. Ensure sockets are closed on disconnect
    def exit(self):
        self.server.close()

    #Handle file request from a peer
    def process_message(self, conn,addr):
        """
        Arguments:
        self -- self object
        conn -- socket object for an accepted connection from a peer
        addr -- address bound to the socket of the accepted connection
        """
        #YOUR code
        #Step 1. read the file name contained in the request
        # read the file name from the connection
        data = ""
        while True:
            part = conn.recv(self.BUFFER_SIZE)
            data = data + part
            if len(part) < self.BUFFER_SIZE:
                break

        #Step 2. read the file from local directory (assuming binary file < 4MB)
        # open the file and stores its contents in a string
        a = open(data, "r")
        file = a.read()

        #Step 3. send the file to the requester
        # send the contents of the file over the connection
        conn.send(file)

    def run(self):
        self.client.connect((self.trackerhost,self.trackerport))
        t = Timer(2, self.sync)
        t.start()
        print('Waiting for connections on port %s' % (self.port))
        while True:
            conn, addr = self.server.accept()
            Thread(target=self.process_message, args=(conn,addr)).start()

    #Send Init or KeepAlive message to tracker, handle directory response message
    #and call self.syncfile() to request files from peers
    def sync(self):
        print 'connect to:'+self.trackerhost,self.trackerport
        #Step 1. send Init msg to tracker
        #YOUR CODE
        # send the most recent message to the tracker
        self.client.send(json.dumps(self.msg))

        #Step 2. receive a directory response message from tracker
        #YOUR CODE
        # get the directory info over the connection
        directory_response_message = ""
        # recive data
        while True:
            part = self.client.recv(self.BUFFER_SIZE)
            directory_response_message = directory_response_message + part
            if len(part) < self.BUFFER_SIZE:
                break

        direc = json.loads(directory_response_message)

        #Step 3. parse the directory response message. if it contains new or
        #more up-to-date files, request the files from the respective peers.
        #NOTE: compare the modified time of the files in the message and
        #that of local files of the same name.
        #YOUR CODE

        # for each file in the directory, check if it its name already exists for this peer.
        # if it does not, then it is a new file and so we can create a new socket 
        # to request the file. we connect to the peer that is hosting the file 
        # to sync. as well, if the file name does already exist, but has been more
        # recently modified, there will be a request for the new file.
        for filename, info in direc.iteritems():
            if filename not in [f["name"] for f in get_file_info()]:
                s = socket(AF_INET, SOCK_STREAM)
                s.connect((info["ip"], info["port"]))
                s.send(filename)
                newfile = ""
                while True:
                    part = s.recv(self.BUFFER_SIZE)
                    newfile = newfile + part
                    if len(newfile) < self.BUFFER_SIZE:
                        break
                print(newfile)
                text_file = open(filename, "w")
                text_file.write(newfile)
                text_file.close()
                s.close()

            for f in get_file_info():
                if (filename == f["name"] and info["mtime"] > f["mtime"]):
                    s = socket(AF_INET, SOCK_STREAM)
                    s.connect((info["ip"], info["port"]))
                    s.send(filename)
                    newfile = ""
                    while True:
                        part = s.recv(self.BUFFER_SIZE)
                        newfile = newfile + part
                        if len(newfile) < self.BUFFER_SIZE:
                            break
                    print(newfile)
                    text_file = open(filename, "w")
                    text_file.write(newfile)
                    text_file.close()
                    s.close()

        #Step 4. construct the KeepAlive message
        self.msg = {"port" : self.port} #YOUR CODE

        #Step 4. start a timer
        t = Timer(5, self.sync)
        t.start()

if __name__ == '__main__':
    #parse commmand line arguments
    parser = optparse.OptionParser(usage="%prog ServerIP ServerPort")
    options, args = parser.parse_args()
    if len(args) < 1:
        parser.error("No ServerIP and ServerPort")
    elif len(args) < 2:
        parser.error("No ServerIP or ServerPort")
    else:
        if validate_ip(args[0]) and validate_port(args[1]):
            tracker_ip = args[0]
            tracker_port = int(args[1])

        else:
            parser.error("Invalid ServerIP or ServerPort")

    #get the next available port
    synchronizer_port = get_next_avaliable_port(8000)
    synchronizer_thread = FileSynchronizer(tracker_ip,tracker_port,synchronizer_port)
    synchronizer_thread.start()
