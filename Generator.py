import public
from faker import Faker


class Generator(Faker):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.faker = Faker()

    def generate_name(self) -> str: return self.faker.name()

    def generate_phone(self) -> str: return self.faker.phone_number()

