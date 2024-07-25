import time

from db.mongo import create_connect_mongo
from db.postgres import get_session_postgres

from mongo import (test_insert_mongo, create_data_for_insert_mongo, create_collections,
                   drop_collections, find_all_id_filmworks, test_expected_value_mongo, test_new_like)
from postgres import (test_insert_postgres, create_database, drop_database, create_data_for_insert_postgres,
                      test_expected_value_postgres, test_add_likes)


def start_test_insert():
    print('Тест на вставку.')
    count_filmwork = 30
    count_scores = 50
    count_reviews = 30
    count_like_reviews = 80
    size_header = 20
    size_text = 2000
    count_user = 400
    count_bookmarks = 30
    print('Создаем данные mongo и соединяемся с бд.')
    db = create_connect_mongo()
    drop_collections(db)
    create_collections(db)
    data = create_data_for_insert_mongo(count_filmwork=count_filmwork, count_scores=count_scores,
                                        count_reviews=count_reviews,
                                        count_like_reviews=count_like_reviews,
                                        size_header=size_header, size_text=size_text,
                                        count_user=count_user, count_bookmarks=count_bookmarks)
    start_time = time.time()
    print('Выполняем.')
    test_insert_mongo(db, data)
    end_time = time.time()
    time_mongo = end_time - start_time

    print('Создаем данные postgres и соединяемся с бд.')
    start_time = time.time()
    drop_database()
    create_database()
    db = get_session_postgres()
    data = create_data_for_insert_postgres(count_user=count_user, count_bookmarks=count_user * count_bookmarks,
                                           count_like_reviews=count_like_reviews * count_reviews,
                                           count_reviews=count_reviews, size_header=size_header,
                                           size_text=size_text, count_scores_users=count_scores,
                                           count_scores_filmwork=count_filmwork, count_filmwork=count_filmwork,
                                           count_reviews_user=count_reviews * count_filmwork)
    print('Выполняем.')
    test_insert_postgres(db, data)
    end_time = time.time()
    time_postgres = end_time - start_time

    print('Время выполнения вставки mongo: ' + str(time_mongo) + ' секунд.')
    print('Время выполнения вставки postgres: ' + str(time_postgres) + ' секунд.')


def start_test_expected_value():
    print('Тест на математическое ожидание.')
    db_mongo = create_connect_mongo()
    db_postgres = get_session_postgres()

    print('Находим данные для mongo.')
    all_id = find_all_id_filmworks(db_mongo)
    print('Выполняем.')
    start_time = time.time()
    test_expected_value_mongo(db_mongo, all_id)
    end_time = time.time()
    time_mongo = end_time - start_time

    # Сразу выпоняем, так как в таблице данные уже готовы
    print('Выполняем для postgres')
    start_time = time.time()
    test_expected_value_postgres(db_postgres)
    end_time = time.time()
    time_postgres = end_time - start_time

    print('Время выполнения поиска мат. ожидания для mongo: ' + str(time_mongo) + ' секунд.')
    print('Время выполнения поиска мат. ожидания для postgres: ' + str(time_postgres) + ' секунд.')


def start_test_like_reviews():
    print('Тест на лайки.')
    db_mongo = create_connect_mongo()
    db_postgres = get_session_postgres()

    print('Находим данные для mongo.')
    all_id = find_all_id_filmworks(db_mongo)
    print('Выполняем.')
    start_time = time.time()
    test_new_like(db_mongo, all_id, 20)
    end_time = time.time()
    time_mongo = end_time - start_time

    # Сразу выпоняем, так как в таблице данные уже готовы
    print('Выполняем для postgres')
    start_time = time.time()
    test_add_likes(db_postgres, 20 * 30)
    end_time = time.time()
    time_postgres = end_time - start_time

    print('Время выполнения добавления лайков для mongo: ' + str(time_mongo) + ' секунд.')
    print('Время выполнения добавления лайков для postgres: ' + str(time_postgres) + ' секунд.')


if __name__ == '__main__':
    print('Тест на скорость записи.')
    start_test_insert()
    time.sleep(10)
    print('Тест на мат. ожидание')
    start_test_expected_value()
    time.sleep(10)
    print('Тест на добавление лайка к отзыву.')
    start_test_like_reviews()
