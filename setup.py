from setuptools import setup, find_packages

requires = [
    'beautifulsoup4',
    'lxml',
    'python-dotenv',
    'requests',
    'selenium',
    'sqlalchemy'
]

setup(
    name='balance_checker',
    version='0.1',
    url='https://github.com/PauliusU/balance_checker',
    description='Scrape balance data of European P2P platforms',
    author='PauliusU',
    author_email='48020370+PauliusU@users.noreply.github.com',
    install_requires=requires
)
