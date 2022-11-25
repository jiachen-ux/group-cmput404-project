
# CMPUT404-Project-Social-Distribution

## [Application Website](https://team9-socialdistribution.herokuapp.com/)

## [API Documentation](https://team9-socialdistribution.herokuapp.com/swagger/schema/)

## Team members 
* jiachen2
* shovo
* yhu19
* hb2
* nusaibah

## Installation and local deployment instructions:

1. Clone repository `git clone https://github.com/jiachen-ux/group-cmput404-project.git
2. Move to project directory with cd group-cmput404-project
3. Create a virtual env with `virtualenv venv --python=python3` and activate it using `source venv/bin/activate`
4. Install requirements after cd group-cmput404-project with pip install -r requirements.txt
5. Run `python manage.py makemigrations` and `python manage.py migrate` to make migrations.
6. To run locally, run `python manage.py runserver` and view site on 127.0.0.1:8000/


## Model Names

* Author
* Followers
* Post
* Comment

## Architecture

* Backend: SQLite3 and Django
* Frontend: Bootstrapped CSS & HTML

## Deployment
Push to heroku using 
`
git push heroku main
`

Run your migrations, create a Superuser
`
heroku run --app team9-socialdistribution python SocialDistribution/manage.py migrate
heroku run --app team9-socialdistribution python SocialDistribution/manage.py createsuperuser
`
