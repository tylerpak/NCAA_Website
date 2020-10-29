import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

class seleniumTest(unittest.TestCase):

    #Tests navigation to about page and back to home page
    def test_about(self):  
        driver = webdriver.Firefox(executable_path=r"./geckodriver")
        # edit the next line to enter the location of "min.html" on your system
        driver.get(r"http://127.0.0.1:5000/")

        elem = driver.find_element_by_id('aboutButton')
        elem.click() #click the button

        result = driver.title

        self.assertEqual('About - College Basketball Internet Database', result)

        elem = driver.find_element_by_id('homeButton')
        elem.click() #click the button

        result = driver.title

        self.assertEqual('College Basketball Internet Database', result)

        driver.close() # close the browser window

    def test_playerModel(self):  
        driver = webdriver.Firefox(executable_path=r"./geckodriver")
        # edit the next line to enter the location of "min.html" on your system
        driver.get(r"http://127.0.0.1:5000/")

        elem = driver.find_element_by_id('playerButton')
        elem.click() #click the button

        result = driver.title

        self.assertEqual('Players - College Basketball Internet Database', result)

        driver.close() # close the browser window

    def test_teamModel(self):  
        driver = webdriver.Firefox(executable_path=r"./geckodriver")
        # edit the next line to enter the location of "min.html" on your system
        driver.get(r"http://127.0.0.1:5000/")

        elem = driver.find_element_by_id('teamButton')
        elem.click() #click the button

        result = driver.title

        self.assertEqual('Teams - College Basketball Internet Database', result)

        driver.close() # close the browser window

    def test_gameModel(self):  
        driver = webdriver.Firefox(executable_path=r"./geckodriver")
        # edit the next line to enter the location of "min.html" on your system
        driver.get(r"http://127.0.0.1:5000/")

        elem = driver.find_element_by_id('gameButton')
        elem.click() #click the button

        result = driver.title

        self.assertEqual('Games - College Basketball Internet Database', result)

        driver.close() # close the browser window
    
    def test_gameInstances(self):  
        driver = webdriver.Firefox(executable_path=r"./geckodriver")
        # edit the next line to enter the location of "min.html" on your system
        driver.get(r"http://127.0.0.1:5000/games1")

        elems = driver.find_elements_by_id('reference')
        i=0
        while i < len(elems):
            elems = driver.find_elements_by_id('reference')
            elem = elems[i]
            elem.click()

            team = driver.find_element_by_id('home')
            team.click()
            result = driver.title
            self.assertEqual('Internet Database',result[-17:])
            driver.back()

            team = driver.find_element_by_id('away')
            team.click()
            result = driver.title
            self.assertEqual('Internet Database',result[-17:])
            driver.back()

            players = driver.find_elements_by_id('player')
            j=0
            while j < len(players):
                players = driver.find_elements_by_id('player')
                player = players[j]
                player.click()
                result = driver.title
                self.assertEqual('Internet Database',result[-17:])
                driver.back()
                j = j+1
            driver.back()
            i = i+1

        driver.close() # close the browser window

    def test_playerInstances(self):  
        driver = webdriver.Firefox(executable_path=r"./geckodriver")
        # edit the next line to enter the location of "min.html" on your system
        driver.get(r"http://127.0.0.1:5000/players1")

        elems = driver.find_elements_by_id('reference')
        i=0
        while i < len(elems):
            elems = driver.find_elements_by_id('reference')
            elem = elems[i]
            elem.click()

            team = driver.find_element_by_id('team')
            team.click()
            result = driver.title
            self.assertEqual('Internet Database',result[-17:])
            driver.back()

            games = driver.find_elements_by_id('game')
            j=0
            while j < len(games):
                games = driver.find_elements_by_id('game')
                game = games[j]
                game.click()
                result = driver.title
                self.assertEqual('Internet Database',result[-17:])
                driver.back()
                j = j+1

            driver.back()
            i = i+1

        driver.close() # close the browser window


    def test_teamInstances(self):  
        driver = webdriver.Firefox(executable_path=r"./geckodriver")
        # edit the next line to enter the location of "min.html" on your system
        driver.get(r"http://127.0.0.1:5000/teams1")

        elems = driver.find_elements_by_id('reference')
        i=0
        while i < len(elems):
            elems = driver.find_elements_by_id('reference')
            elem = elems[i]
            elem.click()

            players = driver.find_elements_by_id('player')
            j=0
            while j < len(players):
                players = driver.find_elements_by_id('player')
                player = players[j]
                player.click()
                result = driver.title
                self.assertEqual('Internet Database',result[-17:])
                driver.back()
                j = j+1

            games = driver.find_elements_by_id('game')
            j=0
            while j < len(games):
                games = driver.find_elements_by_id('game')
                game = games[j]
                game.click()
                result = driver.title
                self.assertEqual('Internet Database',result[-17:])
                driver.back()
                j = j+1


            driver.back()
            i = i+1

        driver.close() # close the browser window
    

if __name__ == '__main__':
    unittest.main()
