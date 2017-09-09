import io
import socket
import sys


class WsgiSw:
    def __init__(self, application):
        self.application = application
        self.env         = {}
        self.headers_set = []
        
        self.ip          = socket.gethostbyname('localhost')
        self.port        = 80
        
        self.sock        = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip,self.port))
        self.sock.listen(1)
        print("WsgiSw has started on",self.ip,self.port)

    def serve_forever(self):
        while True:
            self.client_conn, client_add = self.sock.accept()
            print(client_add,"has requested")
            
            self.request  = self.client_conn.recv(2048).decode()
            self.parse_request(self.request)


    def parse_request(self,request):
        request_initial_line = request.splitlines()[0]
        self.request_method, self.path, self.http_ver = request_initial_line.split()

        self.finish_response()

    def fill_environ(self):
        self.env['wsgi.version']      = (1, 0)
        self.env['wsgi.url_scheme']   = 'http'
        self.env['wsgi.input']        = io.StringIO(self.request)
        self.env['wsgi.errors']       = sys.stderr
        self.env['wsgi.multithread']  = False
        self.env['wsgi.multiprocess'] = False
        self.env['wsgi.run_once']     = False
        self.env['REQUEST_METHOD']    = self.request_method
        self.env['PATH_INFO']         = self.path
        self.env['SERVER_NAME']       = 'cr1Server'
        self.env['SERVER_PORT']       = str(self.port)


    def start_response(self, status, response_headers, exc_info = None):
        self.headers_set[:] = status, response_headers

    def finish_response(self):
        self.fill_environ()

        data     = self.application(self.env, self.start_response)
        status   = self.headers_set[0]
        
        response = ""
        for i in data:
            response += i.decode()

        self.client_conn.send(("HTTP/1.1 {}\n\n{}".format(status,response)).encode())
        self.client_conn.close()
        
        


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide a WSGI app in 'module:app' format")
    else:
        app_path       = sys.argv[1]
        module, app    = app_path.split(":")
        module         = __import__(module)
        app            = getattr(module, app) 

        server = WsgiSw(app)
        server.serve_forever()
    
