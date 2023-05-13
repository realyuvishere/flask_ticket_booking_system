from flask import Flask, render_template
from flask_restful import Api

from app.utils import Configuration as Config
from app.utils import db

app = Flask(__name__)

Config.DEBUG = True

app.config.from_object(Config)
db.init_app(app=app)
api = Api(app=app, prefix=Config.API_PREFIX)
app.app_context().push()

from app.views import *

from app.api import *

api.add_resource(RatingAPI, '/rating/<int:event_id>')
api.add_resource(EventAPI, '/event', '/event/<int:event_id>')
api.add_resource(VenueAPI, '/venue', '/venue/<int:venue_id>')
api.add_resource(ShowsAPI, '/shows', '/shows/<int:show_id>') 

@app.errorhandler(404)
def page_not_found(e):
    return render_template('_404.html'), 404

if __name__ == '__main__':
    app.run()