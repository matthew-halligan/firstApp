from tkinter import *
from Automate import Automation
from threading import Thread
from PyQt5.QtCore import *
from time import sleep

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

def popupmsg_error(msg):
    popup = Tk()

    def leavemini():
        popup.destroy()

    popup.wm_title("ERROR!")
    label = Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady= 10)
    B1 = Button(popup, text="Okay", command=leavemini)
    B1.pack()
    popup.mainloop()


class AutomateGUI(QObject):

    def __init__(self, master, parent=None):
        super(AutomateGUI, self).__init__(parent)
        frame = Frame(master)
        frame.grid()
        self.defaultsleep = IntVar(value=30, name="30")
        self.defaultIterations = IntVar(value=250, name="250")
        #
        self.entry_user = Entry(root)
        self.entry_password = Entry(root)
        self.entry_hashtag = Entry(root)
        self.entry_timesleep = Entry(root)
        self.entry_timesleep.insert(END, self.defaultsleep)
        self.entry_iterations = Entry(root)
        self.entry_iterations.insert(END, self.defaultIterations)

        self.label_username = Label(root, text="Username: ")
        self.label_password = Label(root, text="Password: ")
        self.label_hashtag = Label(root, text="Target hashtag: ")
        self.label_timesleep = Label(root, text="| Time Between Likes:")
        self.label_iterations = Label(root, text="Iterations:")
        self.persistLogin = Checkbutton(root, text="Stay Logged in?*")
        self.button_launch = Button(root, text="Launch", command=self.processLaunch)



        self.label_username.grid(row=0, sticky=E)
        self.label_password.grid(row=0, column=2, sticky=E)
        self.persistLogin.grid(row=1, columnspan=3)
        self.label_timesleep.grid(row=1, column=2, sticky=E)
        self.label_iterations.grid(row=2, column=2, sticky=E)
        self.label_hashtag.grid(row=3, sticky=E)
        self.button_launch.grid(row=3, column=3)

        self.entry_user.grid(row=0, column=1)
        self.entry_password.grid(row=0, column=3)
        self.entry_hashtag.grid(row=3, column=1)
        self.entry_timesleep.grid(row=1, column=3)
        self.entry_iterations.grid(row=2,column=3)


    def processLaunch(self):
        # Initialize worker thread
        self.WorkerThread = WorkerThread(username=self.entry_user.get(), password=self.entry_password.get(), hashtag=self.entry_hashtag.get(), timesleep=int(str(self.entry_timesleep.get())), iterations=int(str(self.entry_iterations.get())))
        self.WorkerThread.start()


class WorkerThread(Thread):

    def __init__(self, username, password, hashtag, timesleep, iterations, parent=None):
        super(WorkerThread, self).__init__(parent)

        self.instance = Automation(username=username, password=password, timesleep=timesleep, iterations=iterations)
        self.hashtag = hashtag
        self.i = 0

    def run(self):

        self.instance.setUrl(self.hashtag)

        def loginInstace(instance):
            try:
                instance.login()
            except:
                instance.reloadBrowser()
                sleep(3)
                loginInstace(instance)

        def navigateInstance(instance):
            try:
                instance.navigation()
            except:
                msg = "Chrome Was Unreachable and will be reloaded.  If persistant restart application and report bug to Matt"
                popupmsg_error(msg)
                sleep(3)
                navigateInstance(instance)

        def likePostInstance(instance):
            try:
                instance.likePost()
            except:
                instance_next = instance.browser.find_element_by_class_name("coreSpriteRightPaginationArrow")
                instance_next.click()
                likePostInstance(instance)

        # this is where the action starts

        loginInstace(self.instance)
        navigateInstance(self.instance)
        while self.i < self.instance.getIterations():
            sleep(2)
            likePostInstance(self.instance)

            instance_next = self.instance.browser.find_element_by_class_name("coreSpriteRightPaginationArrow")
            instance_next.click()
            self.i += 1
            print("I am on number", format(self.i, "d"), ". That's", format(self.i / self.instance.getIterations() * 100, "0.2f"), "% complete.")
        self.instance.closeBrowser()



root = Tk(className=" Automate Instagram v0_1")

automate = AutomateGUI(root)



root.mainloop()