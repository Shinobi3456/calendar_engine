import datetime
import time
from typing import Tuple, Optional, List

from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config
from exceptions import NoDateCanBeSelected, NotFoundMouthYear


class Calendar:
    """Движок для календаря"""
    _input = None
    _back_button_locators = None
    _next_button_locators = None
    _day_locators = None
    _mouth_locators = None
    _year_locators = None
    _mouth_and_year_locators = None
    _lang = None

    mouth_name = {
        'ru': {
            'январь': 1,
            'февраль': 2,
            'март': 3,
            'апрель': 4,
            'май': 5,
            'июнь': 6,
            'июль': 7,
            'август': 8,
            'сентябрь': 9,
            'октябрь': 10,
            'ноябрь': 11,
            'декабрь': 12
        }
    }

    def __init__(self,
                 input_locators: Tuple[str, str],
                 back_button_locators: Tuple[str, str],
                 next_button_locators: Tuple[str, str],
                 calendar_locators: Tuple[str, str],
                 day_locators: Tuple[str, str],
                 browser: WebDriver,
                 mouth_locators: Optional[Tuple[str, str]] = None,
                 year_locators: Optional[Tuple[str, str]] = None,
                 mouth_and_year_locators: Optional[Tuple[str, str]] = None,
                 lang='ru',
                 delimiter=','
                 ):
        self._input = input_locators
        self._back_button_locators = back_button_locators
        self._next_button_locators = next_button_locators
        self._calendar_locators = calendar_locators
        self._day_locators = day_locators
        self._mouth_locators = mouth_locators
        self._year_locators = year_locators
        self._mouth_and_year_locators = mouth_and_year_locators
        self._lang = lang
        self.browser = browser
        self.delimiter = delimiter

    def get_element_timeout(self, how: str, what: str, timeout: int = 10) -> Optional[WebElement]:
        """Возвращает элемент, или если вышел timeout None.

        :param how: тип селектора (CSS_SELECTOR, XPATH, ID и т.д.)
        :param what: селектор
        :param timeout: время ожидания появления элемента
        :return: объект класс WebElement - который описывает найденный элемент
        """
        try:
            element = WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return None
        return element

    def get_elements_timeout(self, how: str, what: str, timeout=5) -> Optional[List[WebElement]]:
        """Возвращает элементы, или если вышел timeout None.

        :param how: тип селектора (CSS_SELECTOR, XPATH, ID и т.д.)
        :param what: селектор
        :param timeout: время ожидания появления элемента
        :return: объект класс WebElement - который описывает найденный элемент
        """
        try:
            elements = WebDriverWait(self.browser, timeout).until(EC.presence_of_all_elements_located((how, what)))
        except TimeoutException:
            return None
        return elements

    def get_element_clickable_and_timeout(self, how: str, what: str, timeout=10) -> Optional[WebElement]:
        """Ожидает что элемент станет кликабельным в течении timeout.

        :param how: тип селектора (CSS_SELECTOR, XPATH, ID и т.д.)
        :param what: селектор
        :param timeout: время ожидания появления элемента
        :return: объект класс WebElement - который описывает найденный элемент
        """
        try:
            element = WebDriverWait(self.browser, timeout).until(EC.element_to_be_clickable((how, what)))
        except TimeoutException:
            return None
        return element

    def find_cursor(self, mouth: int, year: int) -> Optional[int]:
        """Сравнивает текущий месяц и год с заданными значениями.

        :param mouth: месяц, который нужно выбрать
        :param year: год, который нужно выбрать
        :return:
        """
        if not self._mouth_and_year_locators:
            mouths = self.get_elements_timeout(*self._mouth_locators)
            years = self.get_elements_timeout(*self._year_locators)
            for i in range(0, len(mouths)):
                m = mouths[i].text.lower().replace(',', '')
                mouth_select = self.mouth_name[self._lang][m]
                year_select = int(years[i].text)
                if mouth_select == mouth and year_select == year:
                    return i
        else:
            value = None
            for attempt in range(0, 5):
                value = self.get_element_timeout(*self._mouth_and_year_locators)
                if value:
                    break
                time.sleep(1)

            if not value:
                raise NotFoundMouthYear("Не удалось получить текущий месяц и год. За 5 попыток.")

            mouth_name, year_select = value.text.split(self.delimiter)
            mouth_select = self.mouth_name[self._lang][mouth_name.lower()]
            if mouth_select == mouth and int(year_select) == year:
                return 0
        return None
        # raise NotFoundMouthYear("Не удалось получить текущий месяц и год.")

    def next_click(self):
        """Выполняет нажатие по кнопке Следующий."""
        button = self.get_element_timeout(*self._next_button_locators)
        button.click()

    def back_click(self):
        """Выполняет нажатие по кнопке Предыдущий."""
        button = self.get_element_timeout(*self._back_button_locators)
        button.click()

    def select_date(self, date):
        """Выбирает переданную дату в календаре.

        :param date: дата в формате ДД.MM.ГГГГ
        :return:
        """

        field = self.get_element_clickable_and_timeout(*self._input)
        field.click()

        day, mouth, year = date.split('.')
        cursor_calendar = self.find_cursor(int(mouth), int(year))

        if cursor_calendar is None:
            find = True
            while find:
                if not self._mouth_and_year_locators:
                    mouths = self.get_elements_timeout(*self._mouth_locators)
                    years = self.get_elements_timeout(*self._year_locators)

                    mouth_select = self.mouth_name[self._lang][mouths[0].text.lower().replace(',', '')]
                    year_select = int(years[0].text)
                else:
                    title = self.get_element_timeout(*self._mouth_and_year_locators).text
                    mouth_name, year_select = title.split(self.delimiter)
                    mouth_select = self.mouth_name[self._lang][mouth_name.lower().replace(self.delimiter, '')]
                    year_select = int(year_select)

                if year_select == int(year):
                    if mouth_select > int(mouth):
                        self.back_click()
                    elif mouth_select == int(mouth):
                        cursor_calendar = 0
                        break
                    else:
                        self.next_click()
                elif year_select > int(year):
                    self.back_click()
                else:
                    self.next_click()
                cursor_calendar = self.find_cursor(int(mouth), int(year))
                find = False if cursor_calendar else True
        calendars = self.get_elements_timeout(*self._calendar_locators)
        days = calendars[cursor_calendar].find_elements(*self._day_locators)

        for d in days:
            if d.text.strip():
                if int(d.text) == int(day):
                    d.click()
                    return
        raise NoDateCanBeSelected(f"Не могу выбрать дату {date}")
