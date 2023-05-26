from selenium.webdriver.common.by import By


input_value = (By.CSS_SELECTOR, "div#datepicker1 input")
input_datepicker1 = (By.CSS_SELECTOR, "div#datepicker1 span.input-group-addon")
back_button_locators = (By.CSS_SELECTOR, 'th[data-action="previous"]')
next_button_locators = (By.CSS_SELECTOR, 'th[data-action="next"]')
calendar = (By.CSS_SELECTOR, 'div.datepicker-days>table>tbody')
day_locators = (By.CSS_SELECTOR, 'div.datepicker-days>table>tbody td')
mouth_and_year_locators = (By.CSS_SELECTOR, 'div.datepicker-days>table th.picker-switch')


input_datepicker2 = (By.CSS_SELECTOR, "input#datepicker2")
back_button_locators2 = (By.CSS_SELECTOR, 'div#ui-datepicker-div a.ui-datepicker-prev')
next_button_locators2 = (By.CSS_SELECTOR, 'div#ui-datepicker-div a.ui-datepicker-next')
calendar2 = (By.CSS_SELECTOR, 'div#ui-datepicker-div table>tbody')
day_locators2 = (By.CSS_SELECTOR, 'div#ui-datepicker-div table>tbody td')
mouth_locators = (By.CSS_SELECTOR, 'div#ui-datepicker-div span.ui-datepicker-month')
year_locators = (By.CSS_SELECTOR, 'div#ui-datepicker-div span.ui-datepicker-year')
