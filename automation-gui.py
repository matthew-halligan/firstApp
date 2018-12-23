from tkinter import *
from Automate import Automation


class AutomateGUI:

    def __init__(self, master):
        frame = Frame(master)
        frame.grid()
        #create instance of Automation


        self.label_username = Label(root, text="Username: ")
        self.label_password = Label(root, text="Password: ")
        self.label_hashtag = Label(root, text="Target hashtag: ")
        self.persistLogin = Checkbutton(root, text="Stay Logged in?")
        self.button_launch = Button(root, text="Launch", command=self.launch)

        #
        self.entry_user = Entry(root)
        self.entry_password = Entry(root)
        self.entry_hashtag = Entry(root)

        self.label_username.grid(row=0, sticky=E)
        self.label_password.grid(row=0, column=2, sticky=E)
        self.persistLogin.grid(row=1, columnspan=3)
        self.label_hashtag.grid(row=2, sticky=E)
        self.button_launch.grid(row=2, column=3)

        self.entry_user.grid(row=0, column=1)
        self.entry_password.grid(row=0, column=3)
        self.entry_hashtag.grid(row=2, column=1)

    def launch(self):
        self.instance = Automation(username=self.entry_user.get(),password=self.entry_password.get())
        #self.instance.setUsername(self.entry_user.get())
        #self.instance.setPassword(self.entry_password.get())
        self.instance.setUrl(self.entry_hashtag.get())
        self.instance.login()
        try:
            self.instance.navigation()
        except:
            print("Chrome Was Unreachable.  Window must have closed early.  Launch again.")




root = Tk(className=" Automate Instagram")

automate = AutomateGUI(root)



root.mainloop()

