## Сценарии использования и эндпоинты:
- просмотр средней пользовательской оценки фильма;
- добавление, удаление или изменение оценки
    - GET, POST, DELETE filmworks/{filmwork_id}/score (get возвращает среднюю оценку фильма);

- добавление / удаление / изменение рецензии к фильму
    - POST, DELETE filmworks/{filmwork_id}/reviews;
- добавление / удаление лайка рецензии
    - POST, DELETE filmworks/{filmwork_id}/reviews/{user_id}/likes;
- просмотр списка рецензий с возможностью гибкой сортировки (по дате и лайкам);
- просмотр рецензий на странице фильма
    - GET filmworks/{filmwork_id}/reviews?order=likes|created_at;
- просмотр рецензий на странице пользователя
    - GET users/{user_id}/reviews;

- добавление / удаление фильма в закладки
    - POST, DELETE /bookmarks;
- просмотр списка закладок (по юзеру получить из его закладок)
    - GET /bookmarks;