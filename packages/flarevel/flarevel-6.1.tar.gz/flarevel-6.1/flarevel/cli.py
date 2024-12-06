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
    This group will perform a global verification of the 'forge' file.
    """
    # Ensure that the 'forge' file exists before allowing any commands to run
    verify_forge()

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
    pass

# Register make:model and make:controller commands under the forge group
forge.add_command(make_model, 'make:model')
forge.add_command(make_controller, 'make:controller')
forge.add_command(migrate, 'forge:migrate')

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
</head>
<body>
    <div class="content">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
""",
                        "home.html": """{% extends 'base.html' %}

{% block content %}
<div class="title m-b-md">
    Welcome to Flarevel
</div>
{% endblock %}
""",
                    },
                },
                "__init__.py": """from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite'
    app.config['SECRET_KEY'] = 'your_secret_key'

    db.init_app(app)
    migrate = Migrate(app, db)

    from app.Model.User import User
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
                    0.1
                )  # Simulate some delay (you can remove this or adjust as needed)

                bar.update(1)

    # Create the project folder structure (unchanged)
    create_structure(".", structure)

    # Write the config.json with project details and Flarevel version (unchanged)
    project_details = {
        "name": "Flarevel",
        "type": "project",
        "description": "The Flask MVC Package",
        "flarevel_version": "6.1",
        "license": "MIT",
        "require": {
            "python": '>=3.7',
            "flask": '>=3.1.0',
            "flask-sqlalchemy": '>=3.1.1',
            "flask-migrate": '>=4.0.7'
        }
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
