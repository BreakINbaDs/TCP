from socket import AF_INET, SOCK_STREAM, socket
from socket import error as SocketErrors
from text_file import File
from class_queue import Queue
import sys
from threading import Thread



class Server:

    def __init__(self):
        self.host = '127.0.0.1'       # ip server's address
        self.port1 = 50001    # server's port
        self.port2 = 50002
        self.port3 = 50003
        self.backlog = 0     # at most server will work with three clients
        self.size = 1024     # max message size
        self.server = None
        self.threads = []

    def file_syncronization(self, triple, text, client_socket, queue, port, filename):

        if port == self.port1:
            queue.add_user1(triple)
            i,j,elem = text.parse_triple(triple)
            text.change(i,j,elem)
            text.upload_to_txt(filename)

        if port == self.port2:
            queue.add_user2(triple)
            i,j,elem = text.parse_triple(triple)
            text.change(i,j,elem)
            text.upload_to_txt(filename)

        if port == self.port3:
            queue.add_user3(triple)
            i,j,elem = text.parse_triple(triple)
            text.change(i,j,elem)
            text.upload_to_txt(filename)

    def edit_function(self, text, client_socket, port,queue, filename):
        while True:
            print 'YA TUT'
            triple = client_socket.recv(1024)
            if triple != 'Nothing':
                self.file_syncronization(triple, text, client_socket, queue, port,filename)

            if port == self.port1:
                print queue.q_user2.__len__()
                while queue.q_user2.__len__() != 0:
                    client_socket.send(queue.take2())
                while queue.q_user3.__len__() != 0:
                    client_socket.send(queue.take3())
                if queue.q_user2.__len__() == 0:
                    client_socket.send('Nothing')
                if queue.q_user3.__len__() == 0:
                    client_socket.send('Nothing')

            if port == self.port2:
                print queue.q_user2.__len__()
                while queue.q_user1.__len__() != 0:
                    client_socket.send(queue.take1())
                while queue.q_user3.__len__() != 0:
                    client_socket.send(queue.take3())
                if queue.q_user1.__len__() == 0:
                    client_socket.send('Nothing')
                if queue.q_user3.__len__() == 0:
                    client_socket.send('Nothing')

            if port == self.port3:
                while queue.q_user1.__len__() != 0:
                    client_socket.send(queue.take1())
                while queue.q_user2.__len__() != 0:
                    client_socket.send(queue.take2())
                if queue.q_user1.__len__() == 0:
                    client_socket.send('Nothing')
                if queue.q_user2.__len__() == 0:
                    client_socket.send('Nothing')

    def check_file_names(self, filename):
        file = open('passwords.txt', 'r')
        names = []
        for line in file:
            names.append(line.split(';-')[0])
        if filename in names:
            file.close()
            return True
        else:
            file.close()
            return False

    def check_pass(self, filename, password):
        passes = {}
        if self.check_file_names(filename):
            file = open('passwords.txt', 'r')
            for line in file:
                l = line.split(';-')
                passes[l[0]] = l[1].strip()
            if passes[filename] == password:
                file.close()
                return True
            else:
                file.close()
                return False

    def list_of_files(self):
        files = ''
        file = open('passwords.txt', 'r')
        for line in file:
            files += str(line.split(';-')[0]) + ' '
        file.close()
        return files

    def open_socket(self, port,text,queue):
        try:
            self.server = socket(AF_INET, SOCK_STREAM)
            self.server.bind((self.host, port))
            self.server.listen(self.backlog)
            print str(port) + ' port ' + 'is open for accepting clients clients'
            while True:
                client_socket, client_addr = self.server.accept()
                print 'New Client has been connected!'
                decision = client_socket.recv(1024)

                if decision == '1':
                    ListOfFiles = self.list_of_files()
                    client_socket.send(ListOfFiles)
                    filename = client_socket.recv(1024)
                    password = client_socket.recv(1024)
                   # if self.check_file_names(filename):
                       ### passes.close()
                    with open(str(filename), 'wb') as f:
                         print 'file %s opened' % str(filename)
                         data = client_socket.recv(1024)
                         while data:
                                print('receiving data...')
                                f.write(data)
                                if data[-4:] == 'STOP':
                                    break
                                else:
                                    data = client_socket.recv(1024)
                    f.close()
                    #client_socket.send('Done receiving!')
                    print 'KUKU'
                    text.download_from_txt(filename)
                    #text.download_from_txt(filename)
                    print 'oooP'
                    self.edit_function(text, client_socket, port,queue, filename)

                elif decision == '2':
                    ListOfFiles = self.list_of_files()
                    client_socket.send(ListOfFiles)
                    filename = client_socket.recv(1024)
                    password = client_socket.recv(1024)
                    if self.check_file_names(filename):
                        passes = open('passwords.txt', 'a')
                        passes.write(str(filename) + ';-' + str(password) + '\n')
                        passes.close()
                        text.download_from_txt(filename)
                        self.edit_function(text, client_socket, port,queue, filename)

                elif decision == '3':
                    ListOfFiles = self.list_of_files()
                    client_socket.send(ListOfFiles)
                    filename = client_socket.recv(1024)
                    password = client_socket.recv(1024)
                    if self.check_file_names(filename) and self.check_pass(filename,password):
                        f = open(filename, 'rb')
                        while True:
                            l = f.read(1024)
                            client_socket.send(l)
                            #print('Sent ', repr(l))
                            if not l:
                                client_socket.send('STOP')
                                break
                        f.close()
                        text.download_from_txt(filename)
                        self.edit_function(text, client_socket, port, queue, filename)

                else:
                    client_socket.send('You have made wrong decision. Good luck!\n')

        except SocketErrors, (value, message):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit(1)



if __name__ == '__main__':
    print 'Welcome to the Collaborative Text Editor'
    s = Server()
    queue = Queue()
    text = File()
    thread1 = Thread(target=s.open_socket, args=(s.port1,text,queue))
    thread2 = Thread(target=s.open_socket, args=(s.port2,text,queue))
    thread3 = Thread(target=s.open_socket, args=(s.port3,text,queue))
    s.threads.append(thread1)
    s.threads.append(thread2)
    s.threads.append(thread3)
    for t in s.threads:
        t.start()
        #print 'Servers are born!'
    for t in s.threads:
        t.join()
    #print 'Servers are dead!'



    #############################################
    # ||                                     || #
    # ||          HERE WILL BE BLOCK,        || #
    # ||    WHICH DESCRIBES HOW THE SERVER   || #
    # ||      COMMUNICATE WITH THE CLIENT    || #
    # ||                                     || #
    #############################################