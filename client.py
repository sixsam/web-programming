import argparse,random,socket,zen_utils

def client(address,cause_error=False):
    sock=socket.socket(socket.AF_INET,  socket.SOCK_STREAM) 
    sock.connect(address)
    aphorisms=list(zen_utils.aphorisms)
    if cause_error:
        sock.sendall(aphorisms[0][:-1])
        return
    for aphorism in random.sample(aphorisms,3):
        sock.sendall(aphorism)
        print(aphorism,zen_utils(sock,b'.'))
    sock.close()

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='example client')
    parser.add_argument('host',help='ip or address')
    parser.add_argument('-e',action='store_True',help='cause an error')
    parser.add_argument('-p',metavar='port',type=int,default=1060,help='tcp port (default 1060)')
    args=parser.parse_args()
    address=(args.host,args.p)
    client(address,args.e)