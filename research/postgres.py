import uuid
import random
import datetime
import string

from sqlalchemy import insert, func

from models.models_postgres import Filmwork, Scores, Reviews, LikeReviews, User, Bookmarks, ReviewsUser
from models.base_model import OrmBase
from db.postgres import engine


def create_database() -> None:
    OrmBase.metadata.create_all(engine)


def drop_database() -> None:
    OrmBase.metadata.drop_all(engine)


def insert_to_db(table, db, values):
    ins = insert(table).values(values)
    db.execute(ins)
    db.commit()


def insert_to_db_one(table, db, value):
    ins = insert(table).values(value)
    db.execute(ins)
    db.commit()


def random_str(count):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(count))


def generate_table_user(count):
    return [{'name': random_str(20)} for i in range(count)]


def generate_table_bookmarks(count):
    return [{'user_id': uuid.uuid4(), 'filmwork_id': uuid.uuid4()} for i in range(count)]


def generate_table_like_reviews(count):
    return [{'user_id': uuid.uuid4(), 'reviews_id': uuid.uuid4(), 'like': True} for i in range(count)]


def generate_table_reviews(count, size_header, size_text):
    return [{'filmwork_id': uuid.uuid4(), 'header': random_str(size_header), 'text': random_str(size_text),
             'created_at': datetime.datetime.now()} for i in range(count)]


def generate_table_reviews_user(count):
    return [{'user_id': uuid.uuid4(), 'reviews_id': uuid.uuid4()} for i in range(count)]


def generate_table_scores(count_users, count_filmwork):
    res = []
    for i in range(count_filmwork):
        id_filmworks = uuid.uuid4()
        for j in range(count_users):
            buff = {'user_id': uuid.uuid4(), 'filmwork_id': id_filmworks,
                    'score': random.randint(0, 10)}
            res.append(buff)

    return res


def generate_table_filmwork(count):
    return [{'name': random_str(20)} for i in range(count)]


def create_data_for_insert_postgres(count_user, count_bookmarks, count_like_reviews, count_reviews, size_header,
                                    size_text, count_scores_users, count_scores_filmwork, count_filmwork,
                                    count_reviews_user):
    data_user = generate_table_user(count_user)
    data_bookmarks = generate_table_bookmarks(count_bookmarks)
    data_like_reviews = generate_table_like_reviews(count_like_reviews)
    data_reviews = generate_table_reviews(count_reviews, size_header, size_text)
    data_scores = generate_table_scores(count_scores_users, count_scores_filmwork)
    data_filmwork = generate_table_filmwork(count_filmwork)
    data_reviews_user = generate_table_reviews_user(count_reviews_user)
    return {'Filmwork': data_filmwork, 'Scores': data_scores, 'Reviews': data_reviews,
            'LikeReviews': data_like_reviews, 'User': data_user, 'Bookmarks': data_bookmarks,
            'ReviewsUser': data_reviews_user}


def test_insert_postgres(db, data):
    insert_to_db(User, db, data['User'])
    insert_to_db(Bookmarks, db, data['Bookmarks'])
    insert_to_db(LikeReviews, db, data['LikeReviews'])
    insert_to_db(Reviews, db, data['Reviews'])
    insert_to_db(Scores, db, data['Scores'])
    insert_to_db(Filmwork, db, data['Filmwork'])
    insert_to_db(ReviewsUser, db, data['ReviewsUser'])


def test_add_likes(db, count):
    values = [{'user_id': uuid.uuid4(), 'reviews_id': uuid.uuid4(), 'like': True} for i in range(count)]
    for value in values:
        insert_to_db_one(LikeReviews, db, value)


def test_expected_value_postgres(db):
    res = db.query(Scores.filmwork_id, func.avg(Scores.score)).group_by(Scores.filmwork_id).all()
    for result in res:
        print(result)
