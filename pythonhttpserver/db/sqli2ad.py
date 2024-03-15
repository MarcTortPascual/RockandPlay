import logging
import sqlite3
import sys
from tkinter import filedialog
import platform
import os, os.path

ascii_dict = {
    "%40": "@",
    "%c3%a1": "á",
    "%c3%a9": "é",
    "%c3%ad": "í",
    "%c3%b3": "ó",
    "%c3%ba%0d%0a": "ú"
}

def convert_ascii(string: str) -> str:
    for char in ascii_dict:
        string = string.replace(char, ascii_dict[char])
    return string

if platform.system() != "Windows":
    logging.error(f"This script only works on Microsoft Windows machines. However, your machine is running {platform.system() if platform.system() == "" else "an unknown OS"}.")
    sys.exit(1)
if __name__ != "__main__":
    logging.error(f"This script cannot be started as a module. This can be solved by running 'python {__name__}.py'.")
    sys.exit(1)

default_password: str
try:
    with open("./default_password", "rt") as passwd:
        default_password = passwd.read()

    print("Select the .db file to import to the AD database.")

    db_path = filedialog.askopenfilename(defaultextension=".db")
    if db_path != "":
        db_name = os.path.basename(db_path)

        print(f"Connecting to {db_name}...")
        conn = sqlite3.Connection(db_path)
        print(f"Connected successfully to {db_name}. Retrieving user data...")
        cur = conn.cursor()
        users = cur.execute("SELECT name, last_name, email FROM Players").fetchall()

        print(f"Retrieved {len(users)} user(s) from {db_name}.")

        decision = ""

        if len(users) > 0:
            if len(default_password) > 14:
                print(f"WARNING: the default password is {len(default_password)} characters long. Users in {db_name} won't be able to log in on Windows 2000 and earlier machines.")
                decision = input("Do you want to continue? (Y/N) [Y]: ").lower()

            if decision != "n":
                for user in users:
                    name: str = convert_ascii(user[0])
                    surname: str = convert_ascii(user[1])
                    email: str = convert_ascii(user[2])

                    print(f"Adding user {name} {surname} as {email.split("@")[0]} with password {default_password}...")

                    os.system(f"net user {email.split("@")[0]} \"{default_password}\" /add /fullname:\"{name} {surname}\" /logonpasswordchg:yes /times:lunes-viernes,9-12;lunes-viernes,16-20 /domain /y")
        else:
            logging.warning(f"No users found in {db_name}. Exiting...")
except Exception as e:
    logging.error(f"Something happened: {e}")