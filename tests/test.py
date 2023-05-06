import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from settings import valid_email, valid_password, valid_user_name


def test_show_my_pets():
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys(valid_email)

    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys(valid_password)

    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'body > div > div > form > div:nth-of-type(3) > button').click()
    # Ожидание появления заголовка "PetFriends"
    WebDriverWait(pytest.driver, 1).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    # Нажимаем на кнопку перехода на страницу своих питомцев
    pytest.driver.find_element(By.CSS_SELECTOR, 'div#navbarNav > ul > li > a').click()
    # Ожидание появления заголовка с именем пользователя
    WebDriverWait(pytest.driver, 1).until(EC.visibility_of_element_located((By.TAG_NAME, 'h2')))
    # Проверяем, что мы оказались на странице своих питомцев
    assert pytest.driver.find_element(By.TAG_NAME, 'h2').text == valid_user_name

    # Берем данные всех карточек питомцев
    pet_cards = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr')
    # Ожидание появления карточек питомцев
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr')))
    # Проверяем что карточки питомцев присутствуют на странице
    assert len(pet_cards) > 0
    # Создаем множество для хранения имен питомцев
    pet_names = set()
    # Берем данные питомцев из карточек
    for card in pet_cards:
        pet_info = card.text.split()
        if '×' in pet_info:
            pet_info.remove('×')  # удаляем символ '×'
        # Проверяем, что у всех питомцев есть имя, возраст и порода
        assert len(pet_info) == 3
        # Проверяем, что у всех питомцев разные имена
        pet_name = pet_info[0]
        assert pet_name not in pet_names
        pet_names.add(pet_name)

    list_pets = len(pet_cards)

    # Выбираем статистику питомцев
    number_of_pets = pytest.driver.find_elements(By.XPATH,
                                                 "//text()[contains(., 'Питомцев: " + str(list_pets) + "')]/..")
    # Извлекаем количество питомцев и проверяем совпадение со списком карточек
    number_of_pets_text = number_of_pets[0].text
    pattern = r"\d+"  # Регулярное выражение "\d+" соответствует одной или более цифр
    match = re.search(pattern, number_of_pets_text)
    # Проверяем, что присутствуют все питомцы
    assert len(pet_cards) == int(match.group())

    # Выбираем фото в карточках питомца
    images = pytest.driver.find_elements(By.CSS_SELECTOR, "th[scope='row'] img")
    # Ожидание появления заголовка с именем пользователя
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "th[scope='row'] img")))
    # Получаем количество питомцев с фото и вычисляем половину всех питомцев
    number_of_pets_with_photo = sum(len(img.get_attribute("src")) > 0 for img in images)
    half_count = list_pets // 2
    # Проверяем что, хотя бы у половины питомцев есть фото
    assert number_of_pets_with_photo >= half_count

    # Берем данные всех карточек питомцев
    pet_cards = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr')
    # Проверяем что карточки питомцев присутствуют на странице
    assert len(pet_cards) > 0

    # Создаем множество для хранения уникальных значений информации о карточках и фотографиях
    card_info_set = set()

    # Проверяем, что данные питомцев заполнены и карточки с фотографиями уникальными данными
    for card in pet_cards:
        # Ожидание появления карточек питомцев
        WebDriverWait(pytest.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr')))
        pet_info = card.text.split()
        photo = card.find_element(By.CSS_SELECTOR, 'th[scope="row"] img')
        photo_src = photo.get_attribute("src")

        # Преобразуем информацию о карточке и фотографии в кортеж
        card_info = (tuple(pet_info), photo_src)
        # Проверяем, что карточка с фотографией не встречалась ранее
        assert card_info not in card_info_set
        card_info_set.add(card_info)
