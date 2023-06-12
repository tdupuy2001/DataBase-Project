import faker 

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

DUMMY_DATA_NUMBER = 20;
TABLE_NAME = "Categories";
TABLE_COLUMNS = ["category_name"]
content = "";


for i in range(DUMMY_DATA_NUMBER):
    category_name=categories[i]
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{category_name}");\n'


with open(f"dummy_data_{TABLE_NAME}.txt", 'w') as f:
    f.write(content)
    
    
    
    
    
    
    
    
    
    
    
    
    