import sqlite3
from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

class database:

    def get_connection(self):
        connection = sqlite3.connect(current_app.config['SQL_DATABASE_URL'])
        connection.row_factory = sqlite3.Row
        return connection

    def check_password(self, ticket_number, user_password):
        connection = self.get_connection()
        user = connection.execute("SELECT password FROM user WHERE user_id = ?",
                                  [ticket_number]).fetchone()
        if user is None:
            return False

        if user['password'] is None:
            return False

        return check_password_hash(user['password'], user_password)

    def check_new_user(self, ticket_number, invite_code):
        """
        :return status as int, user as dict
        status: -1 no such user
                 0 user found but not available
                 1 user found and available
                 2 invalid invite_code
        """
        connection = self.get_connection()
        user = connection.execute("SELECT * FROM user WHERE user_id = ?",
                                  [ticket_number]).fetchone()
        connection.close()

        if user is None:
            print("##" * 10)
            return -2  # user not found

        valid = check_password_hash(user['invite_code'], invite_code)
        print("info\n" + "*" * 10)
        print("valid", valid)
        print("user_id", user['user_id'])
        print("invite_code", invite_code)
        print("password", user['password'])

        if valid:
            if user['password'] is None:
                return 1  # valid invite_code and is available
            else:
                return 0  # valid invite_code but not available

        else:
            return -1  # invalid invite_code

    def add_new_user(self, ticket_number, user_password, user_dateTime):
        """

        return: True --> Insertion was successful
                False --> Insertion failed
        """
        connection = self.get_connection()
        hash_pass = generate_password_hash(user_password)

        user_dateTime = user_dateTime.replace('T', ' ') + ':00'
        user_dateTime = datetime.datetime.strptime(user_dateTime, '%Y-%m-%d %H:%M:%S')
        server_dateTime = datetime.datetime.now()
        diff = (server_dateTime - user_dateTime).total_seconds()

        cursor = connection.cursor()
        cursor.execute("UPDATE user SET password = ?, diff = ? WHERE user_id = ?",
                       (hash_pass, diff, ticket_number))
        connection.commit()
        connection.close()
        return cursor.rowcount == 1  # returns 1 if it was successful

    def add_task(self, task_name, task_desc, task_emoji, task_color, deadline_isactive, task_deadline , task_owner):
        """

        return: True --> Insertion was successful
                False --> Insertion failed
        """
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO task(task_name,task_desc,task_emoji,task_color,deadline_isactive,task_deadline,"
                       "task_owner) VALUES(?,?,?,?,?,?,?)",
                       (task_name, task_desc, task_emoji, task_color, deadline_isactive, task_deadline, task_owner))
        connection.commit()
        connection.close()
        return cursor.rowcount == 1

    def get_all_user_tasks(self, user_id):
        connection = self.get_connection()
        task_list = connection.execute("SELECT * FROM task WHERE task_owner=?",
                           [user_id]).fetchall()
        connection.close()
        return task_list

    def check_author(self, user_id, task_id):
        connection = self.get_connection()
        owner_id = connection.execute("SELECT task_owner FROM task WHERE task_id = ?",
                           [task_id]).fetchone()
        connection.close()
        if owner_id['task_owner'] == user_id:
            return True
        else:
            return False

    def delete_task(self, task_id):
        """

        return: True --> Delete was successful
                False --> Delete failed
        """
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM task WHERE task_id = ?",
                       [task_id])
        connection.commit()
        return cursor.rowcount == 1
