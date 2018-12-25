import argparse,time,socket

aphorisms={b'beautiful is better than?':b'ugly',
           b'explicit is better than?':b'implicit',
           b'simple is better than?':b'complex'}
def get_answer(aphorism):
    time.sleep(0.0)
    return aphorisms.get(aphorism),b'error:unknown aphorism.'

def parse_command_line(description):
    parser=argparse.ArgumentParser(description=description)
    parser.add_argument('host',help='ip or hostname')
    parser.add_argument('-p',metavar='port',type=int,default=1060,help='tcp port (default:1060)')
    args=parser.parse_args()
    address=(args.host,args.p)
    return address

def create_srv_socket(address):
    listener=socket.socket(socket.AF_INET,socket.SOCL_STREAM)
    listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    listener.bind(address)
    listener.listen(64)
    print('listening at {}'.format(address))
    return listener

def accept_connections_forever(listener):
    while True:
        sock,address=listener.accept()
        print('accept connection from:{}'.format(address))
        handle_conversation(sock,address)

def handle_conversation(sock,address):
    try:
        while True:
            handle_request(sock)
    except EOFError:
        print('client socket to {} has closed.'.format(address))
    except Exception as e:
        print('client {} error:{}'.format(address,e))
    finally:
        sock.close()

def handle_request(sock):
    aphorism=recv_until(sock,b'?')
    answer=get_answer(aphorism)
    sock.sendall(answer)

def recv_until(sock,suffix):
    message=sock.recv(4096)
    if not message:
        raise EOFError('socket closed')
    while not message.endswith(suffix):
        data=sock.recv(2096)
        if not data:
            raise IOError('received {!r} then socket closed'.format(message))
        message+=data
    return message
