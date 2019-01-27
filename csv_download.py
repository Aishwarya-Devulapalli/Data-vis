from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from itertools import zip_longest as zip
import csv
import locale
import pandas as pd



options = webdriver.ChromeOptions()
options.add_argument('headless')


locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
i = 1
while i <=30:
    if i < 10:
     date = '2018-09-0' + str(i)
    elif i >=10:
     date = '2018-09-' + str(i)


    driver = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
    url = r'https://tools.wmflabs.org/topviews/?project=en.wikipedia.org&platform=all-access&date=' + date + '&excludes='
    driver.get(url)


    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "topview-entries")))
   # driver.minimize_window()


    while True:
     try:
         driver.find_element_by_link_text("Show more")
         driver.find_element_by_link_text('Show more').click()
         try:
          wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "show-more")))
         except TimeoutException:
          print("time out")
     except NoSuchElementException:
         break

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    headers = ["Page", "Pageviews", "Date"]

    name = []
    views = []


    for table in soup.find_all('tbody', attrs={'class': 'topview-entries'}):
     for dl in table.find_all('div',{'class':'topview-entry--label'}):
      for label in dl.find_all('a'):
        name.append(label.text)
     for count in table.find_all('a',{'class':'topview-entry--views'}):
        views.append(locale.atoi(count.text))


    ext = '.csv'
    # months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
    #           "November", "December"]
    file_name = r"PageViews2018\September" + "\\" + date + ext
    dat = pd.to_datetime(date)

    with open(file_name, "w", newline='', encoding="utf-8") as f:
       wr = csv.writer(f)  # delimiter= ' ')
       wr.writerow(headers)
       for (n,v) in zip(name,views):
        row = []
        row.append(n)
        row.append(v)
        row.append(dat.date())
        wr.writerow(row)

    f.close()
    i = i+1

    driver.close()
