import os
from flask import Flask, request
from flask_migrate import Migrate

app = Flask(__name__)

db_name = os.environ.get("POSTGRES_DB", "catalogdb")
db_user = os.environ.get("POSTGRES_USER", "cataloguser")
db_pass = os.environ.get("POSTGRES_PASSWORD", "catalogpass")
db_host = os.environ.get("POSTGRES_SERVICE_HOST", "localhost")
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"
# app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://myappuser:myapppassword@db/myappdb'

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configuração de teste
# Configure para usar uma base de dados de teste, e.g., SQLite in-memory
is_testing =  os.environ.get("TESTING", "1")
is_testing = bool(int(is_testing))
if is_testing:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = is_testing
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

from system.infrastructure.adapters.database.models import *

db.init_app(app)

migrate = Migrate(app, db)

@app.route('/')
def hello():
    return "<h1>Hello, Mundo!</h1>"

if __name__ == '__main__':
    app.run()

# Importing views
from system.adapters_entrypoints.api.routes import (
    product_views,
    general_view,
)


# Command to create tables
@app.cli.command("init-db")
def init_db():
    """Initialize the database."""
    db.create_all()
    print("Initialized the database!")
