# The Search For Herbs  
  
Welcome to The Search For Herbs game.  
This is a text based adventure game that is inspired by 80’s popular RPG game “Dragon Quest”.  
  
<!-- Please enter your name ( the game hero’s name ) alphabet only, 3 or more letters-> input -> validation -->
The hero of this game is going to collect medicinal herbs for their sick sister at the outside of the village; where the animals and monsters exist. Running, fighting or dealing with monsters affects the hero’s status. When your health point (HP) became “0”, the game is over, so try to save your health.  
The goal of this game is to complete collecting more than 10 medicinal herbs and safely come back home to heal the hero’s sister.  
  
> This website is built for academic purpose only.
  
  
## Live site
[Live site >> https://atsukocoffey.github.io/search4herbs/](https://atsukocoffey.github.io/search4herbs/)

# UX DESIGN  
  
## 1. Strategy Plane  
### Target users  
1. Intended to target people who like text based games.

### User value
1.  
  
## 2. Scope Plane  
USER STORIES  
### First time visitor  
* As a user, I want to clearly understand what is offered on this website.  
* As a user, I want to clearly understand how to play this game instinktively.  
* As a user, I want to see my results clearly.  

### Frequent visitor  
  
### The website owner stories  
* As a site owner, I want to encourage users to play games.  
  

## 3. Structure Plane  
  
* The website should have a clear logo or header.
* The landing page should show what this site is offering intuitively.  
  
## 4. Skeleton Plane  

![Algorithm planning](readme/algorithm-plan.webp)  

# EXISTING FEATURES  
  
## Landing and name input  

#### Creating Google API Credentials  
Access to Google Cloud, create a new project. Enable both Google Drive and Google Sheet API. Create credentials with Editor setting.  
From APIs and services, choose Credentials, click the new mail address that has been created, choose KEYS from top navigations and ADD KEY drop dpwn, Create new key. Key type is JSON, click CREATE. Then the credential json file is automatically down loaded.  
  
#### Installing additional dependencies
The first one is Google-oauth which will use creds.json file to setup the authentication to access Google Cloud. The second one is gspread that we use to access and update data in the spreadsheet. These packages are included in the standard Python library, simply command `pip3 install gspread google-auth`



Welcome,

This is the Code Institute student template for deploying your third portfolio project, the Python command-line project. The last update to this file was: **May 14, 2024**

## Reminders

- Your code must be placed in the `run.py` file
- Your dependencies must be placed in the `requirements.txt` file
- Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

---

Happy coding!
