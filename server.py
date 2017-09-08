import socket

IP   = socket.gethostbyname("localhost")
PORT = 80

#IPv4(socket.AF_INET) ve TCP(socket.SOCK_STREAM) üzerine kurulu bir socket nesnesi oluştur.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#IP ve PORT bilgilerini sockete bağla.
sock.bind((IP,PORT))
#Socketi çalıştır. 
sock.listen(1)
print("Server has started...")


while True:
    #accept methodu ile gelen isteği kabul et.
    #Method, bir client bağlantı nesnesi ve ve clientin adres bilgisini döndürür.
    client_connection, client_address = sock.accept()
    #Oluşturulan bağlantı nesnesi ile gelen mesajı oku.
    request = client_connection.recv(2048)
    print(request)
    #sendall methodu ile cliente yanıt gönder. 
    client_connection.sendall("HTTP/1.1 200 OK\n\n<b>Server is Running".encode())
    client_connection.close()
