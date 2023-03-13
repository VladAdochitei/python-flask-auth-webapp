# Python Flask Authentication Application
This handbook will cover documentation regarding Web Application Authentication with Flask-Login.

------------------------
## Contents
- [0. Introduction](#0-introduction)
- [1. Prerequisites](#1-prerequisites)
    - [1.1. Installing packages](#11-installing-packages)
    - [1.2. The main app file](#12-the-main-app-file)
    - [1.3. Add routes](#13-add-routes)
        - [1.3.1. Main routes](#131-main-routes)
        - [1.3.2. Auth rotes](#132-auth-routes)
- [2. Templates](#2-templates)
    - [2.1. Template base.html](#21-template-basehtml)
    - [2.2. Template index.html](#22-template-indexhtml)
    - [2.3. Template login.html](#23-template-loginhtml)
    - [2.4. Template signup.html](#24-template-signuphtml)
    - [2.5. Template profile.html](#25-template-profilehtml)
    - [2.6. Add template rendering to backend](#26-add-template-rendering-to-backend)
    - [2.7. Review templates integration](#27-review-templates-integration)
- [3. Create database user model](#3-create-database-user-model)
- [4. Database configuration](#4-database-configuration)
- [5. Setting up the authorization function](#5-setting-up-the-authorization-function)
    - [5.1. Testing the sign-up method and add flashing messages](#51-testing-the-sign-up-method-and-add-flashing-messages)
    



------------------------

## 0. Introduction
Allowing users to log in the web application is one of the most common features that a web application must accomodate. Authentication features within a Flask Web Application can be added with the *Flask-Login* package

This implementation will cover:
- Use Flask-Login library for session management
- Use the built-in Flask utility for hashing passwords
- Add protected pages to the app for logged users only
- Create sign-up and login forms for the users to create accounts and log in
- Flask error messages back to users to create accounts and log in
- Flask error messages back to users when something goes wrong
- Use information from the user's account to display on the profile page

The web application will be comprised of a sign-up and login page that allow users to log in and access protected pages. Information from the `User` model will be used and displayed on the protected pages when the user logs in to simulate what a profile will look like.

> This implementation is limited in scope and does not cover advanced persisting of sessions. Furthermore, modifying the data type for the primary key or considerations for migrating to different database systems are also outside the scope of this implementation.

<br>

## 1. Prerequisites
First we will have to define the file structure of our project:

```
.
└── flask_auth_app
    └── project
        ├── __init__.py       # setup the app
        ├── auth.py           # the auth routes for the app
        ├── db.sqlite         # the database
        ├── main.py           # the non-auth routes for the app
        ├── models.py         # the user model
        └── templates
            ├── base.html     # contains common layout and links
            ├── index.html    # show the home page
            ├── login.html    # show the login form
            ├── profile.html  # show the profile page
            └── signup.html   # show the signup form
```

This web application was verified with the following packages:
- sqlite3 v3.36.0
- python v3.9.8
- flask v2.0.2
- flask-login v0.5.0
- flask-sqlalchemy v2.5.1.


Packages can also be reviewed on:
> [requirements.txt](./requirements.txt)

### 1.1. Installing packages
There are three main packages that are going to be needed in the project:
- Flask
- Flask-login
- Flask-SQLAlchemy

SQLite will be used to avoid the need of additional dependencies to handle database connections.

Enter the project directory:

```sh
cd flask-app-web-auth
```

Next, create a virtual environment to handle the requirements of this project:

```sh
python3 -m venv virtualenv
```

Make sure to not upload this file to git, since it is pretty large and not that useful.

Activate the virtual environment:

```sh
source virtualenv/bin/activate
```

Now install the requirements with the command:

```sh
pip install -r ./project/requirements.txt
```

You can always exit a virtual environment with the command:

```sh
deactivate
```

### 1.2. The main app file
This web application will use the Flask App factory pattern with blueprints. One blueprint handles the regular routes, which include the index and the protected profile page. Another blueprint handles everything authentication-related. In a real app, the functionality can be broken into any way desired, but the solution covered in this document will work well for this tutorial.

This file will have the function to create the app, which will initialize the database and register the blueprints. At the moment, this will not do much, but it will be needed for the rest of the app.

The main file is `__init__.py` and its purposes are mainly to:
- initialize SQLAlchemy,
- set some configuration values, and 
- register the blueprints.

The `__init__.py` file:

```py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy so it can be used in the Models
db = SQLAlchemy()

def create_app:
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'iuhjkl123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    # Blueprints for auth routes in the app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Blueprints for non-auth parts of the app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
```

### 1.3. Add routes
The two **blueprints** previousely defined will be used for the **routes**.

#### 1.3.1. Main routes
For the `main_blueprint`, there will be two routes, rendering two webpages:
- home page (`/`)
- profile page (`/profile`)

Add the `main_blueprint` in the `main.py` file:

```py
from flask import Blueprint
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return 'index'

@main.route('/profile')
def profile():
    return 'Profile'
```

#### 1.3.2. Auth routes
For the `auth_blueprint`, the routes will render retrieve several webpages:
- login page (`/login`)
- signup page (`/signup`)
- logout page (`/logout`)

Add the `auth_blueprint` in the `auth.py` file:

```py
from flask import Blueprint
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return 'Login'

@auth.route('/signup')
def signup():
    return 'Signup'

@auth.route('/logout')
def logout():
    return 'Logout'
```

For the time being, the `login`, `signup`, and `logout` routes will only return text. Additional routes will need to be configured for handling the `POST` requests from `login` and `signup`. This section of the code will be updated at a future point, so it will handle all the required functionalities.

Export the `FLASK_APP` and `FLASK_DEBUG` variable values in a terminal:

```sh
export FLASK_APP=project
export FLASK_DEBUG=1
```

The `FLASK_APP` environment variable instructs Flask on how to load the app. This is required to point to where `create_app` function is located. In this implementation, the variable will point to the `project` directory.

The `FLASK_DEBUG` envirnment variable is enabled by setting it to `1`. This will enable a debugger that will display the application errors in the browser.

Ensure that you are in the `flask-app-web-auth` directory and un the project:

```sh
flask run
```

At this point the application should work, but its current setup is very limited. It should only return the name of the route when navigating towards it.

![flask-app-initial](./flask-app-web-auth/assets/images/01-flask-app.png)

<br>

## 2. Templates
In this section the templates used by the application are created and described. This step is necessary before you can implement the actual login functionality of the application.

The web app will have four templates:
- `index.html`
- `profile.html`
- `login.html`
- `signup.html`

### 2.1. Template base.html
It will also have a `base.html` template that will have code common to each of the webpages. In this case, the base template will have navigation links and the general layout of the page.

Add the following code to the `base.html` template:

```html
<!DOCTYPE html>

<html>

    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Flask Authentication Web Application</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.2/css/bulma.min.css" />
    </head>

    <body>
        <section class="hero is-primary is-fullheight">

        <div class="hero-head">
            <nav class="navbar">
                <div class="container">
                    <div id="navbarMenuHeroA" class="navbar-menu">
                        <div class="navbar-end">
                            <a href="{{ url_for('main.index') }}" class="navbar-item">
                                Home
                            </a>
                            <a href="{{ url_for('main.profile') }}" class="navbar-item">
                                Profile
                            </a>
                            <a href="{{ url_for('auth.login') }}" class="navbar-item">
                                Login
                            </a>
                            <a href="{{ url_for('auth.signup') }}" class="navbar-item">
                                Sign Up
                            </a>
                            <a href="{{ url_for('auth.logout') }}" class="navbar-item">
                                Logout
                            </a>
                        </div>
                    </div>
                </div>
            </nav>
        </div>

            <div class="hero-body">
                <div class="container has-text-centered">
                    {% block content %}
                    {% endblock %}
                </div>
            </div>
        </section>
    
    </body>

</html>
```

This code will create a series of menu links to each page of the application. It also establishes a block for `content` that can be written by child templates.

> **Note**: This tutorial uses [Bulma](https://bulma.io/) framework to handle styling and layout.


### 2.2. Template index.html
After the `base.html` template is configured we can start working on the other ones, thus `index.html`:

```html
{% extends "base.html" %}

{% block content %}
<h1 class="title">
    Flask Login Web App
</h1>

<h2 class="subtitle">
    Easy authentication and authorization in Flask.
</h2>

{% endblock %}
```

The above code will create a base index page with a simple title and subtitle.

### 2.3. Template login.html
This code generates a login page with fields for **Email** and **Password**. There is also a checkbox to *remember* a logged in session.

Template `login.html`:

```html
{% extends "base.html" %}

{% block content %}
<div class="column is-4 is-offset-4">
    <h3 class="title">Login</h3>
    <div class="box">
        <form method="POST" action="/login">
            <div class="field">
                <div class="control">
                    <input class="input is-large" type="email" placeholder="Your Email" autofocus="">
                </div>
            </div>

            <div class="field">
                <div class="control">
                    <input class="input is-large" type="password" name="password" placeholder="Your Password">
                </div>
            </div>

            <div class="field">
                <label class="checkbox">
                    <input type="checkbox" name="remember">
                    Remember me
                </label>
            </div>

            <button class="button is-block is-info is-large is-fullwidth">Login</button>
       
       </form>
    </div>
</div>
{% endblock %}
```

### 2.4. Template signup.html
The `signup.html` template acts as a sign-up page and has the following fields:
- `email`
- `name`
- `password`

```html
{% extends "base.html" %}

{% block content %}
<div class="column is-4 is-offset-4">
    <h3 class="title">Sign Up</h3>
    <div class="box">
        <form method="POST" action="/signup">
            <div class="field">
                <div class="control">
                    <input class="input is-large" type="email" name="email" placeholder="Email" autofocus="">
                </div>
            </div>

            <div class="field">
                <div class="control">
                    <input class="input is-large" type="text" name="name" placeholder="Name" autofocus="">
                </div>
            </div>

            <div class="field">
                <div class="control">
                    <input class="input is-large" type="password" name="password" placeholder="Password">
                </div>
            </div>

            <button class="button is-block is-info is-large is-fullwidth">Sign Up</button>
        </form>
    </div>
</div>
{% endblock %}
```

### 2.5. Template profile.html
This webpage is used to welcome the user. At the moment its name will be hardcoded into **Vlad**, thus `profile.html`:

```html
{% extends "base.html" %}

{% block content %}
<h1 class="title">
  Welcome, Vlad!
</h1>
{% endblock %}
```

This section will be revisited to dynamically greet any user logged in.


### 2.6. Add template rendering to backend
Once the templates have been added, you can update the return statements in each of the routes to return the templates instead of the placeholder text as shown in the previous snapshot (from section 1.3).

Updated `main.py` file:

```py
from flask import Blueprint, render_template
...
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
def profile():
    return render_template('profile.html')
```

Updated `auth.py`:

```py
from flask import Blueprint, render_template
...
@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

# We won't touch this one yet
@auth.route('/logout')
def logout():
    return 'Logout'
```

The `/logout` route will not display a template at this point and its functionality will be implemented at a later point.

### 2.7. Review templates integration
After the templates are populated and bound to their routes, the application will look something like this:

Home page:

![index](./flask-app-web-auth/assets/images/02-flask-web-auth.png)

Login page:

![login](./flask-app-web-auth/assets/images/03-flask-web-auth.png)

Signup page:

![signup](./flask-app-web-auth/assets/images/04-flask-web-auth.png)

Profile page:

![profile](./flask-app-web-auth/assets/images/05-flask-web-auth.png)

Logout page:

![logout](./flask-app-web-auth/assets/images/06-flask-web-auth.png)


<br>

## 3. Create Database User Model
The user model represents what it means for the web application to have a user. This web application will require fields for:
- email
- password
- name

In more complex web applications, there's a high chance that more information must be stored per user. This can be added subsequently into the User model. Examples of additional information can be birthdays, profile pictures, locations, or any other data.

***Models*** created in **Flask-SQLAlchemy** are represented by calsses that then translate to *tables* in a database. The attributes of those classes then turn into *columns for those tables*.

In the `models.py` file, define the `User` model:

```py
from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) #Primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
```

This code defines a `User` with columns for:
- `id`
- `email`
- `password`
- `name`

Now that the `User` model was created, the database can be configured.

<br>

## 4. Database configuration
You will be using an ***SQLite*** database. **SQLite** databases can be created without the implication of **SQLAlchemy**, but it is easier to let that extension do it for you, it's less of a hassle. The database path is already specified in the `__init__.py` file, so the only remaining step is to tell **Flask-SQLALchemy** to create the database in the Python REPL (or run the `createdb.py`) script

Ensure that you are still in the virtual environment and in the `flask-app-web-auth` directory.

After the flask application is stopped, a Python REPL (Read, Print, Evaluate, Loop - Python terminal) 

```py
from project import db, create_app, models
db.create_all(app=create_app()) # pass the create_app result so Flask-SQLAlchemy gets the configuration.
```

If this does not work, run the createdb.py script.

You will now see a `db.sqlite` file in your project directory. This database will have the ***user table*** in it.

<br>

## 5. Setting up the Authorization Function
For the sign-up function, you will take the data the user submits to the form and add it to the database. There are some checks that are necessary for this mechanism so work. You will need to make sure a user with the same email addres does not already exist in the database. If it does not exist, then you need to make sure you hash the password before placing it into the database

> **Note:** Storing passwords in plaintext is considered a foor security practice. You will generally want a complex *hashing algorithm* and *salt* to keep the passwords secure.

Let's add a second function to handle the `POST` form data. Gather the data passedfrom the user.

Update `auth.py` by modifying the import line and implementing `signup_post`:

```py
from flask import Blueprint, render_template, redirect, url_for
...
@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    return redirect(url_for('auth.login'))
```

Create the function and add a redirect. This will provide a user experience of a successful sign-up and being redirected to the Login Page.

Now let's add the rest of the code necessary for signing up a user. Use the request object to get the form data. 

Continue to update `auth.py` by adding imports and implementing `signup_post`:

```py
from flask import Blueprint, render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
...
@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))
```

This code will check to see if a user with the same email address exists in the database, and based on this will either reload the signup page or create a new user.

### 5.1. Testing the Sign-Up Method and add flashing messages
Now that the sign-up method is integrated, you will be able to create a new user. Let's test the form to create an user.

There are two ways you can verify if the sign-up was successful:
- You can use the database viewer to look at the row that was added to your table.
- Or you can try signing up with the same email address again, and if you get an error, you know the first email was saved properly.

Let's add code to let the user know the email already exists and direct them to go to the login page. By calling the `flash` function, you can send a message to the new request, which in this case is the redirect. The page the user is redirected to will then have access to that message in the template.

First, add the `flask` before you redirect to the sign-up page.

Code in `auth.py` file:

```py
from flask import Blueprint, render_template, redirect, url_for, request, flask
...
@auth.route('/signup', methods=['POST'])
def signup_post():
    ...
    if user: # if a user is found, we want to redirect back to signup page so user can try again and also add a flask message
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
```

To get the flashed message in the template, you can add this code before the form.

Code in `signup.html` file:

```html
...
{% with messages = get_flashed_messages() %}
{% if messages %}
    <div class = "notification is-danger">
        {{ messages[0] }}. Go to <a href = "{{ url_for('auth.login') }}">login page</a>.
    </div>
{% endif %}
{{% endwith %}}
<form method="POST" action="/signup">
``` 

At this point, you can run the application and attempt to sign up with an email address that already exists.

![failed register attempt](./flask-app-web-auth/assets/images/07-flask-web-auth.png)

### 5.2. Adding the Login Method
the login method is similar to the sign-up function. In this case, you will compare the `email` address entered to see if it is in the database. If so, you will test the `password` the user provided by hashing it (user provided password) and comparing it to the already hashed `password` in the database. You will know the user has entered the correct password when both hashed `passwords` match.

Once the user has passsed the password check, you will know that they have the correct credentials and you can log them in using **Flask-Login**. By calling `login_user`, **Flask-Login** will create a session for that user that will persist as the user stays logged in, which will allow the user to view protected pages.

You can start with a new route for handling the data submitted with `POST` and redirect to the profile page when the user successfully logs in:

 In `auth.py` file:

```py
...
@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    return redirect(url_for('main.profile'))
```

Now, implementing the credential check, in `auth.py` file:

```py
@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email = email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login credentials and try again.')
        return redirect(url_for(auth.login)) # if the user doesn't exist or password is wrong, reload the page
    
    # if the above check passses, then we know the user has the right credentials
    return redirect(url_for('main.profile'))
```

Let's add the block in the template so the user can see the flashed message:

In file `login.html`

```html
...

{% with messages = get_flashed_messages() %}
{% if messages %}
    <div class = "notification is-danger">
        {{ messages[0] }}
    </div>
{% endif %}
{% endwith %}
<form method="POST" action="/login">
```

You have the aility to say a user has logged in successfully, but there is nothing to log the user into.

**Flask-Login** can manage user sessions. Start by adding the `UserMixin` to your `User model`. The `UserMixin` will add ***Flask-Login*** attributes to the model so that **Flask-Login** will be able to work with it.

In file `models.py`:

```py
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
```

Then, you need to specify the `user loader`. A user loader tessl **Flask-Login** how to find a specific user from the ID that is stored in their session cookie. Add this in the `create_app` function along with `init` code for **Flask-Login**:

File `__init__.py`:

```py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
...

def create_app():
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, we are going to use it to query for the user
        return User.query.get(int(user_id))
```

Finally, add the `login_user` function before redirecting to the profile page to create the session. In file `auth.py`:

```py
from flask_login import login_user
from .models import User
from . import db
...

@auth.route('/login', methods=['POST'])
def login_post():
    ...
    # if the aboce check passes, then we know the user has the right credentials
    login_user(user, remember = remember)
    return redirect(url_for('main.profile'))
```

With **Flask-Login** setup, use the `/login` route. When everything is in place, you will see the profile page.

![profile page]() !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! to be added

At this point, you can run the application and attempt to log in.

<br>

## 6. Protecting webpages
The goal is for the profile page to display the name in the database. You will need to protect the page and then access the user's data to get the `name`.

To protect the page when using **Flask-Login**, add the `@login_required` decorator between the route and the function. This will prevent a user that is not logged in from seeing the route. If the user is not logged in, the user will get redirected to the login page, per the **Flask-Login** configuration.

With routes that are decorated with the `@login_required` decorator, you can use the `current_user` object inside of the function. This `current_user` represents the user from the database and provides access to all of the attributes of that user with *dot notation*. For example, `current_user.email`, `current_user.password`, `current_user.name`, and `current_user.id` will return the actual values stored in the database for the logged-in user.

Let's use the `name` of the `current_user` and send it to the template:

In the `main.py` file:

```py
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db
...
@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
```

Then in the `profile.html` file, update the page to display the `name` value:

```py
...
<h1 class="title">
  Welcome, {{ name }}!
</h1>
```

Once a user visits the profile page, they will be greeted by their `name`.

![picture]() !!!!!!!!!!!!!!!!!! to be added

## 7. Logout functionality
Now to update the logout view, call the `logout_user` function in a route for logging out:

In file `auth.py`:

```py
from flask_login import login_user, login_required, logout_user
...
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
```

In this particular case, you will need to use te `@login_required` decorator because it does not make sense to log out a user that is not logged in to begin with.

After a user logs out and tries to view the profile page again, they will be presented with an error message:

![pic]() !!!!!!!!!!!!!!! to be added

This is because ***Flask-Login*** flashes a message when the user is not allowed to access a page. One last thing to do is put `if` statements in the templates to display only the links relevant to the user:

In `base.html` file:

```py
...
<div class="navbar-end">
    <a href="{{ url_for('main.index') }}" class="navbar-item">
        Home
    </a>
    {% if current_user.is_authenticated %}
    <a href="{{ url_for('main.profile') }}" class="navbar-item">
        Profile
    </a>
    {% endif %}
    {% if not current_user.is_authenticated %}
    <a href="{{ url_for('auth.login') }}" class="navbar-item">
        Login
    </a>
    <a href="{{ url_for('auth.signup') }}" class="navbar-item">
        Sign Up
    </a>
    {% endif %}
    {% if current_user.is_authenticated %}
    <a href="{{ url_for('auth.logout') }}" class="navbar-item">
        Logout
    </a>
    {% endif %}
</div>
```

Before the user logs in, they will have the option to *log in* or *sign-up*:

![Picture]() !!!!!!!!!!! to be added

With that, you have successfully built your app with authentication.

## 8. Conclusion
In this handbook, *Flask-Login* and *Flask-SQLAlchemy* extensions were used to build a login system for a web application. You covered how to authenticate a user by first creating a user model and storing the user information. Then you had to verify the user's password was correct by hashing the password from the form and comparing it to the one stored in the database. Finally, you added authorization to the app by using `@login_required` decorator on a profile page so only logged in users can see that page.

What you created in this handbook will be sufficient for smaller apps, but if you wish to have more functionality from the beginning, you may want to consider using either Flask-User or Flask-Security libraries, which are both built on top of the Flask-Login library.