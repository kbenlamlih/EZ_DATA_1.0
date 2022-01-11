# EZ_DATA_1.0
# EZ DATA in a few words 

This repo is home to a django web-app designed to sizing photovoltaic cells.
The goal of this application is to digitalize the tool : "pré-configuration" used by Green Technologie commercials. 
 
The front end is a a form filled by the client about his identity and his energy consumption. 
This is what it looks like :
![alt text](https://github.com/kbenlamlih/EZ_DATA_1.0/blob/master/form1.png)
![alt text](https://github.com/kbenlamlih/EZ_DATA_1.0/blob/master/form2.png)
![alt text](https://github.com/kbenlamlih/EZ_DATA_1.0/blob/master/form3.png)


The app name for sizing the cells is PV. 

## Installation

Version of python : 3.7
Version of numpy : 1.18.3
Version of Django : 3.2.9

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the packages required of this project.
```bash
pip install django 
pip install git
pip install numpy
pip install matplotlib 
```
## Set up

Follow this tuto : https://docs.djangoproject.com/fr/2.2/intro/contributing/
To work on this repo you should clone it :

```bash
git clone git@github.com:kbenlamlih/EZ_DATA_1.0.git
```
## GITHUB 
Commandes GitHub à connaitre : 

https://www.hostinger.fr/tutoriels/commandes-git

## Models 
from Models.py
Each model is an object with attributes that is stored.
![alt text](https://github.com/kbenlamlih/EZ_DATA_1.0/blob/master/UML_EZ_DATA.png)

## Forms 
Forms.py 
using ModelForm to save the model attributes in the dataset.

## Back-End
Functions in files : dimens_centrale.py / solutions.py / mde.py / mobilite.py

## View
The link between back-end and front-end is the file view.py importing the solutions and displaying them in the templates.

The variables are renderered in a diccionary and used between brackets in the HTML files  {{ var }}.

##Front-End
All the CSS and HTML files are in the folder PV/static. 

Django uses templates that are in PV/templates.

Using Bootsrap and Chart.js 


## License
[MIT](https://choosealicense.com/licenses/mit/)
