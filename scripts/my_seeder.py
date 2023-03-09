import random

from django_seed import Seed
from faker import Faker

from app.models import Employee, Department


def first_rec():
    dep = Department(
        name='Відділ 1'
    )
    dep.save()
    global first_parent_id
    first_parent_id = Department.objects.all()[0].id


def fill_dep(count, id_min, id_max):
    seeder = Seed.seeder()
    fake = Faker('ru_RU')
    with Department.objects.disable_mptt_updates():
        seeder.add_entity(Department, count, {
            'name': lambda x: "Відділ " + fake.bs(),
            'parent': lambda x: Department.objects.get(
                id=random.randint((first_parent_id + id_min), (first_parent_id + id_max))
            ),
        })
        seeder.execute()


def fill_up_data_base(count, position, year, id_min, id_max):
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
            'department': lambda x: Department.objects.get(
                id=random.randint((first_parent_id + id_min), (first_parent_id + id_max))
                ),
        },
    )
    seeder.execute()


def run():
    first_rec()
    fill_dep(2, 0, 0)
    fill_dep(4, 1, 2)
    fill_dep(5, 3, 6)
    fill_dep(7, 7, 11)
    fill_dep(7, 11, 18)
    Department.objects.rebuild()
    fill_up_data_base(1000, "Регіональний директор", 2010, 1, 2)
    fill_up_data_base(10_000, "Директор по збуту продукції", 2014, 1, 10)
    fill_up_data_base(10_000, "Менеджер по закупівлях", 2012, 1, 25)
    fill_up_data_base(10_000, "Комплектувальник", 2012, 1, 25)
    fill_up_data_base(10_000, "Менеджер з продажу", 2014, 1, 25)
    fill_up_data_base(10_000, "Водій", 2019, 1, 25)
    fill_up_data_base(5000, "Стажер", 2022, 1, 25)
    pass
