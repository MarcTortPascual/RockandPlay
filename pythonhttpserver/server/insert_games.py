import sqlite3, json

con = sqlite3.connect("../db/Rockandplaydb.db")
cur = con.cursor()

with open("../db/leage/juegos.json") as games:
    data = json.loads(games.read())
    for i in data["video_games"]:
        try:
            cur.execute(f"insert into Games (id,name,genere,description,image,link,developer) values (null,'{i['name']}','{i['genere']}','{i['description']}','{i['image']}','{i['link']}','{i['developer']}')")
            cur.execute("COMMIT")
        except sqlite3.Error:
            continue

    