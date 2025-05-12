from setuptools import setup

AUTHOR_NAME = 'Hajar_Hiba'
LIST_OF_REQUIREMENTS = ['streamlit']

setup(
    author = AUTHOR_NAME,
    author_email = 'hhproject@gmail.com',
    description = 'Movie recommender app',
    python_requires = '>=3.7',
    install_requires = LIST_OF_REQUIREMENTS,
)