import datetime
import time
from typing import Tuple, Optional, List

from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config
from exceptions import NoDateCanBeSelected, NotFoundCalendar


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

    def get_current_position(self, mouth_element: Optional[WebElement], year_element: Optional[WebElement],
                             mouth_and_year: Optional[WebElement] = None) -> Tuple[int, int]:
        """Возвращает текущий выбранный месяц и год."""

        if mouth_and_year:
            mouth_name, year_select = mouth_and_year.text.split(self.delimiter)
            mouth_select = self.mouth_name[self._lang][mouth_name.lower()]
            return mouth_select, int(year_select)

        m = mouth_element.text.lower().replace(',', '')
        mouth_select = self.mouth_name[self._lang][m]
        year_select = int(year_element.text)
        return mouth_select, year_select

    def find_cursor(self, mouth: int, year: int) -> Optional[int]:
        """Сравнивает текущий месяц и год с заданными значениями.

        :param mouth: месяц, который нужно выбрать
        :param year: год, который нужно выбрать
        :return:
        """

        if self._mouth_and_year_locators:
            mouth_and_year = self.get_element_timeout(*self._mouth_and_year_locators)
            mouth_select, year_select = self.get_current_position(mouth_element=None, year_element=None,
                                                                  mouth_and_year=mouth_and_year)
            if mouth_select == mouth and int(year_select) == year:
                return True
        else:
            mouth = self.get_element_timeout(*self._mouth_locators)
            year = self.get_element_timeout(*self._year_locators)
            mouth_select, year_select = self.get_current_position(mouth_element=mouth, year_element=year)
            if mouth_select == mouth and year_select == year:
                return True

        return False

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
        calendar_element = self.get_element_timeout(*self._calendar_locators)
        if calendar_element:
            find = self.find_cursor(int(mouth), int(year))
            while not find:
                # Определение текущего положения
                if self._mouth_and_year_locators:
                    mouth_and_year = self.get_element_timeout(*self._mouth_and_year_locators)
                    mouth_select, year_select = self.get_current_position(mouth_element=None,
                                                                          year_element=None,
                                                                          mouth_and_year=mouth_and_year)
                else:
                    mouth_element = self.get_element_timeout(*self._mouth_locators)
                    year_element = self.get_element_timeout(*self._year_locators)
                    mouth_select, year_select = self.get_current_position(mouth_element=mouth_element,
                                                                          year_element=year_element)

                if year_select == int(year):
                    if mouth_select > int(mouth):
                        self.back_click()
                    elif mouth_select == int(mouth):
                        break
                    else:
                        self.next_click()
                elif year_select > int(year):
                    self.back_click()
                else:
                    self.next_click()

                find = self.find_cursor(int(mouth), int(year))

            days = self.browser.find_elements(*self._day_locators)
            for d in days:
                if d.text.strip():
                    if int(d.text) == int(day):
                        d.click()
                        return
            raise NoDateCanBeSelected(f"Не могу выбрать дату {date}")
        raise NotFoundCalendar(f"Не удалось обнаружить календарь. Проверьте локаторы или увеличьте таймаут.")
