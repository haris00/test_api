from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from test_api.config import Config
from flask_restplus import Api
from flask_marshmallow import Marshmallow

# initialize app
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy()
db.init_app(app)
db.app = app
ma = Marshmallow(app)
# import models
from test_api.models import *
db.create_all()
#db.drop_all()

authorizations = {
    'apikey' : {
        'type' : 'apiKey',
        'in' : 'header',
        'name' : 'X-API-KEY'
    }
}


rest_api = Api(app, authorizations=authorizations)


# import routes
from test_api import routes, api


