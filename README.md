# The Search For Herbs  
  
Welcome to The Search For Herbs game.  
This is a text based adventure game that is inspired by the 80’s popular RPG game “Dragon Quest”.  
  
The hero of this game is going to collect medicinal herbs for their sick sister by running, fighting or dealing with monsters outside of the village.   
    
## Live site
[Live site >> https://search-4-herbs-78b993bff664.herokuapp.com/](https://search-4-herbs-78b993bff664.herokuapp.com/)

# UX DESIGN  
  
## 1. Strategy Plane  
***Target users***  
1. Simply those who like to play games especially text based games.

***User value***  
1. This game is not difficult but has plenty of unexpected surprises. So any user can enjoy.
  
## 2. Scope Plane  
USER STORIES  
***First time visitor***  
* As a user, I want to clearly understand what is offered in this game.  
* As a user, I want to clearly understand how to play this game instinctively.  
* As a user, I want to see my results clearly.  

***Frequent visitor***  
* As a frequent visitor, I want to collect some rare items.
  
***The website owner stories***  
* As a site owner, I want to give users positive feelings to play games.

## 3. Structure Plane  
  
* The landing page should intuitively show what this game is offering.  
* The Code Institute provided the template to access the game program.  
  
***Algorithm planning***  
The game's main parts are the field loop and the battle loop. Before entering the loop, the game asks users for their names. After the game (end of the loop), it records the user's data to a Google spreadsheet.  
![Algorithm planning](readme/algorithm-plan.webp)  

# FEATURES  
  
## Existing Features  
  
**Title banner and Introduction**  
I couldn't use graphic images though I used the ASKII letters for the title banner.
Also I changed the lead paragraph to a simple short sentence to explain what this app is.  

**Name Input**  
It asks for the user's name which is used for the hero's name.
Validation requires more than 3 letters, any characters can be used, but not just numbers.  
![Title banner and Introduction](readme/feat-title.png "Title banner and Introduction")  

**Would you like to play?**  
Before this fantasy story begins, I wanted to give the user a little introduction, preparing for the fantasy setting. Then ask the player to play or not. If the user choose "No" then the loop stops for a while but won't exit until the user types "Yes".  
![Would you like to play?](readme/feat-play.png "Would you like to play?") 

**Story display**  
All the story sentences have 2 line breaks for readability.  
![Story display](readme/feat-story.png "Story display") 

 
**Field Loop**  
When the player enters the field loop, the field options appear and ask what the player's next action is. When player selects an action, there are four validations: first, validation for a valid key; next, validation of the map's range; then, a check to see if the location is in the Mountain or not; and finally, proceeding to the cardinal directions `if` statement. Each option calls the `field_event()` function, which sorts the Monsters list based on the location
and selects a Monster for the battle event to start.      

**Field Option**  
![Field Option](readme/feat-field-op.png "Field Option") 

**Hero and Monster Status**  
![Player's status](readme/feat-player-status.png "Player's status")![Monster's status](readme/feat-monster-status.png "Monster's status") 

**Map**  
This map uses player's location information in X, Y coordinates. I couldn't make an automatic position generator
so the Players have to find out their position by them-selves.
Although the map's readability isn't fantastic without graphics, it's not too bad once players get used to it.  
![Map](readme/feat-map.png "Map") 

**Battle first move and Battle loop**  
When encountering Monsters, they have the opportunity to choose their first action. After that, if the Monster doesn’t run away, the Battle_loop() function starts, and the Player can choose an action. This battle loop has one validation for a valid key, all of the actions have a success rate, so sometimes the attack fails and escape can fail too. After the battle event, the code checks the field achievement every time; If the Player has four herbs and the location (X Y) is (0, 0) (the village), an ending story and record() function is triggered.   

**Battle Option**  
![Battle Option](readme/feat-battle-op.png "Battle Option")  

**Function record()**  
After the player has cleared the game, the player's status information and the date are recorded in the Google Sheet. [CREDIT-> Function record()](#credit-record)   
![Function record()](readme/feat-record.png "Function record()")   

**Function get_players_data()**  
To meet the criteria of 'a working data model' and 'manipulate data,' I created a function that accesses the data and downloads the data of the top 5 players with the lowest moves.  
 
1. Get the `moves` column data.
2. Create a dictionary that includes the index number of the data as a "key".
3. Compare the values and retrieve the top 5 index numbers of the best data.
4. From there, it refers to the index numbers to download the complete data for the top 5 entries. 

The `moves` column data was in list format, so I searched for a way to convert it into a dictionary that includes the index numbers together.  
[CREDIT-> List into dictionary (tuple) - `enumerate`](#credit-lis-into-dic)   ![The `moves` culomms data](readme/credit-list-into-dic-index-1.png "The `moves` culomms data")    

After I had created the tuple (Not dictionary because the data was generated using `enumerate()`), I found the new `lambda` function and decided to use it.  
[CREDIT-> List into dictionary - `lambda`](#credit-lambda) 

## Future Features  

**Map**  
I'd like to include a function that generates the player's position on the map. That will help the player to use this map more easily.

**Heal HP and Level Up System**  
To make this game more interesting, adding HP healing option (e.g. medicine, or magic) and adding level up system might be useful.  

**Help button**  
Create a help page and having a link button on the page will help first time players.  

**Add events or functions**  
Add events or functions that use other collected items and tamed monsters. Those might enhance enjoyment.  

# TECHNOLOGY USED  
- [Python](https://www.python.org) used for all functionality. Programming language. 
- [Gitpod](https://gitpod.io) used as a cloud-based IDE for development.
- [Git](https://git-scm.com) used for recording changes. A version control system.
- [GitHub](https://github.com) Used for our project's platformused for secure online code storage.
- [Heroku](https://www.heroku.com) Used for our project's platform. The deployed site.  

# TESTING
> I performed most of the testing myself and had some support from family members with different mobile devices.   

**Testing for visual display**  
| Visual display | Outcome  |
|--|--|
| The title logo and lead texts are printed correctly | Pass |
| Some stories are printed with time control (slow) | Pass |
| The field option, battle option, status box, map show up | Pass |
| After the game, Top 5 best data is displayed | Pass |

**Testing for functionality**  
| Name input validation | Outcome |
|--|--|
| Alphabets, numbers, symbols can be accepted | Pass |
| Prevent less than 3 letters input. | Pass |
| Prevent only numbers input. (No alphabet nor numbers) | Pass |
| prevent empty value to proceed | Pass |
![Testing name input](readme/tes-name3.png "Testing name input") ![Testing name input](readme/tes-name1.png "Testing name input") ![Testing name input](readme/tes-name2.png "Testing name input")

| Start game input validation | Outcome |
|--|--|
| "Yes" "Y" "No" "N" lead to each functions | Pass |
| Prevent all the other keys, print warning. | Pass |
| prevent empty value to proceed | Pass |
![Testing - Start game - Yes or No](readme/tes-yes-no1.png "Testing - Start game - Yes or No") ![Testing - Start game - Yes or No](readme/tes-yes-no2.png "Testing - Start game - Yes or No")

| Field loop option - input validation | Outcome |
|--|--|
| "Status" shows the status box | Pass |
| "Map" shows the map with location X, Y | Pass |
| "North" / "N" "South" / "S" "East" / "E" "West" / "W" | Pass |
| Prevent all the other keys, print warning. | Pass |
| prevent empty value to proceed | Pass |
![Testing - Field option](readme/tes-field1.png "Testing - Field option") ![Testing - Field option](readme/tes-field2.png "Testing - Field option")

|Field loop - other validations | | Outcome |
|--|--|--|
| Map range validation | when player tries to go out side - alert & prevent the move | Pass |
| Northern Mountain | when player is in Northern Mountain position - special event | Pass |
| "North" / "N" | Add counters, lead to the battle event function | Pass |
| "South" / "S" | Add counters, lead to the battle event function | Pass |
| "East" / "E" | Add counters, lead to the battle event function | Pass |
| "West" / "W" | Add counters, lead to the battle event function | Pass |
| Sort monsters by living area zones | | Pass |
| Pick up monsters randomly by weight | | Pass |
| After the battle event | Validate field achievement (4 herbs and back to village) | Pass |
![Testing - Map validation](readme/tes-map-vali.png "Testing - Map validation")![Testing - North Mountain](readme/tes-north-mount.png "Testing - North Mountain")![Testing - Field Achievement - Achived](readme/tes-field-achi.png "Testing - Field Achievement - Achived")![Testing - Field Achievement - Not achived](readme/test-field-achi.png "Testing - Field Achievement - Not achived")
| Battle loop option input validation | Criteria | Outcome |
|--|--|--|
| "Attack"/"A" | "Monster's HP" > 0 leads continue, < 0 lead break the battle | Pass |
| "Run/"R" | Randomly success and fail | Pass |
| "Tame"/"T" | Randomly success and fail | Pass |
| "Surprise"/"S" | 3 options lead to break the battle, 1 option leads to continue | Pass |
| Prevent all the other keys, print warning. || Pass |
| prevent empty value to proceed || Pass |

| Recording the data and loading the best players data | Criteria | Outcome |
|--|--|--|
| Recording new data | Google spread sheet updating | Pass |
| Loading best 5 lowest moves players data | display | Pass |


| Future feature ?  | Outcome |
|--|--|
| Prevent to go outside of the map  | - |
| Find the Medicinal herb at mountain area | - |

**Code Institute - CI Python Linter**  
![Code Institute - CI Python Linter](readme/test-ci-linter.png "Code Institute - CI Python Linter")  


# BUGS
## The bug in the `pick_monster` function
On the map, there are mountains, woods, fields and water areas. And depending on the zone the monsters are different. To sort out monsters, I used if statement inside the `pick_monster` function. When I got this error, I completely forgot to add else statement to it. I was so lucky to find it coincidently though, I realised that I should test everything with all the options and possibilities.    
![The bug in the `pick_monster` function (1)](readme/bug-forget-else.png "The bug in the `pick_monster` function (1)")  
Solution:  
Add `else` statement  

![The bug in the `pick_monster` function (2)](readme/bug-forget-else-2.png "The bug in the `pick_monster` function (2)")

## Get instance by the variable that stores chosen instance name
Luckily, I could find the way to sort out the list of monsters which has specific value attribute smoothly. [CREDIT-> Find instance by value](#credit-ins)  
However, I needed to properly extract the chosen monster’s instance for battle function. While searching for the way, I found it might not possible to use the variable which stores monster’s name that I draw from the random pickup. Because it's not just string, it associated to specified instance. Some article says If it’s dictionary I might be able to use the variable as string keyword. So I searched how to make the dictionary from instances. And there are a lot of different ways, including using `__dict__` or `dic()` method. But this was not really successful because I didn’t really understand the class object itself. Some web pages explained that class objects have a lot of information. It became too complicated to use, there should have been a simpler way so finally I went back to the `@classmethod` to make another sort method.  
What I found from this was `Class` is "Object" so it's not that simple like variable as just stored texts.  

Solution:  
Make another `get_n` `@classmethod` 

## Refactor get instance by the variable
From the above bug report, I had two `@classmethods`. One is for randomly picking up monsters that needs only the name and the zone attributes, and the other is for handling battles. I found that my biggest mistake was that these methods were not practical at all. I thought there were two different purposes, even though they could be combined into a single method.  

Solution:  
Simplifyed to extract the instance 

## Add counter for dictionary items
When the player received items, I thought dictionary format is best though I couldn't figure it out which method is best to add items.  I tried `setdefault`, `update`. Those just swapped the value; couldn't count numbers.  
![Add counter for dictionary items (1)](readme/bug-add-count-dic-1.png "Add counter for dictionary items (1)")  
So I looked for another way using `get` and `update` or create a method (function) inside the Class object. But when I found this page I realised that I didn't need any method, simply reassigned it.  
![Add counter for dictionary items (3)](readme/bug-add-count-dic-3.png "Add counter for dictionary items (3)")  
![Add counter for dictionary items (4)](readme/bug-add-count-dic-4.png "Add counter for dictionary items (4)")  

To implement this I use `try` and `except` for incase of no key exist.  
![Add counter for dictionary items (2)](readme/bug-add-count-dic-2.png "Add counter for dictionary items (2)")  

Solution:  
Simply reassigned it with `try` and `except` statement  

## Do not use bare "except" 
I received this error message from the CI Python Linter. I thought it was no surprise to get the error, as I was using the `try-except` statement in a similar way to the `if` statement. I tried to add the `raise` error and catch at `except` also `else` statement but didn't work as I expected. After looking through the information, I assume the `try-except` statement is mainly used for situations involving user input to validate the input.   

![Do not use bare except (1)](readme/bug-bare-except-1.png "Do not use bare except (1)")  

Solution:  
Change to the `if` statement  
![Do not use bare except (2)](readme/bug-bare-except-2.png "Do not use bare except (2)")  

## Title Banner
Because this project doesn't focus on graphic, I wanted to add ASCII art. However I got the error of the "SyntaxWarning: invalid escape sequence '\/'"   
I couldn't find out how to avoid this error so I changed the ASCII art to not contain any `\/`.
![Bug title banner (1)](readme/bug-backslush-in-string-1.png "Bug title banner (1)")  

## Field achievement validation
I changed the if condition from using any() in a loop to checking for a specific number: 'Medicinal herb' > 3. I thought that if it wasn't true, the code would just continue, but I got a `KeyError`. Again, since "Medicinal herb" does not exist in the `player.items` dictionary, checking for the key's existence is important before doing anything. 

![Field achievement validation (1)](readme/bug-if-condition-achiev-1.png "Field achievement validation (1)")  

Solution:  
Add a check for if the `Key` exists before the purpose code  
![Field achievement validation (2)](readme/bug-if-condition-achiev-2.png "Field achievement validation (2)")  

## The bug after lost the game
When I was testing to purposefully lose the game, I found that the ending is not properly devided for completed version and lost version.  

Solution:  
Made a function lost_status() that shows the players score and get lid of the sentences related to completed version from the ending role.   
![The bug after lost the game](readme/bug-ending-display-lost.png "The bug after lost the game")

# DEPLOYMENT  
First, we make a new repository at GitHub. But that is not really suitable for python apps to deploy there, it suits for front-end web sites. So we should make an account for Heroku service to deploy it.  

## Preparation  

***Installing additional dependencies***  
This game app is using Google sheet to save user's data.
To access Google Cloud, we need to access Google API and create a new project and enable both Google Drive and Google Sheet API. Below are the instructions from Code Institute template document.  
> The first one we need is Google-oauth which will use creds.json file to setup the authentication to access Google Cloud. The second one is gspread that we use to access and update data in the spreadsheet. These packages are included in the standard Python library, simply command `pip3 install gspread google-auth`  

Or we can install this project's requirements using:
`pip3 install requirements.txt`  
If you want to check if pip is already installed or not, you can check the installed version in the terminal:
`pip3 --version`
If it is installed, you’ll see the version information. 
Pip is a Python Package Manager.  

We need this requirements.txt file for deployment with Heroku.  
Create this `Pip3 freeze > requirements.txt` and commit this change as "Add: requirement for deployment" then push to the GitHub.  
  
<hr>

***Creating Google API Credentials***  
This is how to get the credentials, based on the Code Institute template document.  
1. Access to Google Cloud, create a new project.  
2. Enable both Google Drive and Google Sheet API.  
3. Create new credentials for the new project with Editor setting.  
4. From "APIs and services", choose "Credentials", click the new mail address that has been created.  
![Google API Credencial (4)](readme/dep-googleapi-cred-1.png "Google API Credencial (4)")  
5. Choose "KEYS" from top navigations and "ADD KEY" drop down.  
6. Create new key. Key type is JSON, click "CREATE". Then the credential json file is automatically down loaded.  
![Google API Credencial (6)](readme/dep-googleapi-cred-2.png "Google API Credencial (6)")  

We use these credentials to access the spread sheet though we shouldn't push this confidential file to the GitHub. To prevent this file from being added to the stage, add this file name to the ".gitignore" file and update it.  
  
<hr>

***Creating the Heroku app***  
1. After we make our own account, select "New" in the top-right corner of drop down list in Dashboard page, and select "Create new app".  
![Heroku deployment (1)](readme/dep-heroku-1.png "Heroku deployment (1)")  

2. Decide the App name (it must be only lowercase letters, numbers and dashes), and then choose a region "Europe".
![Heroku deployment (2)](readme/dep-heroku-2.png "Heroku deployment (2)")  

3. Click the "Settings" to go Setting page.
![Heroku deployment (3)](readme/dep-heroku-3.png "Heroku deployment (3)")  

4. Goes to "Config Vars". 
We are using confidential credentials, so copy the contents of the credentials in json file and paste into the Config Variables. Also set the value of KEY to "PORT", and the value to "8000" then select add.
![Heroku deployment (4)](readme/dep-heroku-4.png "Heroku deployment (4)")  

5. Underneath "Config Vars" there is "Buildpacks". We will need to add two buildpacks.
(The order of the buildpacks is important)  

> 1. `heroku/python`
> 2. `heroku/nodejs`  
![Heroku deployment (5)](readme/dep-heroku-5.png "Heroku deployment (5)")  
  

## Deployment  

1. When Heroku setting is done, go to "Deploy" page.
![Heroku deployment (3)](readme/dep-heroku-3.png "Heroku deployment (3)")  

2. We are using GitHub so choose "Deployment method" "GitHub". 
And input repository's name to connect to it. 
![Heroku deployment (6)](readme/dep-heroku-6.png "Heroku deployment (6)")  

3. Underneath we can choose the options “Automatic deploys” and “Manual deploy”. I chose “Automatic deploys” but it didn’t provide me the new app’s URL. For me it worked so that it deployed automatically after I selected Manual Deploy, I did not have to click on “Automatic deploys” afterwards. 


## Forking  
>A fork is a new repository that shares code and visibility settings with the original “upstream” repository. Forks are often used to iterate on ideas or changes before they are proposed back to the upstream repository, such as in open source projects or when a user does not have write access to the upstream repository. [Quote from GitHub Docs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo)  

We can make a copy of someone's original repository on our GitHub account, so we can make changes without affecting the original repository.  

1. Locate the objective repository using my Github account (I can’t fork my own repository),
top-right of the Repository (not top of page) just right hand side of the repository title, click the "Fork" Button.  
![Forking (1)](readme/dep-fork-1.png "Forking (1)") 

2. Input available new repository name and click “Create fork”. Now there is a copy of the original repository in my own GitHub account.
![Forking (2)](readme/dep-fork-2.png "Forking (2)") <a id="credit-ins"></a>


# CREDITS
## Code References
### `isnumeric` Method
For my name input validation, I needed a method to check if the user input consists only of numbers.  
![ `isnumeric` Method](readme/credit-isnumeric-input-name.png " `isnumeric` Method")   

### Deepcopy 
To get a copy without affecting any of the original instances, I used a shallow copy in JavaScript for my PP2 project, though I found that it only copies the first level. If we need a complete copy, then the deep copy is the correct answer.    
![Deepcopy](readme/credit-deepcopy.png "Deepcopy")  

### Custom validation
`try` and `except` is useful for user input validation; however, what if I want to validate without raising any errors? I was writing with `if` statement; it was a long statement until I found this useful option.  
`if *** not in ["**", "**", "**"]` This works for my tuples, lists and dictionaries.
![Deepcopy](readme/credit-custom-validation.png "Deepcopy")  

### Find instance by value
These monsters' habitats are different; some of them live in the woods, while others are in the fields or mountains. I want to sort them by their specific class attributes. To make this possible, I will use a @classmethod, as referenced in an article on Stack Overflow.  
First, save all the instances in the list and using `@classmethod` to sort out by specific value. Then, randomly pick up instances by populations' weight.    
![Find instance by value](readme/credit-find-instance-by-value.png "Find instance by value")  

### Slow print use standard output `write` and `flush` 
In this kind of text based game, the effects of text display play an important role in user readability. I found this speed control function code first. However this time I couldn't understand why and how this work. So below are some researches about this.
![Slow print with speed controle - Stack Oveflow](readme/credit-slow-print-1.png "Slow print with speed controle  - Stack Oveflow")  

<details>
<summary>Same code structure but import sys - Stack Oveflow >> </summary>  

![Same code structure but import sys - Stack Oveflow](readme/credit-printing-slowly-1.png "Slow print - flush geeksforgeeks")
</details>  
<details>
<summary>More research about sys  >> </summary>  

![Slow print - research Sys - geeksforgeeks](readme/credit-printing-slowly-2.png "Slow print - flush geeksforgeeks")
</details> 
<details> 
<summary>More research about standard output write >> </summary>  

![Slow print - standard output write - geeksforgeeks](readme/credit-slow-print-geeksforgeeks-2.png "Slow print - standard output write - geeksforgeeks")
</details>  
<details> 
<summary>More research about standard output flush >> </summary>  

![Slow print - standard output flush - geeksforgeeks](readme/credit-slow-print-geeksforgeeks-1.png "Slow print - standard output flush - geeksforgeeks")
</details>  

### Get current time  
When recording player's data into Google sheet, I wanted to use useful Date() function like Java Script has. In python we have a `datetime` package, I implemented this into my `record()` function.  
`datetime.datetime.now()` - I got an error when using single `datetime.now()` I assume the first `datetime` is module name.
![Get current time -](readme/credit-datetime.png "Get current time -")   
These are the some format of the datetime object. I used `%x` and display like this `07/29/24`. 
![Get current time - W3School](readme/credit-datetime-2.png "Get current time - W3School")  
Also I got an another error when I used `str()` to this when exporting it by JSON; we need to convert into string.
![Get current time - W3School](readme/credit-datetime-3.png "Get current time - W3School")<a id="credit-lis-into-dic"></a>

### List into dictionary (tuple) with index no. - `enumerate`   
I found some different ways to achieve this though, this `enumerate` method is build-in function so I wanted to get used to it. Note:`enumerate` returns a `tuple` not dictionary.  
![List into tuple with index no. (1)](readme/credit-list-into-dic-index-2.png "List into tuple with index no. (1)")  
![List into tuple with index no. (2)](readme/credit-list-into-dic-index-3.png "List into tuple with index no. (2)")<a id="credit-lambda"></a>

### Using `lambda` anonymous function
To get lowest `moves` value from the dictionary, I tried to use `min()`. There
were `lambda` in some example code, I changed my mind to use `sorted()` there are `lambda` sample codes again. So learned about this fantastic function.
![Using lambda (1)](readme/credit-lambda-1.png "Using lambda (1)")  
![Using lambda (2)](readme/credit-lambda-2.png "Using lambda (2)")  
W3School's `Try it Yourself` space is really useful to try my code as well. When I checked whether my code was working or not, I have to play and clear the game to reach to the `record()` function. Here I could try `enumerate` and `lambda` together. Below screen-shot shows that I got the sorted tuple data. Underneath is getting the index numbers of the top 5.
![Using lambda (3)](readme/credit-lambda-3.png "Using lambda (3)")  
![Using lambda (4)](readme/credit-lambda-4.png "Using lambda (4)")<a id="credit-record"></a>  

### Function record()
This part I referred to from Code Institute's walkthrough project 'Love Sandwich' to learn how to connect to Google Drive and Google Sheets, as well as how to handle the data in the spreadsheet. 

## Content References
* Code Institute Learning Material
> [Link to Code Institute Full-Stack Software Development Program](https://codeinstitute.net/?nab=0 "Code Institute Full-Stack Software Development Program")

* Text to ASCII Art Generator - patorjk.com
> [ASKII letter art](https://www.patorjk.com/software/taag/#p=display&f=Thick&t=The%20Search%20For%20Herbs "ASKII letter art")
Thick by Randall Ransom 2/94

* W3schools
> Used to research codes

* GeeksforGeeks
> Used to research codes

* stackoverflow
> Used to research codes

* perplexity
> Used for general questions


## Editing and Proofreading
Since I am not a native English speaker, my family assisted me with editing and proofreading.
 [ACKNOWLEDGEMENTS](#acknowledgements)  


# ACKNOWLEDGEMENTS  

I would like to give great thanks to my mentor Alan Bushell for his exellent advice and support.  
Also my cohort facilitator Amy Richardson for all the support and assistance.  

During this project's submission period I needed to go back home to support my family. The Student Care team supported and worked with me, thank you so much.

And also thanks to my family Sean Coffey and Dean Coffey for all the support.
