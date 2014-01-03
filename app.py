from flask import Flask, render_template
import json
import urllib2
import time

app = Flask(__name__)

@app.route('/')
def main():
    ROOT_URL = 'http://www.reddit.com/'
    
    page = urllib2.urlopen('http://www.reddit.com/.json?limit=60')
    j = json.loads(page.read())
        
    images = []
    # pulling image urls and post links from json object
    for c in j['data']['children']:
        if (c['data']['url'][-3:] in ('jpg', 'png', 'gif')) or c['data']['url'][-4:] == 'jpeg':
            images.append([c['data']['url'], ROOT_URL + c['data']['permalink']])
        elif c['data']['url'][7:12] == 'imgur':
            images.append([c['data']['url'] + '.jpg', ROOT_URL + c['data']['permalink']])
        
    # setting current date and time    
    d = time.strftime("%A, %B %d, %Y")
    t = time.strftime("%H:%M:%S")
        
    return render_template('base.html', date=d, time=t, images=images)

app.debug = True
app.run()