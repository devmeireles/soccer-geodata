import time
from helpers.crawler import Crawler

# initial = 155
# final = 159

initial = input("Please enter the initial id: ")
final = input("Please enter the final id: ")


for id in range(int(initial), int(final)):
    time.sleep(5)
    url = f'https://uk.soccerway.com/teams/spain/futbol-club-barcelona/{id}'

    item = Crawler(url, id)
    saved_item = item.save_data()

    if saved_item != None:
        if type(saved_item) is dict:
            print(saved_item['error'])
        else:
            print(f'Created {id} of {final} as {saved_item}')
    else:
        print(f'{id} not found')
