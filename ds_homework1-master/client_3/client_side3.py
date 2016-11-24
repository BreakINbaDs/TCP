from socket import AF_INET, SOCK_STREAM, socket
from socket import error as SocketError
import GUI

if __name__ == '__main__':

    print 'Application started'

    s = socket(AF_INET, SOCK_STREAM)
    print 'TCP Socket created'

    server_adress = ('127.0.0.1',50003)

    try:
        s.connect(server_adress)
        decision = ''
        filename = ''
        password = ''

        print 'Socket connected to %s:%d' % s.getpeername()
        print 'Local end-point is  bound to %s:%d' % s.getsockname()
        print 'Please enter 1 if you want to upload your file.\nPlease enter 2 if you want to create New File.\nPlease enter 3 if you want to open existing file.\n'
        decision=raw_input('Waiting for decision...: ')
        s.send(decision)
        if decision == '1':
            listOfFiles =  s.recv(1024)
            print 'The list of existing files on the server: ', listOfFiles
            filename=raw_input('Enter file name: ')
            s.send(filename)
            password=raw_input('Please, a password for a file: ')
            s.send(password)
            f = open(filename, 'rb')
            while True:
                l = f.read(1024)
                s.send(l)
                if not l:
                    s.send('STOP')
                    break
            print 'Done sending'
            result = s.recv(1024)
            client_GUI = GUI.GUI(filename, s)

        elif decision == '2':
            listOfFiles = s.recv(1024)
            print 'The list of existing files on the server: ', listOfFiles
            filename = raw_input('Please, enter a name of the file to create: ')
            s.send(filename)
            password = raw_input('Please, set a password for a file:')
            s.send(password)
            client_GUI = GUI.GUI(filename, s)

        elif decision == '3':
            listOfFiles = s.recv(1024)
            print 'The list of existing files on the server: ', listOfFiles
            filename = raw_input('Please, enter a name of the file you want to open: ')
            s.send(filename)
            password = raw_input('Please, a password for a file: ')
            s.send(password)
            with open(str(filename), 'wb') as f:
                data = s.recv(1024)
                while data:
                    print('receiving data...')
                    #print('data:', (data))
                    if data[-4:] == 'STOP':
                        f.write(data[:-4])
                        break
                    else:
                        f.write(data)
                    data = s.recv(1024)
            f.close()
            client_GUI = GUI.GUI(filename, s)

        else:
            print 'Wrong input.'

    except SocketError:
        print " Communication ERROR "

    finally:
        raw_input('Press Enter to terminate ...')
        s.close()
        print 'Terminating ...'
