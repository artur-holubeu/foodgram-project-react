# FoodGram
[![FoodGram CL-CD](https://github.com/artur-holubeu/foodgram-project-react/actions/workflows/foodgram_workflow.yaml/badge.svg?branch=master)](https://github.com/artur-holubeu/foodgram-project-react/actions/workflows/foodgram_workflow.yaml)

Лучший сервис для создания и просмотра рецептов со всего мира, здесь
каждый сможет создать рецепт, подписаться на лучшего повара, добавить
в избранные или в лист покупок желаемые рецепты и с итоговым списком 
продуктов отправится в магазин.
### Описание проекта
Бэкенд часть выполнена в лучших практиках стандарта **RESTful веб-API**

Фронт выполнен на react-js индусами, шутка, не знаю кем, может и индусами.

### Адрес сайта

[q8.by](http://q8.by/)

### Необходимые инструменты для запуска
```
docker
docker-compose
```
### Необходимые ключи для файла .env
_На текущий момент проект работает только с базой данных POSTGRES, 
если необходимо подключить другую базу данных, то следует выполнить форк 
и переписать реализацию под нужную базу данных_
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME
DB_HOST
DB_PORT
POSTGRES_USER
POSTGRES_PASSWORD
```

### Запуск приложения
```
sudo docker-compose up -d

sudo docker-compose exec backend python manage.py makemigrations
sudo docker-compose exec backend python manage.py migrate --noinput
sudo docker-compose exec backend python manage.py collectstatic --no-input
```

* #### Подгрузить сформированный ранее список ингредиентов и тегов
```
sudo docker-compose exec web python manage.py loaddata fixtures.json
```

* #### Создание суперпользователя
```
Только для тестирования уже создан суперпользователь:
login: superuser@superuser.com
password: 9TmJ21p^!14NDSSv5p
```



### Описание API запросов с примерами ответов

- [Получить список пользователей](https://github.com/artur-holubeu/foodgram-project-react#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D0%B5%D0%B9)
- [Регистрация пользователя](https://github.com/artur-holubeu/foodgram-project-react#%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F-%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8F)
- [Получить токен авторизации](https://github.com/artur-holubeu/foodgram-project-react#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D1%82%D0%BE%D0%BA%D0%B5%D0%BD-%D0%B0%D0%B2%D1%82%D0%BE%D1%80%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D0%B8)
- [Удалить токен авторизации текущего пользователя](https://github.com/artur-holubeu/foodgram-project-react#%D1%83%D0%B4%D0%B0%D0%BB%D0%B8%D1%82%D1%8C-%D1%82%D0%BE%D0%BA%D0%B5%D0%BD-%D0%B0%D0%B2%D1%82%D0%BE%D1%80%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D0%B8-%D1%82%D0%B5%D0%BA%D1%83%D1%89%D0%B5%D0%B3%D0%BE-%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8F)
- [Получить данные пользователя](https://github.com/artur-holubeu/foodgram-project-react#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%B5-%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8F)
- [Получить данные текущего пользователя](https://github.com/artur-holubeu/foodgram-project-react#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%B5-%D1%82%D0%B5%D0%BA%D1%83%D1%89%D0%B5%D0%B3%D0%BE-%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8F)
- [Изменить пароль текущего пользователя](https://github.com/artur-holubeu/foodgram-project-react#%D0%B8%D0%B7%D0%BC%D0%B5%D0%BD%D0%B8%D1%82%D1%8C-%D0%BF%D0%B0%D1%80%D0%BE%D0%BB%D1%8C-%D1%82%D0%B5%D0%BA%D1%83%D1%89%D0%B5%D0%B3%D0%BE-%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8F)
- [Восстановить пароль пользователя по его email](https://github.com/artur-holubeu/foodgram-project-react#%D0%B2%D0%BE%D1%81%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%B8%D1%82%D1%8C-%D0%BF%D0%B0%D1%80%D0%BE%D0%BB%D1%8C-%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8F-%D0%BF%D0%BE-%D0%B5%D0%B3%D0%BE-email)
- [Подтверждение для восстановления пароля](https://github.com/artur-holubeu/foodgram-project-react#%D0%BF%D0%BE%D0%B4%D1%82%D0%B2%D0%B5%D1%80%D0%B6%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5-%D0%B4%D0%BB%D1%8F-%D0%B2%D0%BE%D1%81%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F-%D0%BF%D0%B0%D1%80%D0%BE%D0%BB%D1%8F)
- [Посмотреть список подписчиков](https://github.com/artur-holubeu/foodgram-project-react#%D0%BF%D0%BE%D1%81%D0%BC%D0%BE%D1%82%D1%80%D0%B5%D1%82%D1%8C-%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D1%87%D0%B8%D0%BA%D0%BE%D0%B2)
- [Подписаться на пользователя](https://github.com/artur-holubeu/foodgram-project-react#%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D0%B0%D1%82%D1%8C%D1%81%D1%8F-%D0%BD%D0%B0-%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8F)
- [Отписаться от пользователя](https://github.com/artur-holubeu/foodgram-project-react#%D0%BE%D1%82%D0%BF%D0%B8%D1%81%D0%B0%D1%82%D1%8C%D1%81%D1%8F-%D0%BE%D1%82-%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8F)
- [Получить список ингредиентов](https://github.com/artur-holubeu/foodgram-project-react#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D0%B8%D0%BD%D0%B3%D1%80%D0%B5%D0%B4%D0%B8%D0%B5%D0%BD%D1%82%D0%BE%D0%B2)
- [Получить ингредиент](https://github.com/artur-holubeu/foodgram-project-react#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D0%B8%D0%BD%D0%B3%D1%80%D0%B5%D0%B4%D0%B8%D0%B5%D0%BD%D1%82)
- [Получить список тегов](https://github.com/artur-holubeu/foodgram-project-react#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D1%82%D0%B5%D0%B3%D0%BE%D0%B2)
- [Получить тег](https://github.com/artur-holubeu/foodgram-project-react#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D1%82%D0%B5%D0%B3)
- [Получить список рецептов](https://github.com/artur-holubeu/foodgram-project-react#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D1%80%D0%B5%D1%86%D0%B5%D0%BF%D1%82%D0%BE%D0%B2)
- [Создать рецепт](https://github.com/artur-holubeu/foodgram-project-react#%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D1%82%D1%8C-%D1%80%D0%B5%D1%86%D0%B5%D0%BF%D1%82)
- [Получить рецепт по id](https://github.com/artur-holubeu/foodgram-project-react#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D1%80%D0%B5%D1%86%D0%B5%D0%BF%D1%82-%D0%BF%D0%BE-id)
- [Полное или частичное обновление рецепта](https://github.com/artur-holubeu/foodgram-project-react#%D0%BF%D0%BE%D0%BB%D0%BD%D0%BE%D0%B5-%D0%B8%D0%BB%D0%B8-%D1%87%D0%B0%D1%81%D1%82%D0%B8%D1%87%D0%BD%D0%BE%D0%B5-%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5-%D1%80%D0%B5%D1%86%D0%B5%D0%BF%D1%82%D0%B0)
- [Удалить рецепт](https://github.com/artur-holubeu/foodgram-project-react#%D1%83%D0%B4%D0%B0%D0%BB%D0%B8%D1%82%D1%8C-%D1%80%D0%B5%D1%86%D0%B5%D0%BF%D1%82)
- [Добавить рецепт в избранное](https://github.com/artur-holubeu/foodgram-project-react#%D0%B4%D0%BE%D0%B1%D0%B0%D0%B2%D0%B8%D1%82%D1%8C-%D1%80%D0%B5%D1%86%D0%B5%D0%BF%D1%82-%D0%B2-%D0%B8%D0%B7%D0%B1%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5)
- [Удалить рецепт из избранного](https://github.com/artur-holubeu/foodgram-project-react#%D1%83%D0%B4%D0%B0%D0%BB%D0%B8%D1%82%D1%8C-%D1%80%D0%B5%D1%86%D0%B5%D0%BF%D1%82-%D0%B8%D0%B7-%D0%B8%D0%B7%D0%B1%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B3%D0%BE)
- [Добавить рецепт в список покупок](https://github.com/artur-holubeu/foodgram-project-react#%D0%B4%D0%BE%D0%B1%D0%B0%D0%B2%D0%B8%D1%82%D1%8C-%D1%80%D0%B5%D1%86%D0%B5%D0%BF%D1%82-%D0%B2-%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D0%BF%D0%BE%D0%BA%D1%83%D0%BF%D0%BE%D0%BA)
- [Удалить рецепт из списка покупок](https://github.com/artur-holubeu/foodgram-project-react#%D1%83%D0%B4%D0%B0%D0%BB%D0%B8%D1%82%D1%8C-%D1%80%D0%B5%D1%86%D0%B5%D0%BF%D1%82-%D0%B8%D0%B7-%D1%81%D0%BF%D0%B8%D1%81%D0%BA%D0%B0-%D0%BF%D0%BE%D0%BA%D1%83%D0%BF%D0%BE%D0%BA)
- [Скачать список покупок](https://github.com/artur-holubeu/foodgram-project-react#%D1%81%D0%BA%D0%B0%D1%87%D0%B0%D1%82%D1%8C-%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D0%BF%D0%BE%D0%BA%D1%83%D0%BF%D0%BE%D0%BA)

##### Получить список пользователей
`GET api/users/`

```
QUERY PARAMETERS:
page - Номер страницы.
list - Количество объектов на странице.
```
**RESPONSE**
```json5
{
  "count": 123,
  "next": "http://foodgram.example.org/api/users/?page=4",
  "previous": "http://foodgram.example.org/api/users/?page=2",
  "results": [
    {
      "email": "user@example.com",
      "id": 0,
      "username": "string",
      "first_name": "Вася",
      "last_name": "Пупкин",
      "is_subscribed": true
    }
  ]
}
```
##### Регистрация пользователя
`POST api/users/`

```
REQUEST BODY SCHEMA: application/json
email - Адрес электронной почты.
username - Уникальный юзернейм.
first_name - Имя.
last_name - Фамилия.
password - Пароль.
```
**RESPONSE**
```json5
{
  "email": "test@yandex.ru",
  "id": 1,
  "username": "test.test",
  "first_name": "Test",
  "last_name": "Test"
}
```

##### Получить токен авторизации
`POST/api/auth/token/login/`

```
REQUEST BODY SCHEMA: application/json
password - пароль пользователя
email - email пользователя
```
**RESPONSE**
```json5
{
    "auth_token": "4304404dd5522ec1f4579ed5508cc921de083fe2"
}
```

##### Удалить токен авторизации текущего пользователя
`POST /api/auth/token/logout/`

```
AUTHORIZATIONS: Token {token}
REQUEST BODY SCHEMA: application/json
```
**RESPONSE**
```json5
{}
```


##### Получить данные пользователя
`GET api/users/{id}/`

```
PATH PARAMETERS:
id - Уникальный номер пользователя
```
**RESPONSE**
```json5
{
  "email": "user@example.com",
  "id": 0,
  "username": "string",
  "first_name": "Test",
  "last_name": "Test",
  "is_subscribed": false
}
```

##### Получить данные текущего пользователя
`GET api/users/me/`

```
AUTHORIZATIONS: Token {token}
```
**RESPONSE**
```json5
{
  "email": "user@example.com",
  "id": 0,
  "username": "string",
  "first_name": "Test",
  "last_name": "Test",
  "is_subscribed": false
}
```

##### Изменить пароль текущего пользователя
`POST /api/users/set_password/`

```
AUTHORIZATIONS: Token {token}
REQUEST BODY SCHEMA: application/json
new_password - новый пароль
current_password - старый пароль
```
**RESPONSE**
```json5
{}
```

##### Восстановить пароль пользователя по его email
`POST /api/users/reset_password/`

```
REQUEST BODY SCHEMA: application/json
email - email пользователя
```
**RESPONSE**
```json5
{}
```

##### Подтверждение для восстановления пароля
`POST /api/users/reset_password_confirm/`

```
REQUEST BODY SCHEMA: application/json
uid - уникальный id пользователя пришедший на почту указанную при 
запросе на восстановление пароля
token - токен пришедший на почту 
new_password - новый пароль для пользователя
```
**RESPONSE**
```json5
{}
```

##### Посмотреть список подписчиков
`GET /api/users/subscriptions/`

```
AUTHORIZATIONS: Token {token}
QUERY PARAMETERS:
page - Номер страницы.
limit - Количество объектов на странице.
recipes_limit - Количество объектов внутри поля recipes.
```
**RESPONSE**
```json5
{
  "count": 123,
  "next": "http://foodgram.example.org/api/users/subscriptions/?page=4",
  "previous": "http://foodgram.example.org/api/users/subscriptions/?page=2",
  "results": [
    {
      "email": "user@example.com",
      "id": 0,
      "username": "string",
      "first_name": "Test",
      "last_name": "Test",
      "is_subscribed": true,
      "recipes": [
        {
          "id": 0,
          "name": "string",
          "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
          "cooking_time": 1
        }
      ],
      "recipes_count": 0
    }
  ]
}
```

##### Подписаться на пользователя
`GET /api/users/{id}/subscribe/`

```
AUTHORIZATIONS: Token {token}
QUERY PARAMETERS:
recipes_limit - Количество объектов внутри поля recipes.
```
**RESPONSE**
```json5
{
  "email": "user@example.com",
  "id": 0,
  "username": "string",
  "first_name": "Test",
  "last_name": "Test",
  "is_subscribed": true,
  "recipes": [
    {
      "id": 0,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "cooking_time": 1
    }
  ],
  "recipes_count": 0
}
```

##### Отписаться от пользователя
`DELETE /api/users/{id}/subscribe/`

```
AUTHORIZATIONS: Token {token}
```
**RESPONSE**
```json5
{}
```

##### Получить список ингредиентов
`GET /api/ingredients/`

```
QUERY PARAMETERS:
name - Поиск по частичному вхождению в начале названия ингредиента.
```
**RESPONSE**
```json5
[
  {
    "id": 1,
    "name": "Капуста",
    "measurement_unit": "кг"
  }
]
```

##### Получить ингредиент
`GET /api/ingredients/{id}/`

**RESPONSE**
```json5
[
  {
    "id": 1,
    "name": "Капуста",
    "measurement_unit": "кг"
  }
]
```

##### Получить список тегов
`GET /api/tags/`

**RESPONSE**
```json5
[
  {
    "id": 1,
    "name": "Завтрак",
    "color": "#E26C2D",
    "slug": "breakfast"
  }
]
```

##### Получить тег
`GET /api/tags/{id}/`

**RESPONSE**
```json5
{
  "id": 1,
  "name": "Завтрак",
  "color": "#E26C2D",
  "slug": "breakfast"
}
```

##### Получить список рецептов
`GET /api/recipes/`

```
QUERY PARAMETERS:
page - Номер страницы.
limit - Количество объектов на странице.
is_favorited - true/false. Показывать только рецепты, находящиеся 
в списке избранного.
is_in_shopping_cart - true/false. Показывать только рецепты, находящиеся 
в списке покупок.
author - Показывать рецепты только автора с указанным id.
tags - Показывать рецепты только с указанными тегами (по slug).
       (Example: tags=lunch&tags=breakfast)
```
**RESPONSE**
```json5
{
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Test",
        "last_name": "Test",
        "is_subscribed": true
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```

##### Создать рецепт
`POST /api/recipes/`

```json5
AUTHORIZATIONS: Token {token}
REQUEST BODY SCHEMA: application/json
ingredients - Список ингредиентов. 
    id - Уникальный id ингредиента
    amount - Количество в рецепте
tags - Список id тегов
image - Картинка, закодированная в Base64
name - Название
text - Описание
cooking_time - Время приготовления

REQUEST FOR EXAMPLE:

{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```
**RESPONSE**
```json5
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": true
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}
```

##### Получить рецепт по id
`GET /api/recipes/{id}`
**RESPONSE**
```json5
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Test",
    "last_name": "Test",
    "is_subscribed": true
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}
```

##### Полное или частичное обновление рецепта
`PUT/PATCH /api/recipes/{id}/`

```json5
AUTHORIZATIONS: Token {token}
REQUEST BODY SCHEMA: application/json
ingredients - Список ингредиентов. 
    id - Уникальный id ингредиента
    amount - Количество в рецепте
tags - Список id тегов
image - Картинка, закодированная в Base64
name - Название
text - Описание
cooking_time - Время приготовления

REQUEST FOR EXAMPLE:

{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```
**RESPONSE**
```json5
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": true
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}
```

##### Удалить рецепт
`DELETE /api/recipes/{id}/`
**RESPONSE**
```json5
{}
```

##### Добавить рецепт в избранное
`GET /api/recipes/{id}/favorite/`

```json5
AUTHORIZATIONS: Token {token}
```
**RESPONSE**
```json5
{
  "id": 0,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "cooking_time": 1
}
```

##### Удалить рецепт из избранного
`DELETE /api/recipes/{id}/favorite/`

```json5
AUTHORIZATIONS: Token {token}
```

**RESPONSE**
```json5
{}
```

##### Добавить рецепт в список покупок
`GET /api/recipes/{id}/shopping_cart/`

```json5
AUTHORIZATIONS: Token {token}
```
**RESPONSE**
```json5
{
  "id": 0,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "cooking_time": 1
}
```

##### Удалить рецепт из списка покупок
`DELETE /api/recipes/{id}/shopping_cart/`

```json5
AUTHORIZATIONS: Token {token}
```

**RESPONSE**
```json5
{}
```

##### Скачать список покупок
`GET /api/recipes/download_shopping_cart/`

```json5
AUTHORIZATIONS: Token {token}
```

**RESPONSE**
```
RESPONSE SCHEMA: application/pdf
string <binary>
```


###### Автор и контакты для связи
`Artur Golubev`
`artur-holubeu@yandex.by`
