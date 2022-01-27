from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import json, time

def main():
    # nie ma co się bać żeby tutaj podać swoje passy, bo plik macie tylko lokalnie
    login_data = open('account_details.json')
    data = json.load(login_data)

    LOGIN = data['login']
    PASSWORD = data['password']
    WORLD = data['world']

    print(f'{LOGIN}, {PASSWORD}, {WORLD}')

    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    options.add_argument('--disable-extensions')

    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

    driver.get("https://plemiona.pl")

    login = driver.find_element(value="username", by=By.NAME)
    login.send_keys(LOGIN)
    password = driver.find_element(value="password", by=By.NAME)
    time.sleep(2)

    password.send_keys(PASSWORD)
    time.sleep(3)

    login.send_keys(Keys.RETURN)
    time.sleep(25)

    output_file = open('ataki.txt', "w")

    try:
        worlds = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CLASS_NAME, "worlds-container"))
        )

        world_buttons = worlds.find_elements(value="world_button_active", by=By.CLASS_NAME)
        chosen_world = None

        for button in world_buttons:
            if button.get_attribute('innerHTML') == f'Świat {WORLD}':
                chosen_world = button

        chosen_world.click()
        clan_window = driver.find_element(value='//*[@id="menu_row"]/td[10]/a', by=By.XPATH).click()

        clan_members_window = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="content_value"]/table/tbody/tr/td[4]/a'))
        ).click()

        incoming_attack_window = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ally_content"]/table[1]/tbody/tr/td[2]/a'))
        ).click()

        drop_down_players_menu = Select(driver.find_element(value='player_id', by=By.NAME))

        all_players = drop_down_players_menu.options

        names = []
        for i in range(1, len(all_players)):
            names.append(all_players[i].text)

        for i in range(0, len(all_players)):
            try:
                Select(driver.find_element(value='player_id', by=By.NAME)).select_by_visible_text(names[i])

                villages_all = WebDriverWait(driver, 4).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="ally_content"]/div/div/table'))
                )

                villages_list = villages_all.find_elements(value='tr', by=By.TAG_NAME)

                for j in range(1, len(villages_list)):
                    village = villages_list[j].find_element(value='a', by=By.TAG_NAME).get_attribute('innerHTML').strip()
                    attacks_on_village = villages_list[j].find_element(value='hidden', by=By.CLASS_NAME).get_attribute('innerHTML').strip()

                    output_file.write(f'GRACZ: {names[i]} WIOSKA:{village}, ATAKI NA WIOSKE: {attacks_on_village}\n')
            except IndexError:
                pass
    finally:
        time.sleep(2)
        output_file.close()
        driver.quit()


if __name__ == "__main__":
    main()