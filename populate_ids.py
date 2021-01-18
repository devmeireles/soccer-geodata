from helpers.database import Database
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(verbose=True)

mongo_address = os.getenv('MONGO_ADDRESS')
db_name = os.getenv('DATABASE_NAME')
collection = 'team_id'

initial = 9999
final = 20000

now = datetime.now()
now = now.strftime("%Y-%m-%d %H:%M:%S")

database = Database(mongo_address, db_name)

for id in range(int(initial), int(final)):
    exists = Database.connection[f'{collection}'].find_one(
        {"id": id})
    if(exists == None):
        data = {"id": id, "status": "created", "created_at": now}
        print(Database.save(data, collection))
    else:
        print(f'{id} already created')
