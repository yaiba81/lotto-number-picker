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
import re

chrome_options = Options()
chrome_options.add_argument('--headless')
website = "https://www.lottopcso.com/"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
regwt = 9
lesswt = 1
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
        
        self.label.mousePressEvent = self.clear
        self.btn642pdp.clicked.connect(lambda: self.pdpBtn(43, sixfortytwo))
        self.btn642sp.clicked.connect(lambda: self.spBtn(43, sixfortytwo))
        self.btn645pdp.clicked.connect(lambda: self.pdpBtn(46, sixfortyfive))
        self.btn645sp.clicked.connect(lambda: self.spBtn(46, sixfortyfive))
        self.btn649pdp.clicked.connect(lambda: self.pdpBtn(50, sixfortynine))
        self.btn649sp.clicked.connect(lambda: self.spBtn(50, sixfortynine))
        self.btn655pdp.clicked.connect(lambda: self.pdpBtn(56, sixfiftyfive))
        self.btn655sp.clicked.connect(lambda: self.spBtn(56, sixfiftyfive))
        self.btn658pdp.clicked.connect(lambda: self.pdpBtn(59, sixfiftyeight))
        self.btn658sp.clicked.connect(lambda: self.spBtn(59, sixfiftyeight))

    def genWeight(self, combi, base):
        count = len(combi)
        weights = []
        weight = base / count
        for i in range(count):
            weights.append(weight)
        return weights
    
    def getNewCombi(self, combi, num):
        for i in combi:
            if num == i:
                combi.remove(i)
        return combi

    def removeNumPerDigit(self, combi, nums):
        for i in combi:
            if i in nums:
                combi.remove(i)
        return combi

    # button for predict per digit
    def pdpBtn(self, num, combi):
        randomPick = []
        nums = []
        com = list(dict.fromkeys(sixfortytwo + sixfortyfive + sixfortynine + sixfiftyfive + sixfiftyeight))

        for i in com:
            if i in combi:
                com.remove(i)

        for i in range(1, num):
            if i not in combi:
                nums.append(i)

        for i in nums:
            if i in com:
                nums.remove(i)

        for i in range(6):
            nums1 = self.removeNumPerDigit(nums, [sixfortytwo[i], sixfortyfive[i], sixfortynine[i], sixfiftyfive[i], sixfiftyeight[i]])
            com1 = self.removeNumPerDigit(com, [sixfortytwo[i], sixfortyfive[i], sixfortynine[i], sixfiftyfive[i], sixfiftyeight[i]])
            wt = self.genWeight(nums1, regwt) + self.genWeight(com1, lesswt)
            pick = int(random.choices(nums1 + com1, k=1, weights=wt)[0])
            randomPick.append(pick)
            nums = self.getNewCombi(nums, pick)
            com = self.getNewCombi(com, pick)

        if num == 43:
            self.label642pdp.setText(str(randomPick).replace("[", "").replace("]", ""))
        if num == 46:
            self.label645pdp.setText(str(randomPick).replace("[", "").replace("]", ""))
        if num == 50:
            self.label649pdp.setText(str(randomPick).replace("[", "").replace("]", ""))
        if num == 56:
            self.label655pdp.setText(str(randomPick).replace("[", "").replace("]", ""))
        if num == 59:
            self.label658pdp.setText(str(randomPick).replace("[", "").replace("]", ""))

    def spBtn(self, num, combi):
        randomPick = []
        nums = []
        com = list(dict.fromkeys(sixfortytwo + sixfortyfive + sixfortynine + sixfiftyfive + sixfiftyeight))

        for i in com:
            if i in combi:
                com.remove(i)

        for i in range(1, num):
            if i not in combi:
                nums.append(i)

        for i in nums:
            if i in com:
                nums.remove(i)

        for i in range(6):
            wt = self.genWeight(nums, regwt) + self.genWeight(com, lesswt)
            pick = int(random.choices(nums + com, k=1, weights=wt)[0])
            randomPick.append(pick)
            nums = self.getNewCombi(nums, pick)
            com = self.getNewCombi(com, pick)

        if num == 43:
            self.label642sp.setText(str(randomPick).replace("[", "").replace("]", ""))
        if num == 46:
            self.label645sp.setText(str(randomPick).replace("[", "").replace("]", ""))
        if num == 50:
            self.label649sp.setText(str(randomPick).replace("[", "").replace("]", ""))
        if num == 56:
            self.label655sp.setText(str(randomPick).replace("[", "").replace("]", ""))
        if num == 59:
            self.label658sp.setText(str(randomPick).replace("[", "").replace("]", ""))

    def testBtn(self, word):
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