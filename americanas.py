from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep


url_start = 'https://www.americanas.com.br/'
# Chrome diver
driver = webdriver.Chrome('./chromedriver')

# maximizar janela
# driver.maximize_window()

driver.get(url_start)
sleep(3)

buscador = driver.find_element_by_xpath('//*[@id="h_search-input"]')
sleep(1)
buscador.click()
buscador.send_keys('Notebook Core i5')
buscador.send_keys(Keys.RETURN)
sleep(5)
quantidade_produtos = driver.find_element_by_xpath('//*[@id="sort-bar"]/div/aside/div/div[1]/span')
quantidade_produtos = str(quantidade_produtos).split(' ')
print(quantidade_produtos[0].text)

links = driver.find_elements_by_xpath('//*[@id="content-middle"]/div[6]/div/div/div/div[1]/div/div/div[2]/a')
links = [link.get_attribute('href') for link in links]

for link in links:
    driver.get(link)
    sleep(5)

sleep(3)
driver.close()