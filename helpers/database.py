from pymongo import MongoClient


class Database():
    """
    A class responsible for execute opertions in a Mongo Database 

    Attributes
    ----------
    url: address
        The url for Mongo connector

    url: database
        The database to be connected

    Methods
    -------
    connect(cls, addr, db)
        Receives a database address and name to return a connected instance

    save(cls, addr, db)
        Receives a json data and a collection to be saved, then return the inserted id
    """
    connection = None
    database = None

    def __init__(self, address, database):
        self.address = address
        self.database = database
        Database.connect(address, database)

    @classmethod
    def connect(cls, addr, db):
        client = MongoClient(addr)
        database = db
        cls.connection = client[f'{database}']

    @staticmethod
    def save(data, collection):
        result = Database.connection[f'{collection}'].insert_one(data)
        return result.inserted_id

    @staticmethod
    def update(data, query, collection):
        Database.connection[f'{collection}'].update_one(query, data)


    @staticmethod
    def save_not_exists(data, collection):
        exists = Database.connection[f'{collection}'].find_one(
            {"club_id": data['club_id']})
        if(exists == None):
            return Database.save(data, collection)
        else:
            return {'error': f"{data['club_id']} already exists"}

    @staticmethod
    def get_team_id():
        item = Database.connection['team_id'].find_one(
            {"status": "created"})

        return item['id']
