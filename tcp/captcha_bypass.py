from urllib.request import urlopen
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract
import base64
import requests
import sys

url  = "http://challenge01.root-me.org/programmation/ch8/"
path = "/tmp/captcha.png"
proxy =    {"http" :"http://127.0.0.1:8080"}
headers = {"Content-Type": "application/x-www-form-urlencoded",
            'Referer': 'http://challenge01.root-me.org/programmation/ch8/ch8.php?frame=1'}
cookies = {"PHPSESSID": ""}

def sanitize(string):
    ret = ""
    for c in string:
        if c.isalnum():
            ret = ret + c
    return  (ret)

def get_image(url):
    response = urlopen(url)
    page = response.read().decode()
    soup = BeautifulSoup(page, 'html.parser')
    img = soup.find_all("img", limit=1)[0]
    b64_image = img['src'].replace("data:image/png;base64,", '')

    return (b64_image)

# overrid image on future requests 
def convert_and_save_image(b64_image, image_path):
    with open(image_path, "wb") as fh:
        fh.write(base64.urlsafe_b64decode(b64_image))
        fh.close()

def smooth_image(image_path):
    image = Image.open(image_path)

    pixels = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            if pixels[i,j] == (0, 0, 0): # if pixel black
                image.putpixel((i,j), (255, 255, 255))
    image.save(image_path)

def get_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    text = sanitize(text)
    return (text)

def hack():

    b64_image = get_image(url)    
    convert_and_save_image(b64_image, path)
    smooth_image(path)
    captcha_text = get_text_from_image(path)
    print(f"[{captcha_text}]")
    response = requests.post(url, data=f"cametu={captcha_text}", headers=headers,cookies=cookies)#, proxies=proxy)
    resp_soup = BeautifulSoup(response.text, "html.parser")
    message = resp_soup.find_all('p',limit=1)[0]
    print(message)
    
hack()
#sys.stderr.write(response.text)
#print(response.text)
