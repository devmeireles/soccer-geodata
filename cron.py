from apscheduler.schedulers.blocking import BlockingScheduler
from helpers.database import Database
import os
from dotenv import load_dotenv
from datetime import datetime
import time
from helpers.crawler import Crawler

load_dotenv(verbose=True)
sched = BlockingScheduler()

# Last id 52257

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    mongo_address = os.getenv('MONGO_ADDRESS')
    db_name = os.getenv('DATABASE_NAME')
    collection = 'team_id'

    database = Database(mongo_address, db_name)

    id = Database.get_team_id()

    url = f'https://uk.soccerway.com/teams/spain/futbol-club-barcelona/{id}'

    item = Crawler(url, id)
    saved_item = item.save_data()

    query = {"id": id}

    if saved_item != None:
        if type(saved_item) is dict:
            print(saved_item['error'])
            data = {"$set": {"status": "crawled"}}
            Database.update(data, query, collection)
        else:
            print(f'Created {id} as {saved_item}')
            data = {"$set": {"status": "crawled"}}
            Database.update(data, query, collection)
    else:
        print(f'{id} not found')
        data = {"$set": {"status": "not found"}}
        Database.update(data, query, collection)


sched.start()
