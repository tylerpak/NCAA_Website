import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class seleniumTest(unittest.TestCase):

    #Tests navigation to about page and back to home page
    def test_about(self):  
        driver = webdriver.Firefox(executable_path=r"/home/jburrus/Documents/geckodriver")
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

    def test_carousel(self):  
        driver = webdriver.Firefox(executable_path=r"/home/jburrus/Documents/geckodriver")
        # edit the next line to enter the location of "min.html" on your system
        driver.get(r"http://127.0.0.1:5000/")


        elem = driver.find_element_by_id('player-car-activate')
        elem.click() #click the button
        elem = driver.find_element_by_id('player-car')
        elem.click() #click the button

        result = driver.title

        self.assertEqual('Players - College Basketball Internet Database', result)

        elem = driver.find_element_by_id('homeButton')
        elem.click() #click the button


        elem = driver.find_element_by_id('team-car-activate')
        elem.click() #click the button
        elem = driver.find_element_by_id('team-car')
        elem.click() #click the button

        result = driver.title

        self.assertEqual('Teams - College Basketball Internet Database', result)

        elem = driver.find_element_by_id('homeButton')
        elem.click() #click the button


        elem = driver.find_element_by_id('game-car-activate')
        elem.click() #click the button
        elem = driver.find_element_by_id('game-car')
        elem.click() #click the button

        result = driver.title

        self.assertEqual('Games - College Basketball Internet Database', result)

        driver.close() # close the browser window

    def test_playerModel(self):  
        driver = webdriver.Firefox(executable_path=r"/home/jburrus/Documents/geckodriver")
        # edit the next line to enter the location of "min.html" on your system
        driver.get(r"http://127.0.0.1:5000/")

        elem = driver.find_element_by_id('playerButton')
        elem.click() #click the button

        result = driver.title

        self.assertEqual('Players - College Basketball Internet Database', result)

        driver.close() # close the browser window

    def test_teamModel(self):  
        driver = webdriver.Firefox(executable_path=r"/home/jburrus/Documents/geckodriver")
        # edit the next line to enter the location of "min.html" on your system
        driver.get(r"http://127.0.0.1:5000/")

        elem = driver.find_element_by_id('teamButton')
        elem.click() #click the button

        result = driver.title

        self.assertEqual('Teams - College Basketball Internet Database', result)

        driver.close() # close the browser window

    def test_gameModel(self):  
        driver = webdriver.Firefox(executable_path=r"/home/jburrus/Documents/geckodriver")
        # edit the next line to enter the location of "min.html" on your system
        driver.get(r"http://127.0.0.1:5000/")

        elem = driver.find_element_by_id('gameButton')
        elem.click() #click the button

        result = driver.title

        self.assertEqual('Games - College Basketball Internet Database', result)

        driver.close() # close the browser window

if __name__ == '__main__':
    unittest.main()
