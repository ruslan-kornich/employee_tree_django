import random

from django_seed import Seed
from faker import Faker

from app.models import Employee, Department


def first_create_department():
    seeder = Seed.seeder()
    fake = Faker("ru_RU")
    with Department.objects.disable_mptt_updates():
        seeder.add_entity(Department, 20, {"name": lambda x: fake.bs()})
        seeder.execute()


def second_department():
    seeder = Seed.seeder()
    fake = Faker("ru_RU")
    with Department.objects.disable_mptt_updates():
        seeder.add_entity(Department, 50, {"name": lambda x: fake.bs(),
                                           "parent": random.randint(1, 19)})
        seeder.execute()


def fill_up_data_base(count, position, year):
    seeder = Seed.seeder("uk_UA")
    fake = Faker("uk_UA")
    seeder.add_entity(
        Employee,
        count,
        {
            "name": lambda x: fake.name(),
            "position": position,
            "hire_date": f"{year}-{random.randint(1, 12)}-{random.randint(1, 28)}",
            "email": lambda x: seeder.faker.email(),
            "department": Department.objects.get(id=random.randint(1, 9)),
        },
    )
    seeder.execute()


def run():
    create_department()
    fill_up_data_base(10, "Регіональний директор", 2010)
    fill_up_data_base(100, "Директор по збуту продукції", 2011)
    fill_up_data_base(1000, "Менеджер по закупівлях", 2012)
    fill_up_data_base(10, "Комплектувальник", 2012)
    fill_up_data_base(10000, "Менеджер з продажу", 2014)
    fill_up_data_base(10, "Водій", 2019)
    fill_up_data_base(10, "Стажер", 2022)
    Employee.objects.rebuild()
    pass
