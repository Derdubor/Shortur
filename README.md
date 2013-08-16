Shortur
=======

A simple shorturl service based on python3 and Pyramid

Installation
------------

You'll need a version of python3 installed. Things might run on python2 (preferrably a rather recent version in that case), but compatibility is not a neither a goal nor a priority. We test and develop on python3.2+.

This recipe creates a dedicated virtualenv to contain Shortur and its dependencies by themselves. If you want to host stuff inside an existing virtualenv, I assume you're able to deduce what parts are relevant for your installation by yourself.

First, create a virtualenv to host your app and pyramid installation. If python3 isn't installed as python, you can provide the executable binary name as an argument to virtualenv.

    virtualenv --python=python3.3 shortur

Move into your new, virtual home and activate it (which means subsequent invocations of python and python relevant paths will point within our environment):

    cd shortur
    source bin/activate

Your prompt should now show you the name of your current virtualenv:

    (shortur)mats@inc:~/Projects/shortur$

Install pyramid:

    pip install pyramid

Clone the Shortur repository:

    git clone git@github.com:Derdubor/Shortur.git

Move into repository and let pyramid do it magic by installing all dependencies:

    cd Shortur
    python setup.py develop

This might take a while. When finished, let SQLAlchemy create the tables used to store url metadata and lookup statistics. By default this will be stored in an sqlite database named "Shortur.sqlite" in the project directory. You can change to another database by changing the SQLAlchemy connection string in development.ini and production.ini.

    initialize_Shortur_db development.ini       (or use production.ini - by default these connection strings are identical)

Start the application in development mode by running:

    pserve --reload development.ini

The --reload parameter will monitor the file system for changes and reload the appropriate parts of your application as a file is updated on disk.

The application should now be available through localhost at: 

    http://localhost:6543/

For production use we've gone the easiest way, the production.ini file will load the application at port 5000, and we let waitress serve all requests (there are no external dependencies at the current time, no static files) through a frontend server (Apache with mod_proxy, nginx, etc.). The main difference between development.ini and production.ini is that the latter does not load the pyramid debug toolbar.

