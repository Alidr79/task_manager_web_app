import random
import os
import sqlite3
import db_work
from werkzeug.security import generate_password_hash

signs = "@#*&$"
digits = "1234567890"
alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
invite_list = set() # to check repeated items

# oops i cant share the seed, but if you want an invite ticket send me an email.
# # *This part is private*
# SEED = ""
# random.seed(SEED)

basedir = os.path.abspath(os.path.dirname(__file__))
SQLite_path = os.path.join(basedir, 'database', 'database.db')
connection = sqlite3.connect(SQLite_path)
connection.row_factory = sqlite3.Row

file = open('invite_codes.txt', 'w')
file.write("Invite_codes\n")
file.write("seed = {}\n".format(SEED))

file.write("_"*30+'\n')
for i in range(500):
    invite_code = ""
    invite_code += random.choice(signs)
    for j in range(3):
        invite_code += random.choice(digits)
        invite_code += random.choice(alphabets)
    invite_code += random.choice(signs)
    connection.execute("INSERT INTO user(invite_code) VALUES(?)"
                       , [generate_password_hash(password = invite_code)])
    connection.commit()
    file.write(str(i+1)+'. '+invite_code+'\n')
    print(invite_code, end=' , ')
    invite_list.add(invite_code)

connection.close()
file.close()
print('\n', len(invite_list))
