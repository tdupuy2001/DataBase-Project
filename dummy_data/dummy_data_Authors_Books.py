import faker 
import random
from functions import create_ISBN
fake = faker.Faker()


DUMMY_DATA_NUMBER = 200;
TABLE_NAME = "Authors_Books";
TABLE_COLUMNS = ["Books_ISBN","Authors_id_author"]
content = "";
ISBNS=create_ISBN(DUMMY_DATA_NUMBER)


for i in range(DUMMY_DATA_NUMBER):
    Book_ISBN=ISBNS[i]
    Authors_id_author=random.randint(1,100)
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{Book_ISBN}","{Authors_id_author}");\n'


with open(f"dummy_data_{TABLE_NAME}.txt", 'w') as f:
    f.write(content)
    
    
    
    
    
    
    
    
    
    
    
    
    