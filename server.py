import socket
import sqlite3
import json
from prettytable import PrettyTable

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 8000))

database = sqlite3.connect("db.sqlite3")
cursor = database.cursor()

while True:
    server.listen(1)
    conn, cli = server.accept()
    data = json.loads(conn.recv(255))

    if "add" in data:
        try:
            id = cursor.execute("SELECT MAX(ID) FROM PASSWORDS;").fetchone()[0]
            cursor.execute("""
                INSERT INTO PASSWORDS (ID, USERNAME, SITE, PASSWORD) VALUES (?,?,?,?);
            """, [(id := int(id) + 1), data["username"], data["site"], data["key"]])

            database.commit()
            conn.send("Success!".encode())
        except:
            id = cursor.execute("SELECT MAX(ID) FROM PASSWORDS;").fetchone()[0]
            cursor.execute("""
                INSERT INTO PASSWORDS (ID, USERNAME, SITE, PASSWORD) VALUES (?,?,?,?);
            """, [0, data["username"], data["site"], data["key"]])

            database.commit()
            conn.send("Success!".encode())

    else:
        if data["decrypt_password"] and not data["choose_password"]:
            cursor.execute("""
                SELECT ID, USERNAME, SITE FROM PASSWORDS;
            """)

            table = PrettyTable()
            table.field_names = ["id", "username", "site"]

            for database_data in cursor.fetchall():
                table.add_row(database_data)

            conn.send(f"{ table }".encode())

        if data["choose_password"]:

            cursor.execute("""
                SELECT password FROM PASSWORDS WHERE ID=?
            """, [data["password_number"]])

            conn.send(cursor.fetchone()[0].encode())
