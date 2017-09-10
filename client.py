import socket

def make_request():
    url       = input("Please enter the url: ")
    host,path = parse_url(url)
    
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ip   = socket.gethostbyname(host)
    port = 80
    sock.connect((ip,port))
    
    sock.send(("GET /{} HTTP/1.1\nHost: {}\nConnection: keep-alive\n\n".format(path,host)).encode())
    response = sock.recv(2048).decode()
    sock.close()
    
    return response


def parse_url(url):
    if "/" in url:
        host, path = url.split("/")
        return host, path
    else:
        host = url
        path = ""
        return host, path

    
    

print(make_request())
