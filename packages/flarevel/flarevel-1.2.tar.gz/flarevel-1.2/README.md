# Flarevel

`flarevel` is a Python command-line tool that helps you quickly create a Flask project with a predefined folder structure. It generates the necessary files for a basic Flask application with SQLAlchemy support, a home page, and a user model.

## Features

- Generates a Flask project with a predefined structure.
- Includes a sample HomeController and User model.
- Includes basic project setup with templates and static assets.
- Automatically creates the necessary directories and files.
- Simple command-line interface to create the project.

## Installation

To install `flarevel`, you can use `pip`:

```bash
pip install flarevel
```

## Usage

To create a new Flarevel project, simply run the following command:

```bash
flarevel create <project_name>
```

You can install the necessary dependencies by running:
```bash
pip install -r requirements.txt
```

## Run the application

After generating the project, you can run it by executing the following command in the project directory:

```bash
python run.py
```

This will start the Flarevel development server, and you can view the project in your browser at http://localhost:5000# flarevel