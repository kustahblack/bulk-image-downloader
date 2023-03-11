from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
import shutil
import os
import os.path
from webdriver_manager.chrome import ChromeDriverManager

def check(url):
    if url.endswith(".jpg"):
        return "jpg"
    if url.endswith(".png"):
        return "png"
    else:
        return "false"

def download(url,num,format,keyword):
    try:
      start = time.time()
      response = requests.get(url,stream=True,timeout=1)
      if time.time() - start < 1:
        with open(f"{keyword} images/image{num+1}.{format}", 'wb') as out_file:
       	  shutil.copyfileobj(response.raw, out_file)
        if response.status_code == 200:
            print(f"{num+1}th picture downloaded. ",url)
            return True
        else:
          print(f"{num+1}th picture couldnt be downloaded.")
          return False
      else:
        print("Passing the picture...")
        return False
    except:
      print(f"Error occured while {num+1}th image downloading.")
      return False

search_word = input("Download pictures of: ")
number_of_images = int(input("Download this much: "))

options = webdriver.ChromeOptions()
aw = "n"
if (aw == "n"):
  options.add_argument("headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
browser = webdriver.Chrome(ChromeDriverManager().install(),options=options)

browser.get(f"https://yandex.com/images/search?text={search_word}")

#browser.get("https://images.yandex.com/")
#search_field = browser.find_element_by_name("text")
#search_field.send_keys(search_word)
#search_field.send_keys(Keys.RETURN)
os.system("cls")
while True:
  try:
    images = browser.find_elements_by_css_selector(".serp-item__preview")
    break
  except: pass


i = 0
downloaded = 0

print("Clicking on the first picture...")
images[0].click()
os.system("cls")
if os.path.exists(f"{search_word} images") == False:
  os.mkdir(f"{search_word} images")

surebaslat = time.time()
while downloaded<number_of_images:
    try:
      buton = browser.find_element_by_xpath("/html/body/div[12]/div[2]/div/div/div/div[3]/div/div[2]/div/div/div[1]/div[4]/div[1]/a")
      print("Fetching link data...")
      url = buton.get_attribute("href")
    except:
      browser.find_element_by_xpath("//body").send_keys(Keys.ARROW_RIGHT)
      continue
    print("Format checking...")
    if check(url) != "false":
      print("Valid Format, downloading...")
      if(download(url,downloaded,check(url),search_word)==False):
          if (os.path.isfile(f"{search_word} images/image{downloaded+1}.{check(url)}")): os.remove(f"{search_word} images/image{downloaded+1}.{check(url)}")
      else: downloaded = downloaded+1
    else: print("Invalid format, passing.")
    browser.find_element_by_xpath("//body").send_keys(Keys.ARROW_RIGHT)
    print("Downloaded successfully.")
    os.system("cls")

browser.quit()
gecensure = time.time() - surebaslat

print("Process completed.")
print("Time elapsed: ", gecensure, "seconds")
gecensure = float(gecensure)
result = "{:.2f}".format(gecensure)
with open(f"{search_word} images/inf.txt", "a") as f:
    f.write(f"{downloaded} {search_word} pictures downloaded in {result} seconds.\nBot Made by Kustah")