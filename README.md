# Udacity FSND Capstone Project

I hope with this project to gather all the knowledge acquired during the course, serving as a basis for the creation of new applications.


## URL location for the hosted API

The public URL preview can be accessed from the link below:

[https://udacity-fsnd-final.herokuapp.com/ ](https://udacity-fsnd-final.herokuapp.com/)
>See API and RBAC section to navigate through endpoints with the necessary permissions


## Getting started

[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository](https://github.com/bsalbuquerque/udacity-fsnd-final) and [Clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine.

### 1. Install Dependencies

- **Python 3.9** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/index.html)
- **Postgres** - The application uses PostgreSQL as a database. Download and set up [postgresql](https://www.postgresql.org/download/) version according to your operating system.
- **Virtual Environment** - I recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
- **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies running:

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.


### 2. Set up Environment Variables
Once have installed Python, Virtual Environment and all dependencies, you need to setup  environment variables, running the command bellow in the main folder:
```bash
## Mac OS
source setup.sh

## Linux
chmod +x setup.sh
./setup.sh
```

### 3. Database and Migrations
Once you have PostgreSQL installed, you will need to create the project database, called `fsnd`, by running the command below in your terminal:
```bash
createdb fsnd
```

To populate the database with the appropriate tables, you will use Flask Migrations to capture the models. In the terminal, go to the folder `/src` and run:
```bash
python3 -m flask db init
python3 -m flask db migrate
python3 -m flask db upgrade
```


### 4. Running the server locally
The final step is to run the application on your local machine. In the `/src` folder, run:
```bash
python3 -m flask run
```


## API and RBAC documentation

In this section I have separated the information necessary to understand the existing routes, the authentication system and the permissions based on each access profile.

### 1. Auth0
The RBAC system used was Auth0.
After [logging in](https://udc-casting-agency.us.auth0.com/authorize?audience=udc-casting-agency&response_type=token&client_id=vVWeqVYEyKA7MQwXvQwgAIYZqwkXxLEd&redirect_uri=http://127.0.0.1/) a JWT Token is generated with all the permissions assigned to the user role to access each endpoint.

For this project, I used three roles called Assistant, Director and Producer. Producer has all necessary permissions to access all available endpoints, and I have set a JWT Token in the environment variable for `unittest` all routes, called `JWT_TOKEN_PRODUCER`.

### 2. API Documentation
The API is separated by two entities: `actors`, `movies`.

#### Error Handlers
```
400
Bad request
Error type: Server was unable to process because a malformated request

401
Unauthorized
Error type: Server was unable to proccess because a missed or an invalid credentials

403
Forbidden
Error type: Server cannot proccess the request because an insufficient permission

404
Resource not found
Error type: Server was unable to find what was requested

405
Method not allowed
Error type: Server has rejected the specific method used

422
Unprocessable
Error type: Server was unable to process the contained instructions
```


#### Resource Endpoint library
```
Endpoints

- Actors
GET '/actors'
GET '/actors/{id}'
POST '/actors'
DELETE '/actors/{id}'
PATCH '/actors/{id}'

- Movies
GET '/movies'
GET '/movies/{id}'
POST '/movies'
DELETE '/movies/{id}'
PATCH '/movies/{id}'

NOTES: 
To test PATCH, each entity has the 'name' body parameter.
Each endpoint has its own permissions (See RBAC documentation below)
```


### 3. RBAC Documentation
Here's the permission and role list.

I recommend using [Postman](https://postman.com) to import the postman collection `udacity-fsnd-final.postman_collection.json` located in the main repository folder to test each endpoint with the appropriate role. Each role is separated by folder and contains its respective JWT Token.

#### Permissions
- `get:actors`
- `post:actors`
- `delete:actors`
- `patch:actors`
- `get:movies`
- `post:movies`
- `delete:movies`
- `patch:movies`

#### Roles
- Assistant
  - Can `get:actors` and `get:movies`

- Director
  - Can perform Assistant actions;
  - Can `post:actors`, `delete:actors`, `patch:actors` and `patch:movies`

- Producer
  - Can perform Director actions;
  - Can `post:movies` and `delete:movies`


## Unittest endpoints
In the `/src` folder run the following command:
```bash
python3 app_test.py
```
JWT Token is stored as local env called `JWT_TOKEN_PRODUCER`.

The database is reset with each new command execution.


## Author
Bruno Souza Albuquerque ([Github](https://github.com/bsalbuquerque))