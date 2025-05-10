# Welcome to CineArchive: A Personal Movie Database System

The objective of this project is to design and implement a logging system for their movies, backed by a reliable relational database. Specifically, the system aims to store and organize comprehensive information about each title, including metadata such as genre, rating, duration, release date, language, director, and main cast. It also aims to support accurate and efficient input and updates through SQL-based operations. It should also enable users to organize content by their viewing status and preferences.

It will allow users to record which titles they have watched or intend to watch, thereby enhancing their ability to plan and personalize their viewing experience. Additionally, the system will feature a basic recommendation mechanism based on the user’s viewing history to assist in content selection. Core technical goals include the development of a well-structured relational database, implementation of essential SQL scripts for data management, and integration of a user-facing application interface.



## DEV NOTES:
Hi guys idk what I'm doing but we ball XD
We'll need to be putting important information in this file pertaining to the requirements and instructions on getting the project to run on your pc in the area above. 
I'll also be adding a sort of TODO list below too.

05/01 - Made the prerequisite file stucture based on the tutorials, not at all functional, just trying to get the foundation for our project right. Don't try to run main.py it wont work XD

### Getting Started:
** BTW when you guys make changes/commit please add a summary of the changes u guys made for easier progress tracking and documentation. 

** To get started, i recommend making a virtual env by running `python -m venv venv` in the terminal then activating it. 
Windows: `venv\Scripts\activate` 
Mac: `source venv/bin/activate`
Then, run the CineArchive_requirement.bat file.

** Make sure to start an sql server on ur device. Here are the links [for Mac](https://youtu.be/ODA3rWfmzg8?si=Hpyy9UMTYXhx0AbV) and [for Windows](https://youtu.be/u96rVINbAUI?si=pKmJOFIRgz-LYiqm). Note that I haven't tested the one for Windows so you guys may have to figure that out urselves XD

** Create a database, either following the tutorial or by running this code in MySQL: `CREATE DATABASE cinearchive CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`

** Then, follow the steps listed in the .env.example file

** Run this in the VSCode terminal (replace the temp values ofc): `mysql -u your_mysql_username -p cinearchive < CineArchive_Flask/data/CineArchive_dump.sql`
    NOTE: You guys will have to run this line everytime anyone else updates the database. Also, double check the file name and ensure that it's set to the latest vers.
    If you guys do make changes to the database, run this code in the VSCode terminal: `mysqldump -u root -p --routines CineArchive > CineArchive_dump#.sql`
    Don't replace old sql dump files (just to be safe, we can delete it later on), append and increment the # symbol with corresponding numbers.

** After following those steps, you should now be able to run the app.py file to start the flask server.

### TODO:
Everything lmao jk I've just made the basic file stucture that we'll probably be using for our project. So everything else is on the table. Feel free to update as we go along:

** Create the views (the pages of our project) based on the [YT Flask tutorial](https://youtu.be/dam0GPOAvVI?si=ckB3nZ6AM8Zqutgt). 

** Create the html+css website templates for said views (again refer to that same vid)

** Basically, everything else front-end related

** Back-end is mostly done maybe? However, we are still missing that movie recomendation system.
