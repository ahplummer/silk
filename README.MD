#Silk (Software Inventory List Kollector)
##Description
This is my attempt to build a CRUD tool to operate a bit more effectively in the management of collecting software inventory.

Furthermore, this tool will manage the evaluation of software based on:
* Technical Integrity
* Business Value

Together, these two dimensions make up the Gartner "TIME" model for software roadmapping and rationalization.

Currently, there is no reporting, no business logic, no fancy graphs, no cool tools;  this is merely a way to capture:
* Software titles:
    * Application roles
    * Technical Owners, Project Leads, etc.
    * Suite mapping
    * Costs
    * Related projects
    * Technical Integrity
    * Business Value
* Projects
* Business Goals, Objectives, Strategies, Tactics
* IT Services (for ITSM)

So - this software does two things:
1. Captures data.
2. Exports selected data into CSV format.

##Usage

1. This is Django / Python.  If you're unsure what this is, you may want to turn around now.
2. Generally, it's wise to stand up a VM, docker container, or minimally a virtualenv.
3. Ensure you have the minimal system requirements:
* >$apt-get install --assume-yes \
	python-dev mysql-client mysql-server supervisor libmysqlclient-dev \
	vim ntp bzip2 python-pip git-all libmysqlclient-dev libjpeg-dev \
	libfreetype6-dev libxft-dev python-pandas build-essential
* >$apt-get build-dep python-matplotlib
3. Do a 'pip install -r requirements.txt' to install all the python requirements
4. Instantiate the MySQL backend (using silkpass as password by default)
* >create database silk;
* >create user 'silkuser'@'localhost' identified by 'silkpass';
* >grant all privileges on *.* to 'silkuser'@'localhost';
5. Modify the './silkcode/silk/settings/development.py' with database information.
6. Run the server: 
* > python manage.py runserver 0.0.0.0:8000 --settings=silk.settings.development
7. Hit the address in your browser: http://localhost:8000/admin

 
##Roadmap
1. Further refine CSV output, as needed.
2. Further refine in TIME graph (XY ScatterPlot using MatPlotLab)
