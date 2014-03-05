from flask import Flask, render_template
from bs4 import BeautifulSoup
import json
import urllib
import time

app = Flask(__name__)

@app.route('/')
def main():
    ROOT_URL = 'http://www.reddit.com/'
    
    page = urllib.urlopen('http://www.reddit.com/.json?limit=60')
    j = json.loads(page.read())

    images = []
    galleries = []

    # pulling image urls and post links from json object
    for c in j['data']['children']:
        if (c['data']['url'][-3:] in ('jpg', 'png', 'gif')) or c['data']['url'][-4:] == 'jpeg':

            images.append([c['data']['url'], ROOT_URL + c['data']['permalink']])

        elif c['data']['url'][7:12] == 'imgur':
            
            imgs = get_imgur_imgs(c['data']['url'])
            
            if imgs:
                galleries.append(imgs)


    # setting current date and time    
    d = time.strftime("%A, %B %d, %Y")
    t = time.strftime("%H:%M:%S")
        
    return render_template('base.html', date=d, time=t, images=images, galleries=galleries)


def get_imgur_imgs(url):
    img_links = []

    try:
        htmltext = urllib.urlopen(url).read()
    except:
        return None
    soup = BeautifulSoup(htmltext)

    # not all Imgur galleries have div id=image-container
    # this will have to be fixed
    start_div = soup.find('div', {'id': 'image-container'})

    if start_div:
        for tag in start_div.findAll('img'):
            img_links.append(tag['data-src'])
    else:
        return None

    return img_links


app.debug = True
app.run()