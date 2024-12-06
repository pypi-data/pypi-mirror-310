import os
import sys
import time
import click
import json
from flarevel.commands.make import make_model, make_controller, migrate


@click.group()
def cli():
    """
    Main entry point for the Flarevel CLI.
    """
    # Ensure that the 'forge' file exists before allowing any commands to run
    pass


# Check if the 'forge' file exists and is correctly configured
def verify_forge():
    """Verify that the forge file exists and is valid."""
    expected_forge_path = os.path.join(os.getcwd(), "forge")

    # Check if the 'forge' file exists
    if not os.path.exists(expected_forge_path):
        click.echo("Error: Could not open input file: forge")
        sys.exit(1)

    # Check the content of the 'forge' file
    with open(expected_forge_path, "r") as forge_file:
        content = forge_file.read()
        if "from flarevel.cli import cli" not in content:
            click.echo("Error: The 'forge' file is not configured correctly.")
            sys.exit(1)


# Now we register subcommands under the forge group
@click.group()
def forge():
    """Group of commands related to Flarevel's generation tool."""
    verify_forge()


# Register make:model and make:controller commands under the forge group
forge.add_command(make_model, "make:model")
forge.add_command(make_controller, "make:controller")
forge.add_command(migrate, "migrate")

# Add the forge group to the main CLI
cli.add_command(forge)


# The create command that generates the Flask project
@click.command()
@click.argument("project_name")
def create(project_name):
    """
    Create a Flask MVC project with Flarevel.
    """
    # Define the folder and file structure (same as before)
    structure = {
        project_name: {
            "app": {
                "Http": {
                    "Controller": {
                        "__init__.py": "",
                        "HomeController.py": """# App/Http/Controller/HomeController.py
                                                
from flask import render_template

# Add @staticmethod every def
class HomeController:
    return
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
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"
""",
                },
                "Resources": {
                    "static": {
                        "css": {
                            "style.css": """
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
                                """
                        },
                        "js": {},
                    },
                    "template": {
                        "base.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link type="text/css" rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <title>Welcome to Flarevel</title>
</head>
<body>
    <div class="flex-center full-height">
        <div class="content">
            {% block content %}{% endblock %}
        </div>
    </div>
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
                <a href="https://pypi.org/project/flarevel/" target="_blank">Documentation</a>
                <a href="https://flask.palletsprojects.com/" target="_blank">Flask</a>
                <a href="https://realpython.com/" target="_blank">Learn Python</a>
            </div>
{% endblock %}
""",
                    },
                },
                "routes": {
                    "__init__.py": "",
                    "web.py": """from flask import Blueprint, render_template
                    
# Web Routes
# Here is where you can register web routes for your application.

web = Blueprint(
    'web',
    __name__,
    static_folder='../Resources/static',  # Path to Resources/static
    template_folder='../Resources/template'  # Path to Resources/tempalte)
    
@web.route('/')
def home():
    return render_template('home.html', title="Welcome to Flarevel")
                    """,
                },
                "__init__.py": """from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import importlib
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__,static_folder='Resources/static')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite'
    app.config['SECRET_KEY'] = 'your_secret_key'

    db.init_app(app)
    migrate = Migrate(app, db)

    # Dynamically import all models in app.Model
    models_directory = os.path.join(os.path.dirname(__file__), 'Model')
    for filename in os.listdir(models_directory):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = f"app.Model.{filename[:-3]}"
            importlib.import_module(module_name)
    
    
    from app.routes.web import web
    app.register_blueprint(web)

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

    def spinner():
        spinner_chars = ["|", "/", "-", "\\"]
        while True:
            for char in spinner_chars:
                yield char

    # Function to create the directory structure (same as before)
    def create_structure(base_path, structure):
        total_files = sum(
            [
                len(content) if isinstance(content, dict) else 1
                for content in structure.values()
            ]
        )
        sp = spinner()  # Create a spinner instance
        with click.progressbar(
            length=total_files, label="Creating project files", file=sys.stdout
        ) as bar:
            for name, content in structure.items():
                path = os.path.join(base_path, name)
                if isinstance(content, dict):
                    os.makedirs(path, exist_ok=True)
                    create_structure(path, content)
                else:
                    with open(path, "w") as f:
                        f.write(content)

                # Show a spinner for each file creation
                sys.stdout.write(f"\r{next(sp)} Creating {name}...")
                sys.stdout.flush()
                time.sleep(
                    0.3
                )  # Simulate some delay (you can remove this or adjust as needed)

                bar.update(1)

    # Create the project folder structure (unchanged)
    create_structure(".", structure)

    # Write the config.json with project details and Flarevel version (unchanged)
    project_details = {
        "name": "Flarevel",
        "type": "project",
        "description": "The Flask MVC Package",
        "flarevel_version": "5.0.0",
        "license": "MIT",
        "require": {
            "python": ">=3.7",
            "flask": ">=3.1.0",
            "flask-sqlalchemy": ">=3.1.1",
            "flask-migrate": ">=4.0.7",
        },
    }
    with open(os.path.join(project_name, "project.json"), "w") as json_file:
        json.dump(project_details, json_file, indent=4)

    # Create the forge file in the project directory (unchanged)
    forge_content = """import os
import sys
from flarevel.cli import cli

if __name__ == "__main__":
    cli()
"""
    with open(os.path.join(project_name, "forge"), "w") as forge_file:
        forge_file.write(forge_content)

    click.echo(f"\nFlask project '{project_name}' created successfully with Flarevel!")


# Register the create command to the cli group
cli.add_command(create)

if __name__ == "__main__":
    cli()
