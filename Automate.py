from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import random


class Automation:
    # initializes an instance of automation.  requires username and password.  All else taken care of by settings
    def __init__(self, username=None, password=None, browser=None, url=None, timesleep=30, iterations=250, comments=[]):
        self.username = username
        self.password = password
        self.browser = browser
        self.url = url
        self.iterations = iterations
        self.comments = comments
        #helpers for customization
        self.i = 0 #found in navigation
        self.j = iterations

        self.timesleep = timesleep #Defaults at 30

        self.image_reload_helper = 9


    # launches the browser, connects to login page, waits, sends keys to login
    def login(self):
        try:
            self.browser = webdriver.Chrome()
            self.browser.get("https://www.instagram.com/accounts/login/?source=auth_switcher")

            sleep(5)

            form = self.browser.find_elements_by_class_name("_2hvTZ")
            form[0].send_keys(self.getUsername())
            form[1].send_keys(self.getPassword(), Keys.ENTER)
            sleep(2)
        except:
            self.browser.close()
            self.login()
    # Finds like element, waits for full page load, clicks like, goes to next picture, returns control to caller
    def likePost(self):
        likes = self.browser.find_elements_by_class_name("dCJp8")
        print(len(likes))
        sleep(self.timesleep)
        likes[0].click()
        sleep(.4)
        print("I've completed liking the post task")

        return

    def commentPost(self):

        commentattribute = self.browser.find_elements_by_class_name("dCJp8")
        sleep(.4)
        commentattribute[1].click()
        action = ActionChains(self.browser)
        action.send_keys(self.getComments(), Keys.ENTER)
        action.perform()

        return

    def navigation(self):
        #navigate to the proper hashtag url after logging in.  Move to 10th image open and return control

        self.browser.get(self.getUrl())

        images = self.browser.find_elements_by_class_name("_9AhH0")
        images[self.image_reload_helper].click() #starts at 9 will change if page needs reload due to failure
        sleep(2)
        self.i = 0



    def closeBrowser(self):
        self.browser.close()

    def reloadBrowser(self):
        self.browser.refresh()
        self.image_reload_helper = self.i + 1
        if self.image_reload_helper < 9:
            self.image_reload_helper = 9
        self.navigation()


    # Getters and Setters

    def setUsername(self, userin):
        self.username = input(userin)
        print(self.getUsername())
        return 0

    def getUsername(self):
        return self.username

    def setPassword(self, userin):
        self.password = input(userin)
        print(self.getUsername())
        return 0

    def getPassword(self):
        return self.password

    def getBrowser(self):
        return self.browser

    def setUrl(self, hashtag):
        self.url = "https://www.instagram.com/explore/tags/" + hashtag
        print(self.getUrl())


    def getUrl(self):
        return self.url

    def setIterations(self, iterations):
        self.iterations = iterations
        return 0

    def getIterations(self):

        return self.j

    def setComments(self):
        self.comments = []
        infile = open("comment-pool.txt", "r")
        for line in infile:
            line = line.strip()
            self.comments.append(line)
        return 0

    def getComments(self):
        number = random.randint(0, len(self.comments) - 1)
        return self.comments[number]

    def setBoolComment(self, bool):
        self.boolComment = bool

    def getBoolComment(self):
        return self.boolComment


    def tooString(self):
        return "this is a working instance of " + self.getUsername()

