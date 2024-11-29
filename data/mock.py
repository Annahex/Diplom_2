from faker import Faker

fake = Faker("ru_RU")

DATA_FOR_USER_CREATE = [
    {
        "email": "test@email.com",
        "password": "password"
    },
    {
        "email": "test@email.com",
        "name": "John Doe"
    },
    {
        "password": "password",
        "name": "John Doe"
    }
]

DATA_FOR_USER_UPDATE = [
    ("email", fake.email()),
    ("name", fake.name())
]