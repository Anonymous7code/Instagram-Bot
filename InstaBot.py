import os
import time
from selenium import webdriver
import configparser


class InstagramBot:

    def __init__(self, username, password):
        """
        Initialize instance of class InstagramBot

        Auth. user by login method and provided username and password
        Args:
            :param username: str: The instagram username for user
            :param password: str: The instagram username for user

        Attributes:
            driver: selenium.webdriver.Chrome()
        """

        self.username = username
        self.password = password
        self.base_url = 'https://www.instagram.com'
        self.driver = webdriver.Chrome('./chromedriver.exe')

        self.login()

    def login(self):
        self.driver.get('{}/accounts/login/'.format(self.base_url))
        self.driver.maximize_window()
        self.driver.find_element_by_name("username").send_keys(self.username)
        self.driver.find_element_by_name("password").send_keys(self.username)
        self.driver.find_element_by_xpath(
            '//*[@id="loginForm"]/div/div[3]/button/div').click()

    def nav_user(self, user):
        self.driver.get('{}/{}/'.format(self.base_url, user))

    def follow(self, user):
        self.nav_user(user)
        follow_button = self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/header/section/div[1]/div/a/button').click()

    def search_tag(self, tag):
        self.driver.get(self.get_tag_url.format(tag))

    def unfollow_user(self, user):
        self.nav_user(user)
        unfollow_btns = self.find_buttons('Following')

        if unfollow_btns:
            for btn in unfollow_btns:
                btn.click()
                unfollow_confirmation = self.find_buttons('Unfollow')[0]
                unfollow_confirmation.click()
        else:
            print('No {} buttons were found.'.format('Following'))

    def download_user_images(self, user):
        self.nav_user(user)

        img_srcs = []
        finished = False
        while not finished:

            finished = self.infinite_scroll()  # scroll down

            img_srcs.extend([img.get_attribute(
                'src') for img in self.driver.find_elements_by_class_name('FFVAD')])  # scrape srcs

        img_srcs = list(set(img_srcs))  # clean up duplicates

        for idx, src in enumerate(img_srcs):
            self.download_image(src, idx, user)

    def like_latest_posts(self, user, n_posts, like=True):
        action = 'Like' if like else 'Unlike'

        self.nav_user(user)

        imgs = []
        imgs.extend(self.driver.find_elements_by_class_name('_9AhH0'))

        for img in imgs[:n_posts]:
            img.click()
            time.sleep(1)
            try:
                self.driver.find_element_by_xpath(
                    "//*[@aria-label='{}']".format(action)).click()
            except Exception as e:
                print(e)

            #self.comment_post('beep boop testing bot')
            self.driver.find_elements_by_class_name('ckWGn')[0].click()

    def download_image(self, src, image_filename, folder):
        """
        Creates a folder named after a user to to store the image, then downloads the image to the folder.
        """

        folder_path = './{}'.format(folder)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        img_filename = 'image_{}.jpg'.format(image_filename)
        urllib.request.urlretrieve(src, '{}/{}'.format(folder, img_filename))

    def infinite_scroll(self):
        """
        Scrolls to the bottom of a users page to load all of their media
        Returns:
            bool: True if the bottom of the page has been reached, else false
        """

        SCROLL_PAUSE_TIME = 1

        self.last_height = self.driver.execute_script(
            "return document.body.scrollHeight")

        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(SCROLL_PAUSE_TIME)

        self.new_height = self.driver.execute_script(
            "return document.body.scrollHeight")

        if self.new_height == self.last_height:
            return True

        self.last_height = self.new_height
        return False


if __name__ == '__main__':
    config_path = './config.ini'
    cparser = configparser.ConfigParser()
    cparser.read(config_path)
    username = cparser['AUTH']["USERNAME"]
    password = cparser["AUTH"]["PASSWORD"]

    ig_bot = InstagramBot(username, password)

    ig_bot.follow('s_a_j_a_l_18')
