import socket
# levantamos el socket tcp para cominicanos con el navegador via http
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


port = 8081
#ip = "172.17.113.69"
ip = "172.17.20.38"
print(f"On ip : {ip}")
try:
    servidor.bind((ip, port))
    print(f"On port: {port}")
except OSError:
    port = 8080
    servidor.bind((ip, port))
    print(f"On port: {port}")
servidor.listen(5)
# codigos de estado http
httpstatus = {
    100: "100 Continue",
    200: "200 OK",
    201: "201 Created",
    400: "400 Bad request",
    403: "403 Forbiden",
    404: "404 Page not found",
    500: "500 Internal server error",
    501: "501 Not implemented",
}
# extenciones de archivos mimes

httpmimes = {
    # text files
    "txt": "text/plain",
    "js": "text/javascript",
    "html": "text/html",
    "css": "text/css",
    # images formts
    "jpg": "image/jpg",
    "jpeg": "image/jpeg",
    "gif": "image/gif",
    "png": "image/png",
    "svg": "image/svg+xml",
    "ico": "image/x-incon",
    "webp": "image/webp",
    # binary partition
    "byte_range": "multipart/byteranges",
    "formulario_multiparte": "multipart/form-data",
    # audio
    "waw": "audio/waw",
    "ogg": "audio/ogg",
    "midi": "audio/midi",
    # video
    "mp4": "video/mp4",
    # binario
    "otro": "application/octet-stream",
    "pkcs12": "application/pkcs12",
    "vnd.mspowerpoint": "application/vnd.mspowerpoints",
    "xhtml": "application/xhtml+xml",
    "xml": "application/xml",
    "pdf": "application/pdf",
    "json": "application/json",
    "toml": "text/toml",
    "ttf": "font/ttf"
}


class httpmessage:
    def __init__(self) -> None:
        self._message = None
        self.command = None
        self.path = None
        self.sessions = {}
        self.headers = {}
        self.Post = {}
        self.Get = {}
        self.body = None

    def send_status_code(self, code):
        self._message = f"""
HTTP/1.1 {code}\r\n
        """

    def send_code(self, code):
        self._message = f"HTTP/1.1 {httpstatus[code]}\n"

    def send_header(self, key, value):
        self._message += f"{key}:{value}\n"
    
    def send_binary(self,body):
        self._message = self._message.encode()
        self._message += body
        
    def send_body(self, body):
        try:
            self._message += f"{body}"
        except TypeError:
            self._message = self._message.decode()
            self._message += f"{body}"
        self._message = self._message.encode()

    def end_header(self):
        self._message += "\r\n"

    def Do_Options(self):
        self.send_code(501)
        self.send_header("Server", "Mtcraft_http_server")
        self.end_header()
        self.send_body("hola el metodo no lo he implementaddo")

    def Do_patch(self):
        self.send_code(501)
        self.send_header("Server", "Mtcraft_http_server")
        self.end_header()
        self.send_body("hola el metodo no lo he implementaddo")

    def Do_Put(self):
        self.send_code(501)
        self.send_header("Server", "Mtcraft_http_server")
        self.end_header()
        self.send_body("hola el metodo no lo he implementaddo")

    def Do_Trace(self):
        self.send_code(501)
        self.send_header("Server", "Mtcraft_http_server")
        self.end_header()
        self.send_body("hola el metodo no lo he implementaddo")

    def Do_get(self):
        pass

    def Do_post(self):
        self.send_code(501)
        self.send_header("Server", "Mtcraft_http_server")
        self.end_header()
        self.send_body("hola el metodo no lo he implementaddo")

    def Do_Head(self):
        pass

    def Do_connect(self):
        self.send_code(501)
        self.send_header("Server", "Mtcraft_http_server")
        self.end_header()
        self.send_body("hola el metodo no lo he implementaddo")

    def Do_delete(self):
        self.send_code(501)
        self.send_header("Server", "Mtcraft_http_server")
        self.end_header()
        self.send_body("hola el metodo no lo he implementaddo")

    def run_forever(self):
        while True:
            enchufe, direcion = servidor.accept()
            self._message = enchufe.recv(1024).decode("utf-8")
            self.command = self._message.split(" ")[0]
            try:
                self.path = self._message.split(" ")[1]
            except IndexError as e:
                self.path = ""
            i = 1
            self._message=self._message.replace("\\\\n","\n")
            self._message=self._message.replace("\\\\r","\r")
            print(self._message)

            for line in self._message.split("\n"):
                if ":" in line:
                    value = ""
                    for i in line.split(":")[1:]:
                        value += i
                    self.headers[line.split(":")[0]]= value 
            match self.command:
                case "CONNECT":
                    self.Do_connect()
                case "DELETE":
                    self.Do_delete()
                case "GET":
                    self.Do_get()
                case "HEAD":
                    self.Do_Head()
                case "OPTIONS":
                    self.Do_Options()
                case "PATCH":
                    self.Do_patch()
                case "POST":
                    self.Do_post()  
                case "PUT":
                    self.Do_Put()
                case "TRACE":
                    self.Do_Trace()
            print(self._message)

            try:
                enchufe.send(self._message)
            except TypeError:
                enchufe.send(self._message.encode("utf-8"))
            enchufe.close()
