from setuptools import setup, find_packages

setup(
    name='flarevel',  # Name of your tool
    version='5.0.0',
    description='Flarevel is a command-line interface (CLI) tool that quickly scaffolds Flask projects with a robust Model-View-Controller (MVC) architecture. It generates a well-organized project structure, including dedicated folders for models, views, controllers, and configurations, enabling developers to start building scalable and maintainable Flask applications in no time. Flarevel streamlines the setup process, saving you time and ensuring a clean, modular foundation for your projects.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Yorts',
    author_email='casterr@protonmail.com',
    url='https://github.com/Yorts11/flarevel',
    packages=find_packages(),
    install_requires=['Click'],  # Dependencies
    entry_points={
        'console_scripts': [
            'flarevel = flarevel.cli:cli',  # This is the updated entry point
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
