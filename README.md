
# Government Grant - TAP Meteor Assessment


## Assumptions
1. Multiple households of the same type can be added in the application
2. A unique person can only belong to one household
3. household_id is the primary key for households and is used to search for family members under a household
4. For the API listing all qualified households for each grant, households and family members can be qualified for multiple grants with no limits (e.g qualify for elder bonus + yolo gst grant).
5. For the API listing all qualified households for each grant, the following convention is to show all current grants. Within each grant is the qualified households and within each household contains the relevant qualified members. An example is shown below.
```
{
    "data": {
        "baby_sunshine_grant": {
                                <household_id 1>: [<list of qualified family members' details>],
                                <household_id 2>: [<list of qualified family members' details>]
                                },
        "elder_bonus":{....},
        "multigeneration_scheme": {...},
        "student_encouragement_bonus": {...},
        "yolo_gst_grant": {...}
    }
}
```
Example:
```
{
    "data": {
        "baby_sunshine_grant": {
            "1": [
                {
                    "annual_income": 0.0,
                    "dob": "Wed, 09 Jul 1997 00:00:00 GMT",
                    "gender": "male",
                    "household_id": 1,
                    "marital_status": "single",
                    "name": "dante1",
                    "occupation_type": "student",
                    "spouse": null
                }
            ],
            "2": [
                {
                    "annual_income": 0.0,
                    "dob": "Wed, 09 Jul 1997 00:00:00 GMT",
                    "gender": "male",
                    "household_id": 1,
                    "marital_status": "single",
                    "name": "dante2",
                    "occupation_type": "student",
                    "spouse": null
                }
            ]
        },
        "elder_bonus": {},
        "multigeneration_scheme": {},
        "student_encouragement_bonus": {},
        "yolo_gst_grant": {}
    }
}
```

## Notes
1. The application instance is hosted on heroku while the database is an AWS RDS MySQL database. Tech stack used for this application is Python Flask. Deployed application is in this link: https://tap-meteor-assessment.herokuapp.com/. To access API endpoints, please use the url pattern below for reference.
```
https://tap-meteor-assessment.herokuapp.com/api/<API Route>

Example: https://tap-meteor-assessment.herokuapp.com/api/get-all-households
```
2. As Heroku tends to switch off applications that are not in use frequently, please contact me through telegram(@danteliew6) if the above link does not work so that I can reboot the deployed application.
3. Postman collection can be found in this repository under "TAP Meteor Assessment.postman_collection.json". Please refer to it for the relevant endpoints and more information on how the APIs work. The standard request body for the REST APIs are in JSON format.
4. Unit Tests can be found under the "tests" folder. To setup unit tests, please follow the guide [here](#how-to-set-up-unit-tests).

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

## How to Set Up Unit Tests
### 1. Navigate into tests directory. In each test file, edit the following code line as shown below.
```
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://<DB_USERNAME>:<DB_PASSWORD>@<DB_ENDPOINT>:3306/<TEST_DB_SCHEMA>'

**Ensure test db schema is different from your actual db schema.
```

### 2. Create the Test DB Schema inside your MySQL DB.
As flask does not automatically create a DB schema for you, please create the schema manually.

### 3. Open a terminal in the home directory and enter the line below to run the unit tests
```
python -m unittest
```
<img width="545" alt="image" src="https://user-images.githubusercontent.com/61372973/178247149-007734a2-c53b-44f7-a030-850e61695908.png">

Alternatively, you may open Visual Studio Code and run the unit tests using the unittest extension.

