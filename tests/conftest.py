import pytest
from selenium import webdriver  # подключение библиотеки

# driver = webdriver.Chrome()
# driver.implicitly_wait(10)

@pytest.fixture(autouse=True)
def testing():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    pytest.driver = webdriver.Chrome(r'C:\Users\Sever\PycharmProjects\task\_30_5_1_selenium\tests\chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.quit()

