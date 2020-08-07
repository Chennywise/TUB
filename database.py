import datetime
import mysql.connector



class DataBase:
    def __init__(self, filename):


        self.mydb = mysql.connector.connect(
          host="99.254.154.29",
          user="bread",
          password="bread123",
          database="sql_clubs",
          port=25910
        )

        self.mycursor = self.mydb.cursor()
        self.user_id = 0


    def get_user(self, email):
        command = "SELECT password, username, creation_date FROM users WHERE email = \'" + email + "\'"
        self.mycursor.execute(command)
        results = self.mycursor.fetchall()
        if len(results) != 0:
            print(results[0])
            return results[0]
        else:
            return -1

    def add_user(self, email, password, name):
        if self.get_user(email) == -1:
            command = "INSERT INTO users (username, password, email, creation_date) VALUES(%s, %s, %s, %s)"
            values = (name.strip(), password.strip(), email.strip(), DataBase.get_date())
            self.mycursor.execute(command, values)
            self.mydb.commit()
            return 1

        else:
            print("Email exists already")
            return -1

    def validate(self, email, password):
        if self.get_user(email) != -1:
            self.mycursor.execute("SELECT password FROM users WHERE email = %s", (email,))
            return self.mycursor.fetchone()[0] == password
        else:
            return False
    def setUser(self, email):
        command = "SELECT user_id FROM users WHERE email = \'" + email + "\'"
        print(command)
        self.mycursor.execute(command)
        self.user_id = self.mycursor.fetchone()[0]
    def saveBio(self, bio):
        command = "UPDATE users SET bio = \'"+bio+"\' WHERE user_id = "+str(self.user_id)
        self.mycursor.execute(command)
        self.mydb.commit()
    def loadBio(self):
        command = "SELECT bio from users WHERE user_id = "+str(self.user_id)
        self.mycursor.execute(command)
        bio = self.mycursor.fetchone()[0]
        if bio:
            return bio
        else:
            return ""
    def changePass(self, newPassword):
        command = "UPDATE users SET password = \'"+newPassword+"\' WHERE user_id = "+str(self.user_id)
        self.mycursor.execute(command)
        self.mydb.commit()

    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]


