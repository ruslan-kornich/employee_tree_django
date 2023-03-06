from django_seed import Seed

from app.models import Employee


def first_record():
    employee = Employee(
        full_name="Зінченко Лада Левівна",
        position="Генеральний директор",
        hire_date="2010-02-16",
        email="director@i.ua")
    employee.save()


def fill_up_data_base():
    seeder = Seed.seeder(locale='uk_UA')
    seeder.add_entity(Employee, 10, {
        'full_name': lambda x: seeder.faker.name(),
        'position': lambda x: seeder.faker.bs(),
        'hire_date': lambda x: seeder.faker.date(),
        'email': lambda x: seeder.faker.email(),

    })
    seeder.execute()
