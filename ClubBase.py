from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase


class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                
                db.add_user(self.email.text, self.password.text, self.namee.text.capitalize())

                self.reset()

                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""


class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            MainWindow.current = self.email.text
            db.setUser(self.email.text)
            self.reset()
            
            sm.current = "main"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""


class MainWindow(Screen):
    n = ObjectProperty(None)
    current = ""

    def logOut(self):
        sm.current = "login"

    def on_enter(self, *args):
        #print(self.current)
        password, name, created = db.get_user(self.current)
        self.n.text = "Account Name: " + name.capitalize()

    def profilebtn(self):
        ProfilePage.current = self.current
        sm.current = "pro"

    def clubsbtn(self):
        ClubList.current = self.current
        sm.current = "clublist"

    def allclubsbtn(self):
        AllClubs.current = self.current
        sm.current = "allclubs"

class ProfilePage(Screen):
    nameee = ObjectProperty(None)
    createe = ObjectProperty(None)
    bio = ObjectProperty(None)
    current = ""

    def on_enter(self, *args):
        password, name, created = db.get_user(self.current)
        self.nameee.text = "Account Name: " + name.capitalize()
        self.createe.text = "Account Created: " + str(created)
        
        #BRANDON OVER HERE!!!!!!!!!!!! WHEN SOMEONE ENTERS THE PROFILE AUTO DISPLAY THE LAST SAVED BIO
        self.bio.text = db.loadBio()
        #END OF UR STARTING BIO DISPLAY

    def Save(self, *args):
        NewBio = self.bio.text
        db.saveBio(NewBio)
        #BRANDON OVER HERE AS WELL!!!!!!!!!!!!!!!!!!!!! SAVE THIS SHIT IN THE FUCKING DATABASE

    def ChangePass(self):
        ChangePassword.current = self.current
        sm.current = "changepass"
        
    def Back(self):
        sm.current = "main"

class ChangePassword(Screen):
    nameee = ObjectProperty(None)
    oldpass = ObjectProperty(None)
    newpass = ObjectProperty(None)
    confirmpass = ObjectProperty(None)
    current = ""

    def on_enter(self, *args):
        password, name, created = db.get_user(self.current)
        self.nameee.text = "Account Name: " + name.capitalize()

    def Save(self, *args):
        check = self.CheckValid()
        if check:
            db.changePass(self.newpass.text)
        else:
            invalidForm()

    def CheckValid(self):
        password, name, created = db.get_user(self.current)
        if self.oldpass.text == password and self.newpass.text != "" and self.confirmpass.text == self.newpass.text:
            return True
        else:
            return False
        
    def Back(self):
        self.reset()
        sm.current = "pro"

    def reset(self):
        self.oldpass.text = ""
        self.newpass.text = ""
        self.confirmpass.text = ""

class SearchSchool(Screen):
    n = ObjectProperty(None)
    schools = ObjectProperty(None)
    current = ""

    def on_enter(self, *args):
        password, name, created = db.get_user(self.current)
        self.n.text = "Account Name: " + name.capitalize()

    def search(self):
        if self.schools.text.lower() == "aurora high school":
            AvailableClubs.current = self.current
            self.reset()
            sm.current = "availclub"
        else:
            invalidForm()

    def reset(self):
        self.schools.text = ""


class ClubList(Screen):
    clubsearch = ObjectProperty(None)
    current = ""

    def getClubs(self, *args):
        myClubs = []
        for club in range(len(clubMembers)):
            if self in clubMembers[club][1]: #List of clubs, [0] is name, [1] is members list
                myClubs.append(club)
        return myClubs

    def reset(self):
        self.clubsearch.text = ""

    def Back(self):
        self.reset()
        MainWindow.current = self.current
        sm.current = "main"

class AllClubs(Screen):
    clubsearch = ObjectProperty(None)
    current = ""

    def reset(self):
        self.clubsearch.text = ""

    def Back(self):
        self.reset()
        MainWindow.current = self.current
        sm.current = "main"



class WindowManager(ScreenManager):
    pass


def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()
db = DataBase("users.txt")

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"),MainWindow(name="main"), ProfilePage(name = "pro"), ChangePassword(name = "changepass"), ClubList(name = "clublist"), AllClubs(name = "allclubs")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
