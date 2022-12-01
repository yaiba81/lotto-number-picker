from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow, QLabel, QPushButton, QMenuBar, QMenu
from PyQt5.uic import loadUi
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import random
import sys
import time
import re

chrome_options = Options()
chrome_options.add_argument('--headless')
website = "https://www.lottopcso.com/"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
sixfortytwo = []
sixfortytwowin = []
sixfortyfive = []
sixfortyfivewin = []
sixfortynine = []
sixfortyninewin = []
sixfiftyfive = []
sixfiftyfivewin = []
sixfiftyeight = []
sixfiftyeightwin = []

class App(QMainWindow):

    def __init__(self):
        super(App, self). __init__()
        loadUi('assets/ui/main.ui', self)
        self.getLatestWinCombi()
        self.pdpBtn(43, sixfortytwo)
        self.label.mousePressEvent = self.clear
        self.btn642pdp.clicked.connect(lambda: self.testBtn("Hello World"))
        self.btn642sp.clicked.connect(lambda: self.testBtn("Hello World"))
        self.btn645pdp.clicked.connect(lambda: self.testBtn("Hello World"))
        self.btn645sp.clicked.connect(lambda: self.testBtn("Hello World"))
        self.btn649pdp.clicked.connect(lambda: self.testBtn("Hello World"))
        self.btn649sp.clicked.connect(lambda: self.testBtn("Hello World"))
        self.btn655pdp.clicked.connect(lambda: self.testBtn("Hello World"))
        self.btn655sp.clicked.connect(lambda: self.testBtn("Hello World"))
        self.btn658pdp.clicked.connect(lambda: self.testBtn("Hello World"))
        self.btn658sp.clicked.connect(lambda: self.testBtn("Hello World"))

    def pdpBtn(self, num, combi):
        pick = []
        choices = []
        nums = []
        weights = []
        iter = num - 6
        
        for i in range(1, num):
            if i not in combi:
                nums.append(i)

        for i in range(1, iter):
            pass



    def spBtn(self, num, combi):
        pass

    def testBtn(self, word):
        self.label642pdp.setText(word) 
        self.label642sp.setText(word)
        self.label645pdp.setText(word) 
        self.label645sp.setText(word) 
        self.label649pdp.setText(word) 
        self.label649sp.setText(word) 
        self.label655pdp.setText(word) 
        self.label655sp.setText(word) 
        self.label658pdp.setText(word) 
        self.label658sp.setText(word)   

    def clear(self, event):
        self.label642pdp.setText('') 
        self.label642sp.setText('')
        self.label645pdp.setText('') 
        self.label645sp.setText('') 
        self.label649pdp.setText('') 
        self.label649sp.setText('') 
        self.label655pdp.setText('') 
        self.label655sp.setText('') 
        self.label658pdp.setText('') 
        self.label658sp.setText('')   

    def getLatestWinCombi(self):
        driver.get(website)

        six42 = re.split("-", driver.find_element(By.XPATH, 
        '//figure[@class="wp-block-table tablepress is-style-stripes"]/table/tbody/tr[5]/td[2]').text)
        for s in six42:
            if s[0] == '0':
                s = s[1]
                sixfortytwo.append(int(s))
            else:
                sixfortytwo.append(int(s))
        self.label642win.setText('-'.join(map(str,sixfortytwo)))

        six45 = re.split("-", driver.find_element(By.XPATH, 
        '//figure[@class="wp-block-table tablepress is-style-stripes"]/table/tbody/tr[4]/td[2]').text)
        for s in six45:
            if s[0] == '0':
                s = s[1]
                sixfortyfive.append(int(s))
            else:
                sixfortyfive.append(int(s))
        self.label645win.setText('-'.join(map(str,sixfortyfive)))

        six49 = re.split("-", driver.find_element(By.XPATH, 
        '//figure[@class="wp-block-table tablepress is-style-stripes"]/table/tbody/tr[3]/td[2]').text)
        for s in six49:
            if s[0] == '0':
                s = s[1]
                sixfortynine.append(int(s))
            else:
                sixfortynine.append(int(s))
        self.label649win.setText('-'.join(map(str,sixfortynine)))

        six55 = re.split("-", driver.find_element(By.XPATH, 
        '//figure[@class="wp-block-table tablepress is-style-stripes"]/table/tbody/tr[2]/td[2]').text)
        for s in six55:
            if s[0] == '0':
                s = s[1]
                sixfiftyfive.append(int(s))
            else:
                sixfiftyfive.append(int(s))
        self.label655win.setText('-'.join(map(str,sixfiftyfive)))

        six58 = re.split("-", driver.find_element(By.XPATH, 
        '//figure[@class="wp-block-table tablepress is-style-stripes"]/table/tbody/tr[1]/td[2]').text)
        for s in six58:
            if s[0] == '0':
                s = s[1]
                sixfiftyeight.append(int(s))
            else:
                sixfiftyeight.append(int(s))
        self.label658win.setText('-'.join(map(str,sixfiftyeight)))
    
    def quitApp(self):
        QtCore.QCoreApplication.instance().quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(
        'QMenu{color: rgb(47,80,85); font-weight: bold;}QMainWindow{color: #fff; font-weight: bold;}QMenuBar:selected{color: rgb(47,80,85);background-color: rgb(47,80,85) !important;}')
    window = App()
    #window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    window.show()
    sys.exit(app.exec_())