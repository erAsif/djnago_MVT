# djnago_MVT
mvt archetecture  --   model form view templates urls

# create environment
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows

# install django
pip install django

# create project
django-admin startproject django_project
cd django_project

# create app
python manage.py startapp accounts

# requirements.txt
pip freeze > requirements.txt

# run server
python manage.py runserver

# create superuser
python manage.py createsuperuser

# migrate
python manage.py makemigrations
python manage.py migrate

# MVT
# Model - database structure (ORM) 
yeh class hoti hai jo database table ko represent karti hai
# View - business logic (Python functions/classes) 
jo request handle karti hai aur response return karti hai
# Template - presentation logic (HTML with Django template language)    
yeh file hoti hai jo data ko HTML format mein display karti hai
# URL - route requests to views (urls.py) 
yeh file hoti hai jo URL patterns define karti hai aur unhe views se map karti hai
# form - user input handling (forms.py) 
yeh file hoti hai jo user input ko validate karti hai aur form fields define karti hai

# git commands
git init
git add .
git commit -m "Initial commit"
git remote add origin <repository_url>
git push -u origin master

# git clone
git clone [<repository_url>](https://github.com/erAsif/djnago_MVT.git)
