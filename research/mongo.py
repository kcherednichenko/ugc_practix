import uuid
import datetime
import bson
import random
import string
from typing import List
from pymongo.collection import Collection


def random_str(size):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(size))


def insert(collection: Collection, data: List) -> List:
    res = collection.insert_many(data)
    return res.inserted_ids


def genererate_data_filmwork(count_filmwork, count_scores, count_reviews, count_like_reviews, size_header, size_text):
    res = []
    for i in range(count_filmwork):
        buff = {
            "id": bson.Binary.from_uuid(uuid.uuid4()),
            "name": random_str(size_header),
            "scores": [],
            "reviews": []
        }
        for i in range(count_scores):
            buff["scores"].append({
                "user_id": bson.Binary.from_uuid(uuid.uuid4()),
                "score": random.randint(0, 10)
            })

        for i in range(count_reviews):
            reviews = {
                "user_id": bson.Binary.from_uuid(uuid.uuid4()),
                "header": random_str(size_header),
                "text": random_str(size_text),
                "created_at": datetime.datetime.now(),
                "likes": []
            }

            for i in range(count_like_reviews):
                reviews["likes"].append({"user_id": bson.Binary.from_uuid(uuid.uuid4())})

            buff["reviews"].append(reviews)

        res.append(buff)

    return res


def genererate_data_user(count_user, count_bookmarks, count_reviews, size_header, size_text):
    res = []
    for i in range(count_user):
        buff = {
            "id": bson.Binary.from_uuid(uuid.uuid4()),
            "name": random_str(size_header),
            "reviews": [],
            "bookmarks": []
        }
        for i in range(count_bookmarks):
            buff["bookmarks"].append({
                "filmwork_id": bson.Binary.from_uuid(uuid.uuid4())
            })

        for i in range(count_reviews):
            reviews = {
                "filmwork_id": bson.Binary.from_uuid(uuid.uuid4()),
                "header": random_str(size_header),
                "text": random_str(size_text),
                "created_at": datetime.datetime.now(),
            }

            buff["reviews"].append(reviews)

        res.append(buff)

    return res


def create_data_for_insert_mongo(count_filmwork, count_scores, count_reviews, count_like_reviews,
                                 size_header, size_text, count_user, count_bookmarks):
    data_filmworks = genererate_data_filmwork(count_filmwork, count_scores, count_reviews,
                                              count_like_reviews, size_header, size_text)
    data_users = genererate_data_user(count_user, count_bookmarks, count_reviews, size_header, size_text)

    return {'filmworks': data_filmworks, 'users': data_users}


def create_collections(db):
    db.create_collection('filmworks')
    db.create_collection('users')


def drop_collections(db):
    db.filmworks.drop()
    db.users.drop()


def test_insert_mongo(db, data):
    insert(collection=db.filmworks, data=data['filmworks'])
    insert(collection=db.users, data=data['users'])


def find(collection: Collection, condition: dict, multiple: bool = False):
    if multiple:
        results = collection.find(condition)
        return [item for item in results]
    return collection.find_one(condition)


def find_all_id_filmworks(db):
    result = find(collection=db.filmworks, condition={}, multiple=True)
    return [r['id'] for r in result]


def find_expected_value_for_id_filmwork(db, id):
    pipeline = [
        {'$match': {'id': id}},
        {'$unwind': '$scores'},
        {'$group': {
            '_id': 'null',
            'average': {'$avg': '$scores.score'}
        }
        }
    ]
    result = db.filmworks.aggregate(pipeline)
    return result


def test_expected_value_mongo(db, all_id):
    for id in all_id:
        find_expected_value_for_id_filmwork(db, id)


def add_like(collections, id, count_reviews):
    for i in range(count_reviews):
        collections.update_many(
            {'id': id},
            {'$push': {"reviews." + str(i) + ".likes": {"user_id": bson.Binary.from_uuid(uuid.uuid4())}}})


def test_new_like(db, all_id_filmwork, count_reviews):
    for id in all_id_filmwork:
        add_like(db.filmworks, id, count_reviews)
