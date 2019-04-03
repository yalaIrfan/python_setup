from flask import Flask,render_template
from flask_cors import CORS

from src.config import Config
from flask_pymongo import PyMongo
# from bson.objectid import ObjectId
from flask_restful import Resource, Api
from flask_compress import Compress
from flask_caching import Cache

mongo = PyMongo()
compress = Compress()
cache = Cache(config={'CACHE_TYPE': 'simple'})


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    api = Api(app)

    # mongo = PyMongo(app)

    mongo.init_app(app)
    compress.init_app(app)

    
    cache.init_app(app)


    # db.init_app(app)
    # bcrypt.init_app(app)

    from src.spell.routes import spell  
    from src.isi.routes import isi
    from src.claims.routes import claims
    from src.contentcompare.routes import contentcompare
    from src.errors.handlers import errors


    @app.route("/")
    def home():
        return render_template("upload.html")


    app.register_blueprint(spell)
    app.register_blueprint(isi) 
    app.register_blueprint(claims)
    app.register_blueprint(contentcompare)
    app.register_blueprint(errors)

    return app