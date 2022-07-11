
# Government Grant - TAP Meteor Assessment


## Assumptions
1. 

## Notes
1. The application instance is hosted on heroku while the database is an AWS RDS MySQL database. Tech stack used for this application is Python Flask. Deployed application is in this link: https://tap-meteor-assessment.herokuapp.com/. To access API endpoints, please use the url pattern below for reference.
```
https://tap-meteor-assessment.herokuapp.com/api/<API URL>

Example: https://tap-meteor-assessment.herokuapp.com/api/get-all-households
```
2. As Heroku tends to switch off applications that are not in use frequently, please contact me through telegram(@danteliew6) if the above link does not work so that I can reboot the deployed application.
3. Postman collection can be found in this repository under "TAP Meteor Assessment.postman_collection.json". Please refer to it for the relevant endpoints and more information on how the APIs work.

## How to Set Up
### 1. After cloning repository, navigate to 'config.py' and edit the database configuration code line below

```
Do ensure that the DB Schema indicated is a valid schema as flask will not create the schema and will throw an error.

Without Password:
SQLALCHEMY_DATABASE_URI = environ.get('dbURL') or 'mysql+mysqlconnector://<DB_USERNAME>@<DB_ENDPOINT>:3306/<DB_SCHEMA>'

With Password:
SQLALCHEMY_DATABASE_URI = environ.get('dbURL') or 'mysql+mysqlconnector://<DB_USERNAME>:<DB_PASSWORD>@<DB_ENDPOINT>:3306/<DB_SCHEMA>'
```

### 2. Open a new terminal and run the following code below to set up the database
```
flask db stamp head
flask db migrate
flask db upgrade
```

### 3. Lastly, run this line of code to boot up your flask application
```
flask run
```
