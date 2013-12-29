import flask.views
import json
import urllib
import time

app = flask.Flask(__name__)

class Main(flask.views.MethodView):
    def get(self):
        page = urllib.urlopen('http://www.reddit.com/.json')
        j = json.loads(page.read())
        images = []
        
        for c in j['data']['children']:
            if (c['data']['url'][-3:] in ('jpg', 'png', 'gif')) or (c['data']['url'][-4:] == 'jpeg'):
                images.append(c['data']['url'])
            elif c['data']['url'][7:12] == 'imgur':
                images.append(c['data']['url'] + '.jpg')
                
        d = time.strftime("%a, %B %d, %Y")
        t = time.strftime("%H:%M:%S")
        
        return flask.render_template('base.html', images=images, date=d, time=t)


app.add_url_rule('/', view_func=Main.as_view('main'), methods=['GET'])

app.debug = True
app.run()