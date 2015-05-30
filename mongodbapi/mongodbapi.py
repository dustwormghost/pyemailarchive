import datetime
from pymongo import MongoClient, ASCENDING, DESCENDING
from bson import ObjectId
from pprint import pprint


class MongoDBApi():

    def __init__(self, database_name, collection_name, host='localhost', port=27017):
        self.client = MongoClient(host, port)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def get_client(self):
        return self.client

    def get_db(self):
        return self.db

    def get_collection(self):
        return self.collection

    def


post = {
    'author' : 'Mike',
    'text' : 'My first blog post!',
    'tags' : ['mongodb', 'python', 'pymongo'],
    'date' : datetime.datetime.utcnow()
}

posts = db.posts
# post_id = posts.insert_one(post).inserted_id

# pprint(post_id)

# list all collections
# pprint(db.collection_names(include_system_collections=False))

# find one entry
# pprint(posts.find_one())
# pprint(posts.find_one({'author': 'Mike'}))
# pprint(posts.find_one({'_id': ObjectId('5566871f129afc0bb42bbf84')}))

# bulk inserts, schema-free
new_posts = [
    {"author": "Mike",
     "text": "Another post!",
     "tags": ["bulk", "insert"],
     "date": datetime.datetime(2009, 11, 12, 11, 14)
     },
    {"author": "Eliot",
     "title": "MongoDB is fun",
     "text": "and pretty easy too!",
     "date": datetime.datetime(2009, 11, 10, 10, 45)
     }
]
# result = posts.insert_many(new_posts)
# pprint(result.inserted_ids)

# list posts with cursor
# for post in posts.find({'author': 'Mike'}):
#     pprint(post)
#
# pprint(posts.find().count())

# range queries
d = datetime.datetime(2009, 11, 12, 12)
for post in posts.find({'date': {'$lt': d}}).sort('author'):
    pprint(post)

# indexing
posts.create_index([('date', DESCENDING),
                    ('author', ASCENDING)
                    ])
pprint(posts.find({'date': {'$lt': d}}).sort('author').explain())