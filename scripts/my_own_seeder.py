import random
from django_seed import Seed
from faker import Faker

from app.models import Employee


def first_record():
    employee = Employee(
        full_name="Зінченко Лада Левівна",
        position="Генеральний директор",
        hire_date="2010-02-16",
        email="director@i.ua",
    )
    employee.save()


def fill_up_data_base(count, position, year, parent_min, parent_max):
    seeder = Seed.seeder("uk_UA")
    fake = Faker("uk_UA")
    seeder.add_entity(
        Employee,
        count,
        {
            "full_name": lambda x: fake.name(),
            "position": position,
            "hire_date": f"{year}-{random.randint(1, 12)}-{random.randint(1, 28)}",
            "email": lambda x: seeder.faker.email(),
            "parent": Employee.objects.get(id=random.randint(parent_min, parent_max)),
        },
    )
    seeder.execute()


def run():
    first_record()
    fill_up_data_base(10, "Регіональний директор", 2010, 1, 1)
    fill_up_data_base(100, "Директор по збуту продукції", 2011, 2, 11)
    fill_up_data_base(1000, "Менеджер по закупівлях", 2012, 12, 112)
    fill_up_data_base(10, "Комплектувальник", 2012, 112, 1111)
    fill_up_data_base(10000, "Менеджер з продажу", 2014, 2, 100)
    fill_up_data_base(10, "Водій", 2019, 112, 1111)
    fill_up_data_base(10, "Стажер", 2022, 1112, 2112)
    Employee.objects.rebuild()
    pass
