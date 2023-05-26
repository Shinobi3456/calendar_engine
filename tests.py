import unittest
import datetime

from selenium import webdriver

import config
from engine import Calendar
import locators


class TestCalendar(unittest.TestCase):
    driver = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        cls.driver.get(config.BASE_URL)

    def test_calendar_page_loads(self):
        self.assertEqual(self.driver.title, "Test Calendar (DatePicker)")

    def test_calendar_prev_month(self):
        """Тест выбора дня в предыдущем месяце."""
        prev_month = datetime.datetime.now() - datetime.timedelta(days=42)
        obj = Calendar(
            input_locators=locators.input_datepicker1,
            back_button_locators=locators.back_button_locators,
            next_button_locators=locators.next_button_locators,
            calendar_locators=locators.calendar,
            day_locators=locators.day_locators,
            browser=self.driver,
            mouth_and_year_locators=locators.mouth_and_year_locators,
            delimiter=' ',
        )

        obj.select_date(prev_month.strftime('%d.%m.%Y'))
        input_value = self.driver.find_element(*locators.input_value)
        assert input_value.get_attribute('value') == prev_month.strftime('%d.%m.%Y'), "Не выбрана дата."

        obj = Calendar(
            input_locators=locators.input_datepicker2,
            back_button_locators=locators.back_button_locators2,
            next_button_locators=locators.next_button_locators2,
            calendar_locators=locators.calendar2,
            day_locators=locators.day_locators2,
            browser=self.driver,
            mouth_locators=locators.mouth_locators,
            year_locators=locators.year_locators
        )

        obj.select_date(prev_month.strftime('%d.%m.%Y'))
        input_value = self.driver.find_element(*locators.input_datepicker2)
        assert input_value.get_attribute('value') == prev_month.strftime('%d.%m.%Y'), "Не выбрана дата."

    def test_calendar_current_month(self):
        """Тест выбора дня в текущем месяце."""
        current_month = datetime.datetime.now().replace(day=11)
        obj = Calendar(
            input_locators=locators.input_datepicker1,
            back_button_locators=locators.back_button_locators,
            next_button_locators=locators.next_button_locators,
            calendar_locators=locators.calendar,
            day_locators=locators.day_locators,
            browser=self.driver,
            mouth_and_year_locators=locators.mouth_and_year_locators,
            delimiter=' ',
        )

        obj.select_date(current_month.strftime('%d.%m.%Y'))
        input_value = self.driver.find_element(*locators.input_value)
        assert input_value.get_attribute('value') == current_month.strftime('%d.%m.%Y'), "Не выбрана дата."

        obj = Calendar(
            input_locators=locators.input_datepicker2,
            back_button_locators=locators.back_button_locators2,
            next_button_locators=locators.next_button_locators2,
            calendar_locators=locators.calendar2,
            day_locators=locators.day_locators2,
            browser=self.driver,
            mouth_locators=locators.mouth_locators,
            year_locators=locators.year_locators
        )

        obj.select_date(current_month.strftime('%d.%m.%Y'))
        input_value = self.driver.find_element(*locators.input_datepicker2)
        assert input_value.get_attribute('value') == current_month.strftime('%d.%m.%Y'), "Не выбрана дата."

    def test_calendar_next_month(self):
        """Тест выбора дня в следующем месяце."""
        next_month = datetime.datetime.now() + datetime.timedelta(days=42)
        obj = Calendar(
            input_locators=locators.input_datepicker1,
            back_button_locators=locators.back_button_locators,
            next_button_locators=locators.next_button_locators,
            calendar_locators=locators.calendar,
            day_locators=locators.day_locators,
            browser=self.driver,
            mouth_and_year_locators=locators.mouth_and_year_locators,
            delimiter=' ',
        )

        obj.select_date(next_month.strftime('%d.%m.%Y'))
        input_value = self.driver.find_element(*locators.input_value)
        assert input_value.get_attribute('value') == next_month.strftime('%d.%m.%Y'), "Не выбрана дата."

        obj = Calendar(
            input_locators=locators.input_datepicker2,
            back_button_locators=locators.back_button_locators2,
            next_button_locators=locators.next_button_locators2,
            calendar_locators=locators.calendar2,
            day_locators=locators.day_locators2,
            browser=self.driver,
            mouth_locators=locators.mouth_locators,
            year_locators=locators.year_locators
        )

        obj.select_date(next_month.strftime('%d.%m.%Y'))
        input_value = self.driver.find_element(*locators.input_datepicker2)
        assert input_value.get_attribute('value') == next_month.strftime('%d.%m.%Y'), "Не выбрана дата."

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()


if __name__ == "__main__":
    unittest.main()
