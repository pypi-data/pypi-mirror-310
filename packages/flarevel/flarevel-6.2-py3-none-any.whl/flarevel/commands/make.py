import os
import click
import subprocess
from flask.cli import with_appcontext

@click.command()
@click.argument('model_name')
def make_model(model_name):
    """Create a new model file."""
    model_path = f"App/Model/{model_name}.py"
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    if os.path.exists(model_path):
        click.echo(f"Model '{model_name}' already exists.")
        return
    
    with open(model_path, 'w') as model_file:
        model_file.write(
f"""from app import db

class {model_name.title()}(db.Model):
    __tablename__ = '{model_name}'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<{model_name.title()} {{self.id}}>"
""")
    click.echo(f"Model '{model_name}' created at '{model_path}'.")

@click.command()
@click.argument('controller_name')
def make_controller(controller_name):
    """Create a new controller file with support for directories."""
    file_path = controller_name.replace("/", os.sep)  # Handle nested directories
    module_name = file_path.split(os.sep)[-1].lower()  # Get the file name
    blueprint_name = controller_name.replace("/", "_").lower()  # Flask-compliant name
    
    controller_path = f"App/Http/Controller/{file_path}.py"
    os.makedirs(os.path.dirname(controller_path), exist_ok=True)
    
    if os.path.exists(controller_path):
        click.echo(f"Controller '{controller_name}' already exists.")
        return

    with open(controller_path, 'w') as controller_file:
        controller_file.write(
f"""from flask import Blueprint, render_template

{blueprint_name}_blueprint = Blueprint(
    '{blueprint_name}',
    __name__,
    static_folder='../../Resources/static',
    template_folder='../../Resources/template'
)

@{blueprint_name}_blueprint.route('') # Add your route here
def index():
    return render_template('', title="")
""")
    click.echo(f"Controller '{controller_name}' created at '{controller_path}'.")

@click.command()
@with_appcontext  # Ensure this command runs within the app context
def migrate():
    """Run database migrations (init, migrate, upgrade)."""
    try:
        # Step 1: Check if migrations directory exists
        migrations_path = "migrations"
        if not os.path.exists(migrations_path):
            click.echo("Initializing database migrations...")
            subprocess.run(["flask", "db", "init"], check=True)
        else:
            click.echo("Migrations directory already exists. Skipping initialization.")
        
        click.echo("Running migration...")
        subprocess.run(["flask", "db", "migrate"], check=True)
        
        click.echo("Upgrading database...")
        subprocess.run(["flask", "db", "upgrade"], check=True)
        
        click.echo("Database migrations applied successfully!")
    
    except subprocess.CalledProcessError as e:
        click.echo(f"Error during migration: {e}")