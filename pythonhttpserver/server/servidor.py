import httpclass
import json
import platform
import hashlib
import sqlite3
from ascii2utf import *

con = sqlite3.connect("../db/Rockandplaydb.db")
cur = con.cursor()

VERSION=platform.python_version()


class api(httpclass.httpmessage):
    def __init__(self):
        super().__init__()
        
    def Do_Head(self):
        if self.path == "/":
            self.send_code(200)
            self.send_header("Server", "Mtcraft_http_server")
            self.send_header("content-type", httpclass.httpmimes["html"])
            self.end_header()
        else:
            try:
                self.send_code(200)
                self.send_header("Server", "Mtcraft_http_server")
                self.send_header(
                    "content-type", httpclass.httpmimes[self.path.split(".")[1]]
                )
                with open(f".{self.path}","rb") as html:
                    html = html.read()

                self.send_header("content-Lenght", str(len(html )))
                self.end_header()
            except IndexError:
                self.send_code(400)
                self.send_header("Archivo", "No lo es")
                self.end_header()
            except FileNotFoundError:
                self.send_code(404)
                self.send_header("Server", f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
                self.send_header("Archivo", "No encontrado")
                self.end_header()

    def Do_get(self):
        print("loged", self.sessions)
        if "db" in self.path:
            self.send_code(400)
            self.send_header("Server", f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
            self.send_header("content-type", httpclass.httpmimes["html"])
            self.end_header()
            self.send_body("""<h1>no permitido</h1>""")

        if self.path == "/":
            self.send_code(200)
            self.send_header("Server", f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
            self.send_header("content-type", httpclass.httpmimes["html"])
            self.end_header()
            with open("../main.html", "r") as body:
                html = body.read()
            self.send_body(html)
        
        else:
            try:
                with open(f"./../{self.path}", "rb") as body:
                    html = body.read()
               
                self.send_code(200)
                self.send_header("Server", f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
                self.send_header(
                    "content-type", httpclass.httpmimes[self.path.split(".")[1]]
                )
                
                self.send_header("content-Lenght", str(len(html)))
                self.end_header()
                if(
                    httpclass.httpmimes[self.path.split(".")[1]].split("/")[0]
                    in "audiovideoimagefont"
                ):
                    self.send_binary(html)
                else:
                    self.send_body(html.decode())
            except IndexError:
                self.send_code(400)
                self.send_header("Server", f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
                self.send_header("Archivo", "No lo es")
                self.end_header()
            except FileNotFoundError:
                self.send_code(404)
                self.send_header("Server", f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
                self.send_header("Archivo", "No encontrado")
                self.end_header()

    def Do_post(self):
        self.Post = {}
        try:
            
            valores = self._message.splitlines()[-1]
            if "&" in valores:
                for i in valores.split("&"):
                    if i.split("=")[0] in self.Post:
                        print (type(self.Post[i.split("=")[0]]))
                        
                        if type(self.Post[i.split("=")[0]]) != list:
                            prev = self.Post[i.split("=")[0]]
                            self.Post[i.split("=")[0]]=list(self.Post[i.split("=")[0]])
                            self.Post[i.split("=")[0]].clear()
                            self.Post[i.split("=")[0]].append(prev)  
                            self.Post[i.split("=")[0]].append(i.split("=")[1])
                        else:
                            self.Post[i.split("=")[0]].append(i.split("=")[1]) 
                    else:
                        self.Post[i.split("=")[0]] = i.split("=")[1]
            else:
                self.Post[valores.split("=")[0]]=valores.split("=")[1]
        except  IndexError:
            self.Post={}
        if self.path == "/usuarios": #alta de un usuario
            user = {}
            self.Post["contra"] = hashlib.sha512(str(self.Post["contra"]).encode("utf-8")).hexdigest()
            try:
            
                cur.execute(f"INSERT INTO Players (id,name,last_name,password,email,genere) VALUES (NULL,?,?,?,?,?)",(f"{self.Post['nombre'].lower()}",f"{self.Post['apedillo'].lower()}",f"{self.Post['contra']}",f"{self.Post['correo'].lower()}",f"{self.Post['genero'].lower()}"))
                cur.execute("COMMIT")
                user["nombre"] = self.Post['nombre']
                user["apedillo"] = self.Post['apedillo']
                user["contra"] = self.Post['contra']
                user["correo"] = self.Post['correo']
                user["genero"] = self.Post['genero']
                user["juegos"] = []
                Player_id_cur = cur.execute(f"Select id from Players where name= ?",(f"{self.Post['nombre'].lower()}",))
                for i in Player_id_cur:
                    Player_id = i[0]
                    user["id"] = Player_id
                try:
                    if type(self.Post["juegos"]) == list:
                        for i in self.Post["juegos"]:
                            a = i.replace("+"," ")
                            user["juegos"].append(a)
                            juego_id_cur = cur.execute(f"SELECT id from Games where name= ?",(f"{a}",))
                            for j in juego_id_cur:
                                
                                cur.execute(f"insert into Games_Players (id_Game,id_player) values (?,?)",(f"{int(j[0])}",f"{int(Player_id)}"))
                                cur.execute("commit")
                    else:
                        
                        a = self.Post["juegos"].replace("+"," ")
                        user["juegos"].append(a)
                
                        juego_id_cur = cur.execute(f"SELECT id from Games where name= ?",(f"{a}",))
                        for j in juego_id_cur:
                            
                            cur.execute(f"insert into Games_Players (id_Game,id_player) values (?,?)",(f"{int(j[0])}",f"{int(Player_id)}"))
                            cur.execute("commit")
                except KeyError:
                    pass #no insertamos nigún juego
                self.sessions[hashlib.sha256(str(user['nombre']).encode("utf-8")).hexdigest()]=user
                self.send_code(200)
                self.send_header("Server", f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
                self.send_header("Set-cookie",f"session-id={hashlib.sha256(str(user['nombre']).encode('utf-8')).hexdigest()}")
                self.end_header()
                self.send_body(f"""<html lang='en'><head>
<meta charset='UTF-8'>
<meta http-equiv='X-UA-Compatible' content='IE=edge'>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
<title>Usuario creado</title>
<link rel='stylesheet' href='/css/main.css'>
</head>
<html>
<h1>Usuario creado</h1>
<a href='http://{httpclass.ip}:{httpclass.port}/catalogo.html'>Visite su catalogo.</a>
</html>""")
            except sqlite3.IntegrityError:
                self.send_code(200)
                self.send_header("Server", f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
                self.end_header()
                self.send_body(f"""<html lang='en'><head>
<meta charset='UTF-8'>
<meta http-equiv='X-UA-Compatible' content='IE=edge'>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
<title>Error de vadilación</title>
<link rel='stylesheet' href='/css/main.css'>
</head>
<html>
<h1>Usuario o correo duplicado, intente de nuevo.</h1>
<a href='http://{httpclass.ip}:{httpclass.port}/liga.html'>Registro</a>
</html>""")


        elif self.path == "/logedinfo":
            try:
                for cookie in self.headers["Cookie"].split(";"):
                    if "session-id" in cookie.split("=")[0]:
                        print("value",cookie.split("=")[1] )
                        id =  cookie.split("=")[1]
                        self.send_code(200)
                        self.send_header("Server", f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
                        self.send_header("content-type", httpclass.httpmimes['json'])
                        self.end_header()
                        self.sessions[id[:-1]]["loged"]=True
                        self.send_body(json.dumps(self.sessions[id[:-1]]))
                        
            except KeyError:
                self.send_code(200)
                self.send_header("Server", f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
                self.send_header("content-type", httpclass.httpmimes['json'])
                self.end_header()
                self.send_body(json.dumps({"loged":False}))
        
        elif self.path == "/apcetar":
            if "Cookie" in self.headers:
                for cookie in self.headers["Cookie"].split(";"):
                    if "session-id" in cookie.split("=")[0]:
                        print("value",cookie.split("=")[1] )
                        id =  cookie.split("=")[1]
                        game = self.Post["game"].replace("+"," ")
                        self.sessions[id[:-1]]["juegos"].append(game)
                        cur.execute("Insert into Games_Players(id_Game,id_player) values ((select id from Games where name = ?),?)",(f'{game}',self.sessions[id[:-1]]["id"]))
                        cur.execute("commit")
                        self.send_code(200)
                        self.send_header("Server", f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
                        self.end_header()
                        self.send_body(f"""<html lang='en'><head>
<meta charset='UTF-8'>
<meta http-equiv='X-UA-Compatible' content='IE=edge'>  
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
<title>Liga de juegos</title>
<link rel='stylesheet' href='/css/main.css'>
</head>
<html>
<h1>Inscrito en {convert_ascii(self.Post["game"])}</h1>
<a href='http://{httpclass.ip}:{httpclass.port}/catalogo.html'>Ir a catalogo</a>
</html>""")
        elif self.path == "/cancelar":
            if "Cookie" in self.headers:
                for cookie in self.headers["Cookie"].split(";"):
                    if "session-id" in cookie.split("=")[0]:
                        print("value",cookie.split("=")[1] )
                        id =  cookie.split("=")[1]
                        game = self.Post["game"].replace("+"," ")
                        try:
                            self.sessions[id[:-1]]["juegos"].remove(game)
                            cur.execute("delete from Games_Players where id_Game = (select id from Games where name = ?) and id_player = ?",(f'{game}',self.sessions[id[:-1]]["id"]))
                            cur.execute("commit")
                            self.send_code(200)
                            self.send_header("Server", f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
                            self.end_header()
                            self.send_body(f"""<html lang='en'><head>
    <meta charset='UTF-8'>
    <meta http-equiv='X-UA-Compatible' content='IE=edge'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Liga de juegos</title>
    <link rel='stylesheet' href='/css/main.css'>
    </head>
    <html>
    <h1>Eliminado de {convert_ascii(self.Post["game"])}</h1>
    <a href='http://{httpclass.ip}:{httpclass.port}/catalogo.html'>Ir a catalogo</a>
    </html>""")         
                        except ValueError:
                            self.send_code(200)
                            self.send_header("Server", f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
                            self.end_header()
                            self.send_body(f"""<html lang='en'><head>
    <meta charset='UTF-8'>
    <meta http-equiv='X-UA-Compatible' content='IE=edge'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Liga de juegos</title>
    <link rel='stylesheet' href='/css/main.css'>
    </head>
    <html>
    <h1>Ya estabas eliminado de {self.Post["game"]}</h1>
    <a href='http://{httpclass.ip}:{httpclass.port}/catalogo.html'>Ir a catalogo</a>
    </html>""")  


        elif self.path == "/catalogo":
            if "Cookie" in self.headers:
                    for cookie in self.headers["Cookie"].split(";"):
                        if "session-id" in cookie.split("=")[0]:
                            try:
                                user =  self.sessions[cookie.split("=")[1][:-1]]
                            except KeyError:
                                self.send_code(403)
                                self.send_header("Server",f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
                                self.end_header()
                                self.send_body("""<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta http-equiv='X-UA-Compatible' content='IE=edge'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Liga de juegos</title>
    <link rel='stylesheet' href='/css/main.css'>
</head>
<body><h1>No disponible</h1></body>
""")
                            try:
                                games = user["juegos"]
                            except KeyError:
                                games = []
                            GamesDB = {}
                            GamesDB["video_games"] = []
                            
                            Games_cur = cur.execute("select * from Games").fetchall()
                            for i in Games_cur:
                                Game = {}
                                Game["name"] = i[1]
                                Game["display_name"] = Game["name"].replace("+"," ")
                                Game["genere"] = i[2]
                                Game["developer"]= i[3]
                                Game["description"]= i[4]
                                Game["image"]= i[5]
                                Game["link"]= i[6]
                                GamesDB["video_games"].append(Game)
                            for i in GamesDB["video_games"]:
                                if (i["name"] in games):
                                    i["subscrito"] = True
                                else:
                                    i["subscrito"] = False
                            self.send_code(200)
                            self.send_header("Server",f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
                            self.send_header("content-type",httpclass.httpmimes["json"])
                            self.end_header()
                            self.send_body(json.dumps(GamesDB, indent=4))


            else:
                self.send_code(403)
                self.send_header("Server",f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
                self.end_header()
                self.send_body("""<!DOCTYPE html>
<html lang='en'><head>
    <meta charset='UTF-8'>
    <meta http-equiv='X-UA-Compatible' content='IE=edge'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Liga de juegos</title>
    <link rel='stylesheet' href='/css/main.css'>
</head>""")
        elif self.path == "/logout":
            if "Cookie" in self.headers:
                    for cookie in self.headers["Cookie"].split(";"):
                        if "session-id" in cookie.split("=")[0]:
                            print("value",cookie.split("=")[1] )
                            
                            id =  cookie.split("=")[1]
                            self.sessions.pop(id[:-1])
                            
            self.send_code(200)
            self.send_header("Set-cookie",f"session-id={cookie.split('=')[1][:-1]};Expires=Thu,01 Jan 1970 00:00:00 GMT")
            self.end_header()
            self.send_body("""<!DOCTYPE html>
<html lang='en'><head>
    <meta charset='UTF-8'>
    <meta http-equiv='X-UA-Compatible' content='IE=edge'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Liga de juegos</title>
    <link rel='stylesheet' href='/css/main.css'>
</head>""")
            self.send_body(f"<h1> Sessión cerrada </h1>")
            self.send_body(f"<a href='http://{httpclass.ip}:{httpclass.port}/liga.html'>Inicio </a>")
            

        elif self.path == "/login":
            user = {}
            Player_cur = cur.execute(f"select * from Players where name = ?",(f"{self.Post['user'].lower()}",))
            i = Player_cur.fetchone()
            if i != None:
                print("player" , i)
                user ["id"] = i[0]
                user ["nombre"] = i[1]
                user ["apedillo"] = i[2]
                user ["contra"] = i[3]
                user ["correo"] = i[4]
                user ["juegos"] = []
                user ["genero"] = i[5]
                juegos_jugadores_cur = cur.execute(f"select id_game from Games_Players where id_player = ?",(f"{user ['id']}",)).fetchall()
                for i in juegos_jugadores_cur:
                    
                    juego_cur = cur.execute(f"select name from Games where id = ?",(f"{int(i[0])}",)).fetchall()
                    print("hola", juego_cur)
                    user ["juegos"].append(juego_cur[0][0])
                    print("\n",user , "\n")
                
                    
                if user["contra"]==hashlib.sha512(str(self.Post["password"]).encode("utf-8")).hexdigest() and user["correo"]==self.Post["email"]:
                    self.send_code(200)
                    self.send_header(
                    "content-type", "text/html"
                    )
                    self.send_header("Set-cookie",f"session-id={hashlib.sha256(str(user['nombre']).encode('utf-8')).hexdigest()}")
                    self.end_header()
                    self.sessions[hashlib.sha256(str(user['nombre']).encode("utf-8")).hexdigest()]=user
                    self.send_body("""<!DOCTYPE html>
<html lang='en'><head>
<meta charset='UTF-8'>
<meta http-equiv='X-UA-Compatible' content='IE=edge'>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
<title>Liga de juegos</title>
<link rel='stylesheet' href='/css/main.css'>
</head>""")
                    self.send_body(f"<h1>Hola {convert_ascii(user['nombre'])[0].upper() + convert_ascii(user['nombre'])[1:]}</h1>")
                    self.send_body(f"<a href='http://{httpclass.ip}:{httpclass.port}/liga.html'>Vuelve al inicio</a>")
                else:
                    self.send_code(403)
                    self.send_header("Server", f"Mtcraft_http_server(Python {VERSION} on {platform.system()})")
                    self.end_header()
                    self.send_body(f"""<html lang='en'><head>
<meta charset='UTF-8'>
<meta http-equiv='X-UA-Compatible' content='IE=edge'>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
<title>Error de inicio de session</title>
<link rel='stylesheet' href='/css/main.css'>
</head>
<html>
<h1>Usuario o contraseña incorrectos</h1>
<a href='http://{httpclass.ip}:{httpclass.port}/liga.html'>Intente de nuevo</a>
</html>""")
            else:
                self.send_code(403)
                self.send_header(
                "content-type", "text/html"
                )
                self.end_header()
                self.send_body(f"""<!DOCTYPE html>
<html lang='en'><head>
<meta charset='UTF-8'>
<meta http-equiv='X-UA-Compatible' content='IE=edge'>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
<title>Error de inicio de sessión</title>
<link rel='stylesheet' href='/css/main.css'>
<body>                       
    <h1>Usuario no registrado</h1>
    <a href='http://{httpclass.ip}:{httpclass.port}/liga.html'>Registro</a>
</body>
</head>""")
            
        elif self.path == "/validar":
            print(self.Post)
            Valilate = False
            try:
                email = self.Post['email'].lower()
                val_Play = cur.execute(f"select name,email from Players where name = ?and email = ?",(f"{encode_ascii(self.Post['user'].lower())}",f"{encode_ascii(email)}"))
                Player = val_Play.fetchall()
                print(Player)
                if len(Player)==1:
                    Valilate = True
            except sqlite3.Error():
                Valilate = False
            finally:
                self.send_code(200)
                self.send_header(
                "content-type", f" {httpclass.httpmimes['json']}"
                )
                self.end_header()
                resp = json.dumps({"valido":Valilate})
                self.send_body(resp)
        elif self.path == "/getgames":
            GamesDB = {}
            GamesDB["video_games"] = []
            
            Games_cur = cur.execute("select * from Games").fetchall()
            for i in Games_cur:
                Game = {}
                Game["name"] = i[1]
                Game["display_name"] = Game["name"].replace("+"," ")
                Game["genere"] = i[2]
                Game["developer"]= i[3]
                Game["description"]= i[4]
                Game["image"]= i[5]
                Game["link"]= i[6]
                GamesDB["video_games"].append(Game)
            self.send_code(200)
            self.send_header(
            "content-type", httpclass.httpmimes["json"]
            )
            
            self.end_header()
            self.send_body(json.dumps(GamesDB))


Api = api()
print("Servidor Iniciado")
Api.run_forever()
