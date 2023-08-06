from setuptools import setup, find_packages

classifiers = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9"
]

setup(
    name='think_agent_01',
    version='0.0.5',
    description='check for different services    e.g: Redis, SSL sertificate, Sites, Elasticsearch,Database',
    long_description_content_type="text/markdown",
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    authors='Abdugani Ibragimov and Dilshod Yuldashev',
    author_email='info@thinkland.uz',
    license='MIT',
    classifiers=classifiers,
    keywords='think_agent_01',
    packages=find_packages(),
    install_requires=['psycopg2','redis','certifi','elasticsearch','requests','sockets','PyYAML']
)
