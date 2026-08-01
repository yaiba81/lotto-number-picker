from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow, QLabel, QPushButton, QMenuBar, QMenu
from PyQt5.uic import loadUi
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from collections import Counter
from pathlib import Path
import json
import logging
import random
import sys
import re
import urllib.request

BASE_DIR = Path(__file__).resolve().parent
website = "https://www.pcso.gov.ph/"
history_website = "https://lottomatik.pcso.gov.ph/qrmatik"
history_api = "https://numberpicker.lottomatik.com/member/public/lottery/view/lastResult"
history_draw_limit = 30
log_file = BASE_DIR / "probability.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

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
sixfortytwo_history = []
sixfortyfive_history = []
sixfortynine_history = []
sixfiftyfive_history = []
sixfiftyeight_history = []

game_configs = {
    'lotto': {
        'alt': 'LOTTO42',
        'prefix': 'lotto',
        'latest': sixfortytwo,
        'history': sixfortytwo_history,
        'max_number': 42,
    },
    'mega': {
        'alt': 'ML45',
        'prefix': 'mega',
        'latest': sixfortyfive,
        'history': sixfortyfive_history,
        'max_number': 45,
    },
    'super': {
        'alt': 'SL49',
        'prefix': 'super',
        'latest': sixfortynine,
        'history': sixfortynine_history,
        'max_number': 49,
    },
    'grand': {
        'alt': 'GL55',
        'prefix': 'grand',
        'latest': sixfiftyfive,
        'history': sixfiftyfive_history,
        'max_number': 55,
    },
    'ultra': {
        'alt': 'UL58',
        'prefix': 'ultra',
        'latest': sixfiftyeight,
        'history': sixfiftyeight_history,
        'max_number': 58,
    },
}

class ResultsWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal(dict)
    failed = QtCore.pyqtSignal(str)

    def run(self):
        try:
            self.finished.emit(App.fetchLatestWinCombi())
        except (TimeoutException, WebDriverException, ValueError) as error:
            self.failed.emit(str(error))


class App(QMainWindow):

    def __init__(self):
        super(App, self). __init__()
        loadUi(BASE_DIR / 'assets/ui/main.ui', self)

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
        self.results_thread = None
        self.results_worker = None
        self.setPickerEnabled(False)
        self.statusbar.showMessage('Loading latest PCSO results...')
        QtCore.QTimer.singleShot(0, self.getLatestWinCombi)

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
        nums, com = self.getCandidatePools(num, combi)
        history = self.getHistoryForCombi(combi)
        game_name = self.getGameNameForCombi(combi)

        for i in range(6):
            nums1 = self.removeNumPerDigit(nums, [sixfortytwo[i], sixfortyfive[i], sixfortynine[i], sixfiftyfive[i], sixfiftyeight[i]])
            com1 = self.removeNumPerDigit(com, [sixfortytwo[i], sixfortyfive[i], sixfortynine[i], sixfiftyfive[i], sixfiftyeight[i]])
            population = nums1 + com1
            wt = self.genProbabilityWeights(nums1, history, regwt, i) + self.genProbabilityWeights(com1, history, lesswt, i)
            pick = int(random.choices(population, k=1, weights=wt)[0])
            self.logProbability(game_name, 'per digit pick', population, wt, pick, i)
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
        nums, com = self.getCandidatePools(num, combi)
        history = self.getHistoryForCombi(combi)
        game_name = self.getGameNameForCombi(combi)
        
        for i in range(6):
            population = nums + com
            wt = self.genProbabilityWeights(nums, history, regwt) + self.genProbabilityWeights(com, history, lesswt)
            pick = int(random.choices(population, k=1, weights=wt)[0])
            self.logProbability(game_name, 'str8 pick', population, wt, pick, i)
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

    def getCandidatePools(self, num, combi):
        latest_other_game_numbers = list(dict.fromkeys(
            sixfortytwo + sixfortyfive + sixfortynine + sixfiftyfive + sixfiftyeight
        ))
        com = [
            value for value in latest_other_game_numbers
            if value not in combi and value < num
        ]
        nums = [
            value for value in range(1, num)
            if value not in combi and value not in com
        ]
        return nums, com

    def getHistoryForCombi(self, combi):
        for config in game_configs.values():
            if combi is config['latest']:
                return config['history']
        return []

    def getGameNameForCombi(self, combi):
        labels = {
            'lotto': '6/42',
            'mega': '6/45',
            'super': '6/49',
            'grand': '6/55',
            'ultra': '6/58',
        }
        for key, config in game_configs.items():
            if combi is config['latest']:
                return labels[key]
        return 'unknown'

    def genProbabilityWeights(self, candidates, history, base, position=None):
        if not candidates:
            return []

        frequency = Counter()
        position_frequency = Counter()
        for draw in history:
            frequency.update(draw)
            if position is not None and len(draw) > position:
                position_frequency[draw[position]] += 1

        weights = []
        for number in candidates:
            weight = base
            if history:
                weight *= 1 + (frequency[number] / len(history))
                if position is not None:
                    weight *= 1 + (position_frequency[number] / len(history))
            weights.append(weight)
        return weights

    def logProbability(self, game_name, mode, population, weights, pick, position):
        total_weight = sum(weights)
        if total_weight <= 0:
            logger.info('%s %s position %s: no candidates', game_name, mode, position + 1)
            return

        probabilities = [
            (number, weight, (weight / total_weight) * 100)
            for number, weight in zip(population, weights)
        ]
        probability_text = ', '.join(
            f'{number}: weight={weight:.4f}, probability={probability:.2f}%'
            for number, weight, probability in probabilities
        )
        picked_probability = next(
            probability
            for number, _weight, probability in probabilities
            if number == pick
        )
        logger.info(
            '%s %s position %s picked %s (%.2f%%). Candidates: %s',
            game_name,
            mode,
            position + 1,
            pick,
            picked_probability,
            probability_text,
        )

    @staticmethod
    def createDriver():
        firefox_options = Options()
        firefox_options.add_argument('--headless')
        gecko_driver = App.findGeckoDriver()
        if gecko_driver is not None:
            service = FirefoxService(executable_path=str(gecko_driver))
        else:
            service = FirefoxService()

        driver = webdriver.Firefox(service=service, options=firefox_options)
        driver.set_page_load_timeout(45)
        driver.set_script_timeout(45)
        return driver

    @staticmethod
    def findGeckoDriver():
        cached_drivers = sorted(
            (Path.home() / '.cache/selenium/geckodriver/win64').glob('*/geckodriver.exe'),
            reverse=True,
        )
        if cached_drivers:
            return cached_drivers[0]

        bundled_driver = BASE_DIR / 'geckodriver.exe'
        if bundled_driver.exists():
            return bundled_driver

        return None

    @staticmethod
    def readLottoNumbers(driver, prefix):
        numbers = []
        wait = WebDriverWait(driver, 30)

        for index in range(1, 7):
            element_id = f'cphContainer_cphContainer_LottoResults_{prefix}{index}'
            element = wait.until(EC.presence_of_element_located((By.ID, element_id)))
            match = re.search(r'\d+', element.text)
            if not match:
                raise ValueError(f'No number found for {element_id}')
            numbers.append(int(match.group(0)))

        return numbers

    @staticmethod
    def readLottoMatikHistory(driver, game_alt):
        draws = []
        seen = set()
        images = driver.find_elements('xpath', f'//img[@alt="{game_alt}"]')

        for image in images:
            node = image
            numbers = []
            for _ in range(8):
                text = node.text
                numbers = [int(number) for number in re.findall(r'\b\d{1,2}\b', text)]
                if len(numbers) >= 6:
                    numbers = numbers[:6]
                    break
                node = node.find_element('xpath', '..')

            if len(numbers) == 6:
                key = tuple(numbers)
                if key not in seen:
                    draws.append(numbers)
                    seen.add(key)

            if len(draws) >= history_draw_limit:
                break

        return draws

    @staticmethod
    def readLottoMatikApiHistory():
        request = urllib.request.Request(
            history_api,
            headers={'User-Agent': 'Mozilla/5.0'},
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode('utf-8'))

        results = {
            key: []
            for key in game_configs
        }
        lottery_to_key = {
            config['alt']: key
            for key, config in game_configs.items()
        }

        for item in payload.get('result', []):
            key = lottery_to_key.get(item.get('lottery'))
            if key is None or len(results[key]) >= history_draw_limit:
                continue

            numbers = [
                int(number)
                for number in item.get('result', '').split(',')
                if number.strip()
            ]
            if len(numbers) == 6:
                results[key].append(numbers)

        if all(results.values()):
            return results

        raise ValueError('LottoMatik API did not return complete six-number game history')

    def showLatestWinCombiError(self, message):
        for label in [
            self.label642win,
            self.label645win,
            self.label649win,
            self.label655win,
            self.label658win,
        ]:
            label.setText('unavailable')
        self.statusbar.showMessage(message)

    def setPickerEnabled(self, enabled):
        for button in [
            self.btn642pdp,
            self.btn642sp,
            self.btn645pdp,
            self.btn645sp,
            self.btn649pdp,
            self.btn649sp,
            self.btn655pdp,
            self.btn655sp,
            self.btn658pdp,
            self.btn658sp,
        ]:
            button.setEnabled(enabled)

    @staticmethod
    def fetchLatestWinCombi():
        try:
            return App.readLottoMatikApiHistory()
        except (OSError, TimeoutError, ValueError, json.JSONDecodeError):
            pass

        driver = None
        try:
            driver = App.createDriver()
            driver.get(history_website)

            results = {}
            for key, config in game_configs.items():
                history = App.readLottoMatikHistory(driver, config['alt'])
                if history:
                    results[key] = history

            if len(results) == len(game_configs):
                return results

            driver.get(website)
            return {
                key: [App.readLottoNumbers(driver, config['prefix'])]
                for key, config in game_configs.items()
            }
        finally:
            if driver is not None:
                driver.quit()

    def getLatestWinCombi(self):
        if self.results_thread is not None and self.results_thread.isRunning():
            return

        self.setPickerEnabled(False)
        self.statusbar.showMessage('Loading latest PCSO results...')
        self.results_thread = QtCore.QThread(self)
        self.results_worker = ResultsWorker()
        self.results_worker.moveToThread(self.results_thread)
        self.results_thread.started.connect(self.results_worker.run)
        self.results_worker.finished.connect(self.applyLatestWinCombi)
        self.results_worker.failed.connect(self.handleLatestWinCombiError)
        self.results_worker.finished.connect(self.results_thread.quit)
        self.results_worker.failed.connect(self.results_thread.quit)
        self.results_thread.finished.connect(self.results_worker.deleteLater)
        self.results_thread.finished.connect(self.results_thread.deleteLater)
        self.results_thread.finished.connect(self.clearResultsWorker)
        self.results_thread.start()

    def applyLatestWinCombi(self, results):
        games = [
            ('lotto', sixfortytwo, self.label642win),
            ('mega', sixfortyfive, self.label645win),
            ('super', sixfortynine, self.label649win),
            ('grand', sixfiftyfive, self.label655win),
            ('ultra', sixfiftyeight, self.label658win),
        ]

        for key, combi, label in games:
            combi.clear()
            game_configs[key]['history'].clear()
            game_configs[key]['history'].extend(results[key][:history_draw_limit])
            combi.extend(game_configs[key]['history'][0])
            label.setText('-'.join(map(str, combi)))

        self.setPickerEnabled(True)
        draw_count = min(len(config['history']) for config in game_configs.values())
        self.statusbar.showMessage(f'Loaded {draw_count} historical draws per game')

    def handleLatestWinCombiError(self, message):
        self.setPickerEnabled(False)
        self.showLatestWinCombiError(f'Unable to fetch latest results: {message}')

    def clearResultsWorker(self):
        self.results_thread = None
        self.results_worker = None
    
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
