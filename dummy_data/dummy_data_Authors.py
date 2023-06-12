import faker 

fake = faker.Faker()


DUMMY_DATA_NUMBER = 100;
TABLE_NAME = "Authors";
TABLE_COLUMNS = ["first_name", "last_name","birth_date"]
content = "";

for _ in range(DUMMY_DATA_NUMBER):
    firstName = fake.first_name()
    lastName = fake.last_name()
    birth_date=fake.date_of_birth(minimum_age=20,maximum_age=500)
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{firstName}", "{lastName}", "{birth_date}");\n'


with open(f"dummy_data_{TABLE_NAME}.txt", 'w') as f:
    f.write(content)