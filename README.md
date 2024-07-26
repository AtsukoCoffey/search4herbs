# The Search For Herbs  
  
Welcome to The Search For Herbs game.  
This is a text based adventure game that is inspired by 80’s popular RPG game “Dragon Quest”.  
  
The hero of this game is going to collect medicinal herbs for their sick sister with running, fighting or dealing with monsters at the outside of the village.   
    
## Live site
[Live site >> https://search-4-herbs-78b993bff664.herokuapp.com/](https://search-4-herbs-78b993bff664.herokuapp.com/)

# UX DESIGN  
  
## 1. Strategy Plane  
***Target users***  
1. Simply who likes to play games specially text based games.

***User value***  
1. This game is not difficult but plenty of surporise and unexpectedness in the battle. So any user can enjoy a little bit.
  
## 2. Scope Plane  
USER STORIES  
***First time visitor***  
* As a user, I want to clearly understand what is offered on this website.  
* As a user, I want to clearly understand how to play this game instinctively.  
* As a user, I want to see my results clearly.  

***Frequent visitor***  
* As a Frequent visitor, I want to collect something rare items
  
***The website owner stories***  
* As a site owner, I want to give users positive feelings to play games.

## 3. Structure Plane  
  
* The landing page should show what this site is offering intuitively.  
* Code Institute's gave me the template for access the game program.
  
## 4. Skeleton Plane  

![Algorithm planning](readme/algorithm-plan.webp)  

***Algorithm planning***  
As the planning sheet, this game's main parts are the field loop and the battle loop. So before entering the loop ask users their names, and after the game (end the loop) record the user's data to google spread sheet. 


# FEATURES  
  
## Existing Features  
  
**Titile banner and Introduction**  
I couldn't use graphical material though I used the ASKII letter for the title banner.
Also I changed the lead paragraph to a simple short sentence for understanding what this app is.

**Name Input**  
It is asking user's name. It is used for the hero's name.
validation is setting more than 3 letter, any charactors can use but not only numbers.  

**Story Summary**  
Before this fantasy story has begun, I wanted to give the user a little mark time, a preparing for the fantasy setting.

**Play Input**  
This validation is asking the user to play or not. If User choose "No" then the loop stop for a while though, this loop won't be exit untill user type "Yes".  

**Field Loop**  
When player went into the field loop, the field option was showed up and asked what is the next player's action.   

**Field Option**  


**Status Window**  

**Map**  
This map uses player's location information X, Y. I counldn't make automatic position generator
so the Players have to find out their position by them selves.
Also without graphical material, I can't say the map's readability is fantastic though when player become get used to it, it's not so bad, I think.


## Future Features  

**Map**  
I'd like to have the function that generates the player's position on the map. That will help player to use this map more handy.

**Heal the HP and Level Up System**
For making this game more interesting, adding HP healing option (e.g. medicine, or magic) and adding level up system might be work.  

  


# TECHNOLOGY USED

# TESTING

# BUGS

# DEPLOYMENT  
First, we make a new repository at Git Hub. But that is not really suitable for python apps to deploy there, it suits for front-end web sites. So we should make an account for Heroku service to deploy it.  

## Preparation  

***Installing additional dependencies***  
This game app is using Google sheet to save user's data.
To access to Google Cloud, we need to access Google API and create a new project and enable both Google Drive and Google Sheet API. Below is the instraction sentences from Code Institute template document.  
> The first one we need is Google-oauth which will use creds.json file to setup the authentication to access Google Cloud. The second one is gspread that we use to access and update data in the spreadsheet. These packages are included in the standard Python library, simply command `pip3 install gspread google-auth`  

Or we can install this project's requirements using:
`pip3 install requirements.txt`  
If you want to check already pip is installed or not, you can check the installed version in the terminal:
`pip3 --version`
If it is installed, you’ll see the version information. 
Pip is a Python Package Manager.  

We need this requirements.txt file for deploy with Heroku.  
To create this `Pip3 freeze > requirements.txt` and commit this change as "Add: requirement for deployment" then push to the Git Hub.  
  
<hr>

***Creating Google API Credentials***  
This is how to get the credentials, based on the Code Institute template document.  
1. Access to Google Cloud, create a new project.  
2. Enable both Google Drive and Google Sheet API.  
3. Create new credentials for the new project with Editor setting.  
4. From "APIs and services", choose "Credentials", click the new mail address that has been created.  
![Google API Credencial (4)](readme/dep-googleapi-cred-1.png "Google API Credencial (4)")  
5. Choose "KEYS" from top navigations and "ADD KEY" drop dpwn  
6. Create new key. Key type is JSON, click "CREATE". Then the credential json file is automatically down loaded.  
![Google API Credencial (6)](readme/dep-googleapi-cred-2.png "Google API Credencial (6)")  

We use this credeincials to access the spread sheet though, we shouldn't push this to the Git Hub. For preventing this file to be added to the stage, add this file name to the ".gitignore" file and update it.  
  
<hr>

***Creating the Heroku app***
1. After we make our own account, select "New" in the top-right corner of drop down list in Dashboard page, and select "Create new app".  
![Heroku deployment (1)](readme/dep-heroku-1.png "Heroku deployment (1)")  

2. Decide the App name (it must be only lowercase letters, numbers and dashes), and then choose a region "Europe".
![Heroku deployment (2)](readme/dep-heroku-2.png "Heroku deployment (2)")  

3. Click the "Settings" to go Setting page.
![Heroku deployment (3)](readme/dep-heroku-3.png "Heroku deployment (3)")  

4. Goes to "Config Vars". 
We are using confidential credentials, so copy the contents of credentials in json file and past into the Config Variables. Also set the value of KEY to "PORT", and the value to "8000" then select add.
![Heroku deployment (4)](readme/dep-heroku-4.png "Heroku deployment (4)")  

5. Underneath of "Config Vars" there is "Buildpacks". We will need to add two buildpacks.
(The order of the buildpacks is important)  

> 1. `heroku/python`
> 2. `heroku/nodejs`  
![Heroku deployment (5)](readme/dep-heroku-5.png "Heroku deployment (5)")  
  

## Deployment  


## Forking  


# CREDITS

# ACKNOWLEDGEMENTS




When you create the app, you 

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

---

Happy coding!
