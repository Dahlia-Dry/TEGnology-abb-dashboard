# TEGnology data dashboard
This is a [Dash](https://dash.plotly.com/)-based graphical user interface for displaying live demo data from sensors powered by TEGnology devices. It is hosted on [Heroku](https://heroku.com) via this GitHub repository. 

## How to modify this dashboard
Prerequisites: A GitHub account, a Heroku account, and python >= 3.11
### I. Installing on local machine
1. Open a terminal window and clone this repository to your local machine: ```git clone https://github.com/Dahlia-Dry/TEGnology-dashboard.git```
2. Navigate to the root directory of this repository (the folder containing this README).
3. Create a new virtual environment: ```python -m venv .venv/```
4. Activate the new virtual environment: ```source .venv/bin/activate```
5. Install dependencies: ```pip install -r requirements.txt```
### II. Modifying python code
You can view the dashboard on a local server by running ```python dashboard.py``` and pasting the port address printed to the terminal into your browser. 
- dashboard.py is the main file and contains the callbacks and Dash app object; modify behavior of dynamic components here.
- dashboard_layout.py contains the html layout of the dashboard; add/delete dynamic components here.
- assets/ contains all static files that are loaded into dashboard_layout.py. Add images,videos, and text files you wish to display here.
### III. Deploying to web
1. Make sure you have a heroku account and have installed the [heroku command line interface](https://devcenter.heroku.com/articles/heroku-cli). Heroku will ask you to provide payment information to verify your account, but as long as the app does not get much traffic and is not very large in size it is free to host on the web.
2. Login to the Heroku CLI using ```heroku login``` and following the instructions in your browser.
3. If you have cloned this repository and are pushing to the same branch, the heroku app will already exist and you can skip this step. Otherwise, create a new repository in your GitHub account using ```git init``` and follow the standard procedure to do a first commit. Then, run ```heroku create``` to create a new app.
4. If you haven't already, commit and push any changes to your GitHub remote using ```git push```. Then, push to the heroku remote using ```git push heroku main```.
5. If all is well, you should be able to follow the url printed to the terminal to view the deployed app on the web!