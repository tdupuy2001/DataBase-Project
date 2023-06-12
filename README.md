# DataBase-Project
NTUA DataBase Project BOULNOIS-DUPUY (Erasmus students)

With the help of [Databases-Python-Demo](https://github.com/mkoniari/DBLAB---Databases-Python-Demo/tree/main) for the understanding of the front-end part.

## Dependencies

 - [MySQL](https://www.mysql.com/) for Windows
 - [Python](https://www.python.org/downloads/), with the additional libraries:
    - [Flask](https://flask.palletsprojects.com/en/2.0.x/)
    - [Flask-MySQLdb](https://flask-mysqldb.readthedocs.io/en/latest/)
    - [faker](https://faker.readthedocs.io/en/master/) (for data generation)
    - [Flask-WTForms](https://flask-wtf.readthedocs.io/en/1.0.x/install/) and [WTForms-validators](https://pypi.org/project/wtforms-validators/)

Use `pip install <package_name>` to install each individual Python package directly for the entire system or in a virtual environment.


## Project Structure

The package named "`projectDB`" contains the application's code and files, separated into folders for each category (Blueprints, HTML templates - views, static files such as css or images).

This package contains a `__init__.py` file which creates the application, connects the application to the database and imports all the routes. There is also a `routes.py` file where we create the home page (before the connection).

In this package, there are two Blueprints: "`login`" and "`sign-up`", each contains: 
    - an `__init__` file that initializes the Blueprint
    - a `routes.py` file with the relevant endpoints and corresponding controllers
    - a `forms.py`file with all the forms that the user will meet during his experience on the website
    
The "`sign-up`" file contains the sign-up page. In the "`login`" file, there are all the controllers after the connection (we could have built it differently).
All HTML templates are stored together in the `templates` folder.

The file `run.py` launches the simple, built-in server and runs the app on it.

All the project is linked with the database contained is the `database` folder. You can create it running the DDL file (for the database structure) on MySQL. You also must create views, procedures,triggers and events (in this order) on MySQL (all the files are contained in the `database` folder). The queries file contains all the queries of the project (queries at the end of the wording that are graded) but we also added other queries in the python files of the front-end to look like, as much as possible, a real Lbrary website.

Finally, you can populate the database using the DML file (the data have been created thanks to the python files contained in the `dummy_data` folder).


## Screenshots

Global landing
![global landing](https://github.com/tdupuy2001/DataBase-Project/assets/136317311/f7efc794-a2b0-4f04-b589-e58cdfd020c2)


Landing for teachers and students
![landing for teachers and students](https://github.com/tdupuy2001/DataBase-Project/assets/136317311/6323f583-82e4-4557-92b4-31962325fb17)


Landing for operator
![landing for operator]()


Landing for administrator
![landing for administrator](https://github.com/tdupuy2001/DataBase-Project/assets/136317311/67600e67-7ccb-4b9d-8d76-4f6686441e25)


