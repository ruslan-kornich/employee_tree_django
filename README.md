
## Tech Stack

The project is currently running on the:

Backend:
- Python
- Django
- django-mptt

Frontend:
- Bootstrap 
- Jquery

Test values for the database:
- django-seed 
- Faker 

## Running Locally

To run the project locally first you need to clone the repository:

```bash
https://github.com/ruslan-kornich/employee_tree_django.git
```

Create a virtualenv and activate:
```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```

Install the development requirements:
```bash
pip install -r requirements.txt
```
Populate the database with test values, it takes about 9 minutes:
```bash
python3 manage.py runscript -v3 my_seeder;
```
Run the local server:
```bash
python manage.py runserver
```