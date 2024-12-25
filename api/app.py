from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from models import db
from routes import books_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/books'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 32,
    'pool_recycle': 60,
    'pool_pre_ping': True,
    'pool_timeout': 30
}

CORS(app)
Swagger(app)
db.init_app(app)

app.register_blueprint(books_bp, url_prefix='/books')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)