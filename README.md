
# WePark

A MVP Django web application to find parking spaces nearby. 






## About

Finding parking spaces in densely populated areas can be a challenge and this web application looks to reduce the size of the problem.

Parking spaces can be added, reviewed and discovered by people in nearby locations.

## Run Locally

Clone the project

~~~bash
git clone https://github.com/m4yow4f/WePark.git
~~~

Go to the project directory

~~~bash
cd WePark
~~~

Create and activate a virtual environment

**On macOS/Linux:**
~~~bash
python3 -m venv venv
source venv/bin/activate
~~~

**On Windows:**
~~~bash
python -m venv venv
venv\Scripts\activate
~~~

Install dependencies

~~~bash
pip install -r requirements.txt
~~~

Apply database migrations

~~~bash
python manage.py migrate
~~~

Start the development server

~~~bash
python manage.py runserver
~~~
