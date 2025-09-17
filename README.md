# Welcome to CineArchive: A Personal Movie Database System

The objective of this project is to design and implement a logging system for their movies, backed by a reliable relational database. Specifically, the system aims to store and organize comprehensive information about each title, including metadata such as genre, rating, duration, release date, language, director, and main cast. It also aims to support accurate and efficient input and updates through SQL-based operations. It should also enable users to organize content by their viewing status and preferences.

It will allow users to record which titles they have watched or intend to watch, thereby enhancing their ability to plan and personalize their viewing experience. Additionally, the system will feature a basic recommendation mechanism based on the user’s viewing history to assist in content selection. Core technical goals include the development of a well-structured relational database, implementation of essential SQL scripts for data management, and integration of a user-facing application interface.



## Getting Started:
** BTW when you guys make changes/commit please add a summary of the changes u guys made for easier progress tracking and documentation. 

** To get started, i recommend making a virtual env by running `python -m venv venv` in the terminal then activating it. 
Windows: `venv\Scripts\activate` 
Mac: `source venv/bin/activate`
Then, run the CineArchive_requirement.bat file.

** Make sure to start an sql server on ur device. Here are the links [for Mac](https://youtu.be/ODA3rWfmzg8?si=Hpyy9UMTYXhx0AbV) and [for Windows](https://youtu.be/u96rVINbAUI?si=pKmJOFIRgz-LYiqm). Note that I haven't tested the one for Windows so you guys may have to figure that out urselves XD

** Create a database, either following the tutorial or by running this code in MySQL: `CREATE DATABASE cinearchive CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;`

** Then, follow the steps listed in the .env.example file

** Run this in the VSCode terminal: `mysql -u root -p --default-character-set=utf8mb4 CineArchive < dump.sql`
    NOTE: You guys will have to run this line everytime anyone else updates the database. Also, double check the file name and ensure that it's set to the latest vers.
    If you guys do make changes to the database, run this code in the VSCode terminal: `mysqldump -u root -p --routines CineArchive > CineArchive_dump#.sql`
    Don't replace old sql dump files (just to be safe, we can delete it later on), append and increment the # symbol with corresponding numbers.

** After following those steps, you should now be able to run the app.py file to start the flask server.

## Revisiting CineArchive TODO:
Ah sht, here we go again. Who's ready for round 2?

### All pages:
- [ ] The images uploaded to discord are no longer available so i rewrote it to use the ones in the static folder. Please check if i used the right photos in the right places im mostly guessing kek. 
- [ ] We dont actually have a page that tracks the movies watched?? only a watchlist? If we plan to make that a feature - Add a button for it in Home, make a new page for it, and code the sql functions
- [ ] Figure out how to implement the recommendation system and the accessibility features - or at the very least, implement placeholders for those functions

### Home page: 
- [ ] Search bar isn't working 
- [ ] The movie posters seem to be cycling thru the same ones? Maybe fix the randomizer on that
- [ ] Double check if the black gradient at the bottom half of the page is intended. If so, consider shortening it/adding flavor text
- [ ] The footer also seems oddly shaped maybe make it shorter as well 

### Watchlist page:
- [ ] The modal div containing the movie info isn't scrollable pls fix
- [ ] Change the fav button into a watched button that removes the movie from the watchlist and adds it to the watched list 

### Login and Register page:
- [ ] The logo isnt fully visible - maybe resize or check if im using the right file

### Movie page:
- [ ] Add a placeholder image for when the movie poster cant be fetched
- [ ] Add placeholders for everything here actually.
- [ ] Also troubleshoot the console errors loue, thanks loue


