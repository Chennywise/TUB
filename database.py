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

            return results[0]
        else:
            return -1

    def add_user(self, email, password, name):
        if self.get_user(email) == -1:
            command = "INSERT INTO users (username, password, email, creation_date) VALUES(%s, %s, %s, %s)"
            values = (name.strip(), password.strip(), email.strip(), DataBase.get_date())
            self.mydb.commit()
            self.mycursor.execute(command, values)
            return 1


        else:

            return -1
    def add_club(self, name, school, description, status):
        command = "INSERT INTO club_list (club_name, club_school, descr, stat, creation_date) VALUES(%s, %s, %s, %s, %s)"
        val = (name.strip(), school.strip().lower(), description.strip(), status, DataBase.get_date())
        self.mycursor.execute(command, val)
        self.mycursor.execute("SELECT LAST_INSERT_ID()")
        id = self.mycursor.fetchone()[0]

        self.joinClub(id, admin = True)
        self.mydb.commit()

    def validate(self, email, password):
        if self.get_user(email) != -1:
            self.mycursor.execute("SELECT password FROM users WHERE email = %s", (email,))
            return self.mycursor.fetchone()[0] == password
        else:
            return False
    def setUser(self, email):
        command = "SELECT user_id FROM users WHERE email = \'" + email + "\'"

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
    def searchClubs(self, school, keyword):
        command = "SELECT club_name, club_school, club_id FROM club_list WHERE club_school LIKE \'%"+school+"%\' AND club_name LIKE \'%"+keyword+"%\' ORDER BY club_name"
        self.mycursor.execute(command)
        return self.mycursor.fetchall()
    def searchMyClubs(self, school, keyword):
        command = "SELECT c.club_name, c.club_school, c.club_id FROM club_list c RIGHT JOIN club_members m ON c.club_id = m.club_id WHERE c.club_school LIKE \'%"+school+"%\' AND c.club_name LIKE \'%"+keyword+"%\' AND m.user_id = "+str(self.user_id)+" ORDER BY c.club_name"
        self.mycursor.execute(command)
        return self.mycursor.fetchall()
    def joinClub(self, club_id, admin = False):
        command = "INSERT INTO club_members (club_id, user_id, role, `rank`, admin_stat) VALUES(%s, %s, %s, %s, %s)"
        val = (club_id, self.user_id, "member", 0, admin)
        self.mycursor.execute(command, val)
        self.mydb.commit()
    def applyClub(self, club_id):
        command = "INSERT INTO club_applications (club_id, user_id, application_date) VALUES(%s, %s, %s)"
        val = (club_id, self.user_id, DataBase.get_date())
        self.mycursor.execute(command, val)
        self.mydb.commit()

    def getClubPage(self, club_id):
        command = "SELECT club_name, club_school, descr, creation_date, stat FROM club_list WHERE club_id = " + str(club_id)
        self.mycursor.execute(command)
        return self.mycursor.fetchone()
    def isInClub(self, club_id):
        command = "SELECT admin_stat FROM club_members WHERE user_id = {} AND club_id = {}".format(self.user_id, club_id)
        self.mycursor.execute(command)
        result = self.mycursor.fetchall()
        if len(result) != 0:
            if result[0][0] == 1:
                return "admin"
            else:
                return "in"
        else:
            command = "SELECT application_id FROM club_applications WHERE user_id = {} AND club_id = {}".format(self.user_id, club_id)
            self.mycursor.execute(command)
            if len(self.mycursor.fetchall()) != 0:
                return "pending"
            else:
                return "not in"
            

    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]
