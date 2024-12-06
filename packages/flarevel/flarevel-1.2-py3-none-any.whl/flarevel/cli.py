import os
import click
import sys
import time

@click.group()
def cli():
    """
    Main entry point for the flarevel CLI.
    """
    pass

@click.command()
@click.argument('project_name')
def create(project_name):
    """
    Create a Flask project with the given PROJECT_NAME and a predefined structure.
    """
    # Define the folder and file structure with content
    structure = {
        project_name: {
            "app": {
                "Http": {
                    "Controller": {
                        "__init__.py": "",
                        "HomeController.py": """from flask import Blueprint, render_template

home_blueprint = Blueprint(
    'home', 
    __name__, 
    static_folder='../../Resources/static', 
    template_folder='../../Resources/template'
)

@home_blueprint.route('/')
def home():
    return render_template('home.html', title="Welcome to Flarevel")
""",
                    },
                },
                "Model": {
                    "__init__.py": "",
                    "User.py": """from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"
""",
                },
                "Resources": {
                    "static": {
                        "css": {},
                        "js": {},
                    },
                    "template": {
                        "base.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <title>{{ title }}</title>
    <style>
        html, body {
            height: 100%;
            margin: 0;
            font-family: 'Nunito', sans-serif;
            font-weight: 200;
            display: flex;
            justify-content: center;
            align-items: center;
            color: #636b6f;
            background-color: #f5f8fa;
        }
        .full-height {
            height: 100%;
        }
        .flex-center {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            text-align: center;
        }
        .title {
            font-size: 84px;
            color: #4caf50;
            margin-bottom: 30px;
        }
        .links > a {
            color: #636b6f;
            padding: 0 25px;
            font-size: 14px;
            font-weight: 600;
            letter-spacing: .1rem;
            text-decoration: none;
            text-transform: uppercase;
            transition: color 0.3s;
        }
        .links > a:hover {
            color: #4caf50;
        }
        .m-b-md {
            margin-bottom: 30px;
        }
    </style>
</head>
<body>

    <div class="flex-center full-height">
        <div class="content">
            {% block content %}{% endblock %}
        </div>
    </div>
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>
""",
                        "home.html": """{% extends 'base.html' %}

{% block content %}
<div class="title m-b-md">
    Welcome to Flarevel
</div>
<div class="links">
    <a href="https://www.python.org/" target="_blank">Python Official Site</a>
    <a href="https://docs.python.org/3/" target="_blank">Documentation</a>
    <a href="https://pypi.org/" target="_blank">PyPI</a>
    <a href="https://flask.palletsprojects.com/" target="_blank">Flask</a>
    <a href="https://realpython.com/" target="_blank">Learn Python</a>
</div>
{% endblock %}
""",
                    },
                },
                "Seeds": {},
                "__init__.py": """from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite'  # Corrected URI
    app.config['SECRET_KEY'] = 'your_secret_key'

    db.init_app(app)
    migrate = Migrate(app, db)

    # Import models so they are registered with SQLAlchemy
    from app.Model.User import User

    # Register Routes
    from app.Http.Controller.HomeController import home_blueprint
    app.register_blueprint(home_blueprint)

    return app
""",
            },
            "config.py": """class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.sqlite'
    SECRET_KEY = 'your_secret_key'
""",
            "run.py": """from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
""",
            "requirements.txt": "flask\nflask-sqlalchemy\nflask-migrate\n",
        }
    }

    # Spinner function
    def spinner():
        spinner_chars = ['|', '/', '-', '\\']
        while True:
            for char in spinner_chars:
                yield char

   # Function to create the directory structure
    def create_structure(base_path, structure):
        total_files = sum([len(content) if isinstance(content, dict) else 1 for content in structure.values()])
        sp = spinner()  # Create a spinner instance
        with click.progressbar(length=total_files, label="Creating project files", file=sys.stdout) as bar:
            for name, content in structure.items():
                path = os.path.join(base_path, name)
                if isinstance(content, dict):
                    os.makedirs(path, exist_ok=True)
                    create_structure(path, content)
                else:
                    with open(path, 'w') as f:
                        f.write(content)
                
                # Show a spinner for each file creation
                sys.stdout.write(f'\r{next(sp)} Creating {name}...')
                sys.stdout.flush()
                time.sleep(0.1)  # Simulate some delay (you can remove this or adjust as needed)

                bar.update(1)

    # Create the project folder structure
    create_structure('.', structure)
    click.echo(f"\nFlask project '{project_name}' created successfully!")

# Register the `create` command to the `cli` group
cli.add_command(create)

if __name__ == '__main__':
    cli()