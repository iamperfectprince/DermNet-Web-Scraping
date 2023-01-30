from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.chrome.options import Options
# from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import os
import time
import pandas as pd
import requests
from PIL import Image

path="C:/Icon_images_of_diseases"
if not os.path.exists(path):
    os.mkdir("C:/Icon_images_of_diseases")

driver = webdriver.Chrome(executable_path="C:\\Users\\Prince Thakur\\chromedriver.exe")
driver.get("https://dermnetnz.org/image-library")
# options.add_argument("--headless")
driver.maximize_window()
# driver.implicitly_wait(3)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

Name_of_Diseases_list = []
Urls_list = []
Images_list = []


page_check = WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH,'//*[@class="imageList__group__item__copy"]/h6'))).text
rows = WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH, '//*[@class="[ js-content-images ] "]'))).find_elements(By.CSS_SELECTOR, '.imageList__group__item')
length = len(rows)
print(length)

for k in range(0,length):
    html_element = WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH, "//div[5]/div/div/div[1]/div[3]"))).find_elements(By.CSS_SELECTOR, '.imageList__group__item')[k]
    
    try:
        urls = html_element.find_element(By.XPATH,"//*[@class='imageList__group__item']").get_attribute("href")
        Urls_list.append(urls)
        print(urls)
    except:
        pass
    
    try:
        full_name = html_element.find_element(By.CSS_SELECTOR,"div.imageList__group__item__copy > h6").text
        diseases_name = re.split("images", full_name)[0]
        if full_name != "":
            Name_of_Diseases_list.append(diseases_name)
            print(diseases_name)
        else:
            print("No diseases_name Found for %s" %urls)
        
    except:
        pass

    try:
        images_link = html_element.find_element(By.CSS_SELECTOR,"div.imageList__group__item__image > img").get_attribute("src")
        if images_link != "":
            Images_list.append(images_link)
            tmp_img_name=diseases_name.replace(" ","_")
            img = Image.open(requests.get(images_link, stream = True).raw)       
            img.save('%s/%s.jpg' %(path,tmp_img_name))
            if os.path.exists("%s/%s.jpg" %(path,tmp_img_name)):
                print("Successfully Downloaded %s" %tmp_img_name)
            else:
                print("Error in downloading image For %s" %full_name)
        else:
            print("No images_link Found  for %s" %full_name)
    except:
        pass
data_list = {
    "Name of Diseases": Name_of_Diseases_list,
    "URLs associated with diseases": Urls_list,
    "Icon images of diseases": Images_list,
}

df = pd.DataFrame.from_dict(data_list)
df.transpose()
df.to_csv("dermnetnz_org.csv",index=False)   
            
time.sleep(1)
driver.quit()
