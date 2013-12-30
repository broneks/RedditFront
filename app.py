import flask.views
import json
import urllib2
import time

app = flask.Flask(__name__)

class Main(flask.views.MethodView):
    def get(self):
        # creating custom user agent
        req = urllib2.Request('http://www.reddit.com/.json', None, { 'User-agent': """Mozilla/5.0 (Windows NT 6.1; WOW64) 
                                                                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.
                                                                    1650.63 Safari/537.36 | by Bszulc""" })
        page = urllib2.urlopen(req)
        j = json.loads(page.read())
        
        images = []
        # pulling image urls from the json object
        for c in j['data']['children']:
            if (c['data']['url'][-3:] in ('jpg', 'png', 'gif')) or (c['data']['url'][-4:] == 'jpeg'):
                images.append(c['data']['url'])
            elif c['data']['url'][7:12] == 'imgur':
                images.append(c['data']['url'] + '.jpg')
        
        # setting current date and time    
        d = time.strftime("%a, %B %d, %Y")
        t = time.strftime("%H:%M:%S")
        
        return flask.render_template('base.html', images=images, date=d, time=t)


app.add_url_rule('/', view_func=Main.as_view('main'), methods=['GET'])

app.debug = True
app.run()
