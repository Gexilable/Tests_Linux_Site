import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


@pytest.fixture(scope="module")
def browser():
    options = Options()
    options.add_argument("-headless")
    b = webdriver.Firefox(options=options)
    yield b
    b.close()


class TestLinuxSite:
    @pytest.fixture(autouse=True)
    def _init(self, browser):
        self.browser = browser
        self.link = "https://www.linux.org.ru/"
        self.go_to_main_page()
        self.browser.implicitly_wait(1)

    def go_to_main_page(self):
        self.browser.get(self.link)


class TestHd(TestLinuxSite):
    @pytest.fixture(autouse=True)
    def init(self):
        self.hd = self.browser.find_element(By.ID, "hd")

    def find_logo(self):
        logo_div = self.hd.find_element(By.ID, "sitetitle")
        return logo_div.find_element(By.TAG_NAME, "a")

    def find_menu(self):
        return self.hd.find_element(By.CLASS_NAME, "menu")

    def find_reg_button(self):
        return self.hd.find_element(By.ID, "regmenu")

    def find_log_button(self):
        return self.hd.find_element(By.ID, "loginbutton")

    def test_hd_structure(self):
        logo = self.find_logo()
        menu = self.find_menu()
        assert logo
        assert menu

    def test_logo_text_and_href(self):
        logo = self.find_logo()
        assert logo.text == "LINUX.ORG.RU"
        assert logo.get_attribute("href") == self.link

    def test_menu_structure(self):
        expected_text = {
            "Новости",
            "Галерея",
            "Статьи",
            "Форум",
            "Трекер",
            "Поиск",
        }
        menu = self.find_menu()
        menu_list = menu.find_elements(By.CSS_SELECTOR, "ul > li")
        assert menu_list
        found_text = set(element.text for element in menu_list)
        assert found_text == expected_text

    def test_authorization_menu(self):
        expected_text = {"Регистрация", "Вход"}
        authorization_menus = self.hd.find_elements(
            By.CSS_SELECTOR, "#loginGreating > div > a"
        )
        found_text = set(url.text for url in authorization_menus)
        assert found_text == expected_text


class TestBd(TestLinuxSite):
    @pytest.fixture(autouse=True)
    def init(self):
        self.bd = self.browser.find_element(By.ID, "bd")

    def test_bd_structure(self):
        mainpage = self.find_mainpage()
        assert mainpage

    def test_mainpage_structure(self):
        mainpage = self.find_mainpage()
        news = mainpage.find_element(By.ID, "news")
        aside = mainpage.find_element(By.ID, "boxlets")
        assert news
        assert aside

    def test_news(self):
        news_block = self.bd.find_element(By.ID, "news")
        ad = news_block.find_element(By.ID, "interpage")
        news = news_block.find_elements(By.CLASS_NAME, "news")
        assert ad
        assert len(news) == 5

    def test_more_news_not_empty(self):
        more_news = self.browser.find_elements(By.CSS_SELECTOR, "#news>section ul")
        assert len(more_news) > 0

    def test_bd_buttons(self):
        expected_text = {"Добавить новость", "Все новости", "Неподтвержденные новости"}
        buttons = self.bd.find_elements(By.CSS_SELECTOR, "#news>nav>a")
        found_text = set(b.text for b in buttons)
        assert found_text == expected_text

    def test_additional_urls(self):
        expected_text = {"RSS-подписка на новости", "Канал в Telegram"}
        additional_urls = self.browser.find_elements(By.CSS_SELECTOR, "#news>p")
        found_text = set(u.text for u in additional_urls)
        assert found_text == expected_text

    def test_aside(self):
        aside = self.bd.find_element(By.TAG_NAME, "aside")
        ddos_def_div = aside.find_elements(By.TAG_NAME, "div")[0]
        ddos_def = ddos_def_div.find_element(By.TAG_NAME, "a")
        boxlets = aside.find_elements(By.CLASS_NAME, "boxlet")
        assert len(boxlets) == 5
        assert ddos_def.get_attribute("href") == "http://qrator.net/"

    def test_comments(self):
        news_block = self.bd.find_element(By.ID, "news")
        some_news = news_block.find_elements(By.CLASS_NAME, "news")
        assert some_news
        for n in some_news:
            news_id = (
                n.find_element(By.TAG_NAME, "a").get_attribute("href").split("/")[-1]
            )
            comm_url = (
                n.find_element(By.CLASS_NAME, "nav")
                .find_element(By.TAG_NAME, "a")
                .get_attribute("href")
            )
            assert comm_url.endswith(f"{news_id}#comments")

    def find_mainpage(self):
        mainpage = self.bd.find_element(By.ID, "mainpage")
        return mainpage


class TestFt(TestLinuxSite):
    @pytest.fixture(autouse=True)
    def init(self):
        self.ft = self.browser.find_element(By.ID, "ft")

    def test_ft(self):
        scroll_top_button = self.find_scroll_top_button()
        ft_info = self.ft.find_element(By.ID, "ft-info")
        assert scroll_top_button
        assert ft_info

    def test_ft_info(self):
        ft_info_text = {
            "О Сервере",
            "Правила форума",
            "Разработка и поддержка — Максим Валянский 1998–2023",
            "Сервер для сайта предоставлен «ITTelo»",
            "Размещение сервера и подключение к сети Интернет осуществляется компанией «Selectel».",
        }
        ft_info = self.ft.find_element(By.ID, "ft-info")
        for t in ft_info_text:
            assert t in ft_info.text

    def test_ft_button_scroll_page_on_top(self):
        scroll_top_button = self.find_scroll_top_button()
        self.scroll_down()
        assert self.get_y_offset() > 0
        scroll_top_button.click()
        time.sleep(3)
        assert self.get_y_offset() == 0

    def scroll_down(self):
        self.browser.execute_script("window.scrollBy(0,document.body.scrollHeight)")

    def get_y_offset(self):
        return self.browser.execute_script("return window.pageYOffset")

    def find_scroll_top_button(self):
        return self.ft.find_element(By.ID, "ft-back-button")
