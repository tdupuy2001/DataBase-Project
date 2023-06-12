import faker 
import random
from functions import create_ISBN
fake = faker.Faker()

categories = [
    "Fantasy",
    "Science Fiction",
    "Mystery/Thriller",
    "Romance",
    "Historical Fiction",
    "Young Adult",
    "Horror",
    "Non-Fiction (Biography/Autobiography)",
    "Crime/Noir",
    "Adventure",
    "Comedy/Humor",
    "Dystopian",
    "Paranormal/Supernatural",
    "Self-Help/Personal Development",
    "Poetry",
    "Memoir",
    "Contemporary Fiction",
    "Science/Popular Science",
    "Travel",
    "Children's Literature"
]

DUMMY_DATA_NUMBER = 200;
TABLE_NAME = "Categories_Books";
TABLE_COLUMNS = ["Books_ISBN","Categories_category_name"]
content = "";
ISBNS=create_ISBN(DUMMY_DATA_NUMBER)


for i in range(DUMMY_DATA_NUMBER):
    Book_ISBN=ISBNS[i]
    Categories_category_name=categories[random.randint(0,19)]
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{Book_ISBN}","{Categories_category_name}");\n'


with open(f"dummy_data_{TABLE_NAME}.txt", 'w') as f:
    f.write(content)
    
    
    
    
    
    
    
    
    
    
    
    
    