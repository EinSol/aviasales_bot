from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from decouple import config
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from search_screen.texts import country_list, city_list

username = config('USERNAME')
password = config('PASS')
env = config('ENV')

options = Options()
if env == 'DEBUG':
    path_driver = config('PATH_TO_DRIVER')
    path_chrome = config('PATH_TO_CHROME')
    options.binary_location = path_chrome  # chrome binary location specified here

options.add_argument("--headless")
options.add_argument("--start-maximized")  # open Browser in maximized mode
options.add_argument("--no-sandbox")  # bypass OS security model
options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
chrome_prefs = {}
options.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}


def get_info(param):
    """
    Input: dict {'destination_country': str,
              'departure_city': str,
              'min_nights': str,
              'max_nights': str,
              'date': 'dd.mm.yyyy - dd.mm.yyyy',
              'adults': str,
              'kids': str,
              'stars': list(str),
              'food': list(str)
                }
    Output: list [
                dict {
                      'hotel_name': str,
                      'stars': str,
                      'start_price': str,
                      'town': str,
                      'tours': list [
                                dict {
                                     'arrival_date': 'dd.mm.yyyy',
                                     'food': str,
                                     'nights': str,
                                     'price': str,
                                     'room': str
                                    }
                                ]
                     }
                 ]

    """

    if env == 'DEBUG':
        driver = webdriver.Chrome(options=options, executable_path=path_driver)
    else:
        driver = webdriver.Chrome(options=options)

    driver.get(config('URL'))
    wait = WebDriverWait(driver, 50)

    try:
        # find password input field and insert username
        username_field = wait.until(EC.visibility_of_element_located((By.ID, 'loginform-login')))
        username_field.send_keys(username)

        # find password input field and insert password as well
        password_field = wait.until(EC.visibility_of_element_located((By.ID, 'loginform-password')))
        password_field.send_keys(password)

        # click login button
        log_in_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@type='submit']")))
        log_in_button.click()

        # wait till page is rendered
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "card-calendar")))

        # go to search page
        navbar = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'navbar-toggler')))
        navbar.click()

        # wait till navbar is opened
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "material-icons")))

        # choose search page
        search_link = driver.find_element_by_xpath("//*[contains(@href,'/search')]")
        search_link.click()

        #######################################
        # destination country
        actions = ActionChains(driver)

        destination_block = wait.until(EC.visibility_of_element_located((By.ID, "country_id_chosen")))
        actions.move_to_element(destination_block)
        actions.click(destination_block)
        actions.perform()
        actions = ActionChains(driver)
        destination_list = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "chosen-results")))
        countries = destination_list.find_elements_by_tag_name("li")
        for country in countries:
            if country.text == country_list[param['destination_country']]:
                actions.move_to_element(country).click().perform()

        # departure city
        actions = ActionChains(driver)
        departure_city_block = wait.until(EC.visibility_of_element_located((By.ID, "town_from_id_chosen")))
        actions.move_to_element(departure_city_block)
        actions.click(departure_city_block)
        actions.perform()
        actions = ActionChains(driver)
        destination_list = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "chosen-results")))[1]
        print(destination_list.text)
        cities = destination_list.find_elements_by_tag_name("li")
        for city in cities:
            if city.text == city_list[param['destination_country']]:
                actions.move_to_element(city).click(city).perform()

        # date
        date_input = wait.until(EC.visibility_of_element_located((By.ID, "search_date")))
        date_input.send_keys(param['date'])

        # min nights
        select = wait.until(EC.visibility_of_element_located((By.ID, "nights_from")))
        ActionChains(driver).move_to_element(select).click().perform()
        select = Select(select)
        select.select_by_visible_text(param['min_nights'])

        # max nights
        select = wait.until(EC.visibility_of_element_located((By.ID, "nights_till")))
        ActionChains(driver).move_to_element(select).click().perform()
        select = Select(select)
        select.select_by_visible_text(param['max_nights'])

        # adults
        select = wait.until(EC.visibility_of_element_located((By.ID, "adult_count")))
        ActionChains(driver).move_to_element(select).click().perform()
        select = Select(select)
        select.select_by_visible_text(param['adults'])

        # kids
        select = wait.until(EC.visibility_of_element_located((By.ID, "children_count")))
        ActionChains(driver).move_to_element(select).click().perform()
        select = Select(select)
        select.select_by_visible_text(param['kids'])

        # hotel stars
        stars_block = wait.until(EC.visibility_of_element_located((By.NAME, "STARS")))
        stars_list = stars_block.find_elements_by_tag_name('input')
        for star in stars_list:
            if star.get_attribute('value') in param['stars']:
                star.click()

        # food
        food_block = wait.until(EC.visibility_of_element_located((By.ID, "MEAL")))
        food_list = food_block.find_elements_by_tag_name('input')
        for food in food_list:
            if food.get_attribute('value') in param['food']:
                food.click()

        # search
        search_button = wait.until(EC.visibility_of_element_located((By.ID, "searchButton")))
        actions.move_to_element(search_button).click().perform()

        # find offers
        offers = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "tourua-price")))
        proceed_offers = []
        for offer in offers:
            actions = ActionChains(driver)
            start_price = offer.find_element_by_class_name('price').find_element_by_tag_name(
                'a').text.split(' ')[1:]
            print(offer.find_element_by_class_name('town-name').text[12:])
            proceed_offer = {'town': offer.find_element_by_class_name('town-name').text[12:],
                             'hotel_name': ' '.join(
                                 offer.find_element_by_class_name('tourua-hotel-name').text.split(' ')[1:]),
                             'stars': offer.find_element_by_class_name('tourua-hotel-name').find_element_by_xpath(
                                 '..').text[-2:-1],
                             'start_price': '.'.join(start_price)}

            open_list_button = offer.find_element_by_class_name('result-icon').find_element_by_class_name(
                'material-icons')
            actions.move_to_element(open_list_button).click().perform()

            possible_tours = wait.until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME, 'tourua-price-detail')))[:-1]
            proceed_offer['tours'] = []
            for tour in possible_tours:
                tour_info = {}
                information_blocks = tour.find_elements_by_tag_name('div')
                tour_info['room'] = information_blocks[1].text
                tour_info['food'] = information_blocks[2].text
                tour_info['arrival_date'] = information_blocks[3].text.split(' ')[0][:-1]
                tour_info['nights'] = information_blocks[3].text.split(' ')[1].split('н')[0]
                tour_info['price'] = information_blocks[3].find_element_by_tag_name('a').get_attribute(
                    'text').strip()
                proceed_offer['tours'].append(tour_info)

            open_list_button.click()
            proceed_offers.append(proceed_offer)
        driver.close()
        return proceed_offers

    except Exception as e:
        print(e)
        driver.close()
        return
