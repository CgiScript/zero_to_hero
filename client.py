import socket

def make_request():
    url  = input("Please enter the url: ")
    
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ip   = socket.gethostbyname(url)
    port = 80
    sock.connect((ip,port))
    
    sock.send(("GET / HTTP/1.1\nHost: {}\nConnection: keep-alive\n\n".format(url)).encode())
    response = sock.recv(2048).decode()
    sock.close()
    
    return response
    

print(make_request())
