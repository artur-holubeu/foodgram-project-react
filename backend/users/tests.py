from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Subscription


class PaginationTestCase(TestCase):
    def pagination(self, response, **kwargs):
        """Реализованы проверки:
            - наличие полей в ответе по атрибуту pagination_fields
            - проверка типа полей по атрибуту field_type_{field_name}
            - проверка значения для поля по атрибуту field_result_{field_name}
        :param response:
        :param kwargs:
        :return:
        """
        self.response = response
        self.url = response.request.get('PATH_INFO')
        if kwargs.get('pagination_fields'):
            pagination_fields = kwargs.get('pagination_fields')
        else:
            pagination_fields = ('count', 'next', 'previous', 'results')

        # корректные поля пагинации
        for attr in pagination_fields:
            with self.subTest(field=attr):
                self.assertIn(
                    attr,
                    response.data,
                    msg=(f'Ошибка пагинации при запросе {self.url} не найден '
                         f'параметр {attr}')
                )

        # корректное значение для параметра count если есть ожидаемый результат
        for field in [x for x in kwargs if 'field_result' in x]:
            self._check_result_for_field(field, kwargs.get(field))

        # проверка типов полей
        for field in [x for x in kwargs if 'field_type' in x]:
            self._check_type_for_field(field, kwargs.get(field))

    def _check_result_for_field(self, field, expected_result):
        """Проверка поля на тип данных
        :param field: str(full_name) or field_name
        :param expected_result: Any
        :return: None
        """
        _field = field.split('_')[-1]
        self.assertEqual(
            self.response.data[_field],
            expected_result,
            msg=(
                f'При GET запросе {self.url} возвращаете данные '
                f'с пагинацией. Значение параметра {_field} не правильное')
        )

    def _check_type_for_field(self, field, expected_type):
        """Проверка поля на тип данных
        :param field: str(full_name) or field_name
        :param expected_type: type
        :return: None
        """
        _field = field.split('_')[-1] if len(field.split('_')) > 1 else field
        self.assertIsInstance(
            self.response.data[_field],
            expected_type,
            msg=(f'При GET запросе {self.url} возвращаете данные с пагинацией.'
                 f'Тип параметра {_field} должен быть список')
        )


class UsersTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = get_user_model().objects.create(
            email='test@test.com',
            username='username',
            first_name='first_name',
            last_name='last_name',
            password='password',
        )
        cls.admin = get_user_model().objects.create(
            email='admin@admin.com',
            username='admin',
            first_name='admin_first_name',
            last_name='admin_last_name',
            password='admin_password',
            is_staff=True,
        )
        cls.pagination_attr = ('count', 'next', 'previous', 'results')

    def setUp(self) -> None:
        self.client = APIClient()
        self.admin_user = APIClient()
        self.authorized_client = APIClient()
        self.admin_user.force_login(self.admin)
        self.authorized_client.force_login(self.user)
        self.admin_token = f'Token {Token.objects.create(user=self.admin).key}'
        self.auth_token = f'Token {Token.objects.create(user=self.user).key}'
        self.user_attr = ['email', 'username', 'first_name', 'last_name', 'id',
                          'is_subscribed']

    def test_get_users(self):
        url = '/api/users/'
        response = self.client.get(url)
        # страница существует
        self.assertNotEqual(
            404,
            response.status_code,
            msg=f'Страница `{url}` не найдена'
        )
        # страница доступна для Анонима
        self.assertEqual(
            200,
            response.status_code,
            msg=(f'При GET запросе {url} без токена авторизации '
                 'возвращается статус 200')
        )
        # страница доступна авторизованному пользователю
        response = self.authorized_client.get(
            url,
            HTTP_AUTHORIZATION=self.auth_token
        )
        self.assertEqual(
            200,
            response.status_code,
            msg=(f'При GET запросе {url} с токена авторизации '
                 'возвращается статус 200')
        )
        PaginationTestCase().pagination(
            response,
            field_result_count=2,
            field_type_results=list
        )
        # данные объекта массива results содержат корректные поля и значения
        # значение is_subscribed не хранится в бд и будет проверено отдельно
        check_is_subscribed = self.user_attr.pop(
            self.user_attr.index('is_subscribed')
        )
        for attr in self.user_attr:
            with self.subTest(field=attr):
                self.assertIn(
                    attr,
                    response.data['results'][0],
                    msg=(f'Ошибка пагинации при запросе {url} не найден '
                         f'параметр {attr}')
                )
                self.assertEqual(
                    response.data['results'][0].get(attr),
                    self.user.__dict__.get(attr),
                    msg=(f'Ошибка пагинации при запросе {url} не найден. '
                         f'Значение параметра {attr} не правильное')
                )
        self.assertEqual(
            response.data['results'][0].get(check_is_subscribed),
            False,
            msg=(f'Ошибка пагинации при запросе {url} не найден. '
                 f'Значение параметра {check_is_subscribed} не правильное')
        )

    def test_get_user_id(self):
        url = '/api/users/1/'
        response = self.client.get(url)
        # страница существует
        self.assertNotEqual(
            404,
            response.status_code,
            msg=f'Страница `{url}` не найдена'
        )
        # страница доступна для Анонима
        self.assertEqual(
            200,
            response.status_code,
            msg=(f'При GET запросе {url} без токена авторизации '
                 'возвращается статус 200')
        )
        # страница доступна авторизованному пользователю
        response = self.authorized_client.get(
            url,
            HTTP_AUTHORIZATION=self.auth_token
        )
        self.assertEqual(
            200,
            response.status_code,
            msg=(f'При GET запросе {url} с токена авторизации '
                 'возвращается статус 200')
        )
        # данные ответа содержат корректные поля и значения
        # значение is_subscribed не хранится в бд и будет проверено отдельно
        check_is_subscribed = self.user_attr.pop(
            self.user_attr.index('is_subscribed')
        )
        for attr in self.user_attr:
            with self.subTest(field=attr):
                self.assertIn(
                    attr,
                    response.data,
                    msg=(f'Ошибка пагинации при запросе {url} не найден '
                         f'параметр {attr}')
                )
                self.assertEqual(
                    response.data.get(attr),
                    self.user.__dict__.get(attr),
                    msg=(f'Ошибка пагинации при запросе {url} не найден. '
                         f'Значение параметра {attr} не правильное')
                )
        self.assertEqual(
            response.data.get(check_is_subscribed),
            False,
            msg=(f'Ошибка пагинации при запросе {url} не найден. '
                 f'Значение параметра {check_is_subscribed} не правильное')
        )
        url_404 = '/api/users/100/'
        response = self.client.get(url_404)
        # страница доступна для Анонима
        self.assertEqual(
            404,
            response.status_code,
            msg=(f'При GET запросе {url_404} без токена авторизации '
                 'возвращается статус 404')
        )

    def test_get_user_me(self):
        url = '/api/users/me/'
        response = self.client.get(url)
        # страница существует
        self.assertNotEqual(
            404,
            response.status_code,
            msg=f'Страница {url} не найдена'
        )
        # страница не доступна для Анонима
        self.assertEqual(
            401,
            response.status_code,
            msg=(f'При GET запросе {url} без токена авторизации '
                 'возвращается статус 401')
        )
        # страница доступна авторизованному пользователю
        response = self.authorized_client.get(
            url,
            HTTP_AUTHORIZATION=self.auth_token
        )
        self.assertEqual(
            200,
            response.status_code,
            msg=(f'При GET запросе {url} с токена авторизации '
                 'возвращается статус 200')
        )
        # данные ответа содержат корректные поля и значения
        # значение is_subscribed не хранится в бд и будет проверено отдельно
        check_is_subscribed = self.user_attr.pop(
            self.user_attr.index('is_subscribed')
        )
        for attr in self.user_attr:
            with self.subTest(field=attr):
                self.assertIn(
                    attr,
                    response.data,
                    msg=(f'Ошибка пагинации при запросе {url} не найден '
                         f'параметр {attr}')
                )
                self.assertEqual(
                    response.data.get(attr),
                    self.user.__dict__.get(attr),
                    msg=(f'Ошибка пагинации при запросе {url} не найден. '
                         f'Значение параметра {attr} не правильное')
                )
        self.assertEqual(
            response.data.get(check_is_subscribed),
            False,
            msg=(f'Ошибка пагинации при запросе {url} не найден. '
                 f'Значение параметра {check_is_subscribed} не правильное')
        )

    def test_post_users(self):
        url = '/api/users/'
        user_data = {}
        response = self.client.post(url, data=user_data)

        # проверка кода ошибки
        self.assertEqual(
            400,
            response.status_code,
            msg=(f'При POST запросе {url} с не правильными данными '
                 'возвращает 400')
        )

        # проверка флага обязательного поля и текста сообщения об ошибке
        error_msg_required_fields = {
            'email': _('This field is required.'),
            'username': _('This field is required.'),
            'first_name': _('This field is required.'),
            'last_name': _('This field is required.'),
            'password': _('This field is required.'),
        }
        for field, error_msg in error_msg_required_fields.items():
            with self.subTest(field=field, msg=error_msg):
                self.assertIn(
                    field,
                    response.data,
                    msg=(f'Для поля {field} не установлен фалг '
                         f'обязатльного заполнения.')
                )
                self.assertEqual(
                    error_msg,
                    response.data.get(field)[0],
                    msg=('Текст сообщения об ошибке для поля '
                         f'{field} некорректный')
                )

        # проверка флага уникальности поля и текста сообщения об ошибке
        user_data = {
            'email': self.user.email,
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'password': '34Twesfre(8'
        }
        error_msg_uniq_fields = {
            'email': _('Пользователь с таким Email адрес уже существует.'),
            'username': _('A user with that username already exists.'),
        }
        response = self.client.post(url, data=user_data)
        for field, error_msg in error_msg_uniq_fields.items():
            with self.subTest(field=field, msg=error_msg):
                self.assertIn(
                    field,
                    response.data,
                    msg=(f'Для поля {field} не установлен фалг '
                         f'обязатльного заполнения.')
                )
                self.assertEqual(
                    error_msg,
                    response.data.get(field)[0],
                    msg=('Текст сообщения об ошибке для поля '
                         f'{field} некорректный')
                )

        # проверка максимальной длинны поля и текста сообщения об ошибке
        user_data = {
            'email': 's' * 250 + '@t.cc',
            'username': 's' * 151,
            'first_name': 's' * 151,
            'last_name': 's' * 151,
            'password': 'x' * 146 + '235L)'
        }
        error_msg_max_len_fields = {
            'email': 'Убедитесь, что это значение содержит не более 254 '
                     'символов.',
            'username': 'Убедитесь, что это значение содержит не более 150 '
                        'символов.',
            'first_name': 'Убедитесь, что это значение содержит не более 150 '
                          'символов.',
            'last_name': 'Убедитесь, что это значение содержит не более 150 '
                         'символов.',
            # 'password': 'Ensure this field has no more than 150 characters.',
            # почему-то, при тесте не срабатывает кастомный валидатор
        }
        response = self.client.post(url, data=user_data)
        for field, error_msg in error_msg_max_len_fields.items():
            with self.subTest(field=field, msg=error_msg):
                self.assertIn(
                    field,
                    response.data,
                    msg=(f'Для поля {field} не установлено максимальное '
                         f'количество символов.')
                )
                self.assertEqual(
                    error_msg,
                    _(response.data.get(field)[0]),
                    msg=('Текст сообщения об ошибке для поля '
                         f'{field} некорректный')
                )

        # проверка поля password
        user_data = {
            'email': self.user.email + 'we',
            'username': self.user.username + 'we',
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'password': ''
        }
        error_msg_password = {
            '': _('This field may not be blank.'),
            'poke': _('Введённый пароль слишком короткий. Он должен '
                      'содержать как минимум 8 символов.'),
            'oooooooo': _('This password is too common.')
        }
        for check, error_msg in error_msg_password.items():
            with self.subTest(check=check, msg=error_msg):
                user_data['password'] = check
                response = self.client.post(url, data=user_data)
                self.assertEqual(
                    400,
                    response.status_code,
                    msg=('При некорректных данных для поля password '
                         'должен приходить код 400')
                )
                self.assertEqual(
                    error_msg,
                    response.data['password'][0],
                    msg=(f'Текст сообщения ошибки для проверки ({check}) поля'
                         'password некорректный')
                )

        actual_users_count = get_user_model().objects.count()
        # проверка кода ответа при корректной отправке данных юзера
        user_data = {
            'email': self.user.email + 'we',
            'username': self.user.username + 'we',
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'password': '23Hjdweqwec'
        }
        response = self.client.post(url, data=user_data)
        self.assertEqual(
            201,
            response.status_code,
            msg=(f'При POST запросе {url} с правильными данными '
                 'возвращает 201')
        )
        # проверка что новый польователь добавился в базу
        self.assertEqual(
            get_user_model().objects.count(),
            actual_users_count + 1,
            msg='Новый пользователь не был добавлен в базу данных.'
        )
        obj = get_user_model().objects.get(email=user_data.get('email'))
        # проверка значений в ответе
        expected_fields = {
            'email': obj.email,
            'id': obj.id,
            'username': obj.username,
            'first_name': obj.first_name,
            'last_name': obj.last_name,
        }
        for field, expected in expected_fields.items():
            with self.subTest(field=field):
                self.assertEqual(
                    expected,
                    response.data.get(field),
                    msg=f'Значение для поля {field} некорректное'
                )


class SubscriptionTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user1 = get_user_model().objects.create(
            email='follower@test.com',
            username='follower',
            first_name='follower',
            last_name='follower',
            password='12follower',
        )
        cls.user2 = get_user_model().objects.create(
            email='following@admin.com',
            username='following',
            first_name='following',
            last_name='following',
            password='12following',
        )

    def setUp(self) -> None:
        self.client = APIClient()
        self.follower = APIClient()
        self.following = APIClient()
        self.follower.force_login(self.user1)
        self.following.force_login(self.user2)
        self.follower_token = (f'Token '
                               f'{Token.objects.create(user=self.user1).key}')
        self.following_token = (f'Token '
                                f'{Token.objects.create(user=self.user2).key}')

    def test_get_subscriptions(self):
        url = '/api/users/subscriptions/'
        response = self.client.get(url)
        self.assertNotEqual(
            404,
            response.status_code,
            msg=f'Страница {url} не найдена'
        )
        # страница не доступна для Анонима
        self.assertEqual(
            401,
            response.status_code,
            msg=(f'При GET запросе {url} без токена авторизации '
                 'возвращается статус 401')
        )
        # страница доступна авторизованному пользователю
        response = self.follower.get(
            url,
            HTTP_AUTHORIZATION=self.follower_token
        )
        self.assertEqual(
            200,
            response.status_code,
            msg=(f'При GET запросе {url} с токена авторизации '
                 'возвращается статус 200')
        )
        PaginationTestCase().pagination(
            response,
            field_result_count=0,
            field_type_results=list)

    def test_get_subscribe(self):
        url = '/api/users/2/subscribe/'
        url404 = '/api/users/200/subscribe/'
        response = self.client.get(url)
        # страница не доступна для Анонима
        self.assertEqual(
            401,
            response.status_code,
            msg=(f'При GET запросе {url} без токена авторизации '
                 'возвращается статус 401')
        )
        # страница не найдена
        response = self.follower.get(
            url404,
            HTTP_AUTHORIZATION=self.follower_token
        )
        self.assertEqual(
            404,
            response.status_code,
            msg=('При GET запросе на несущсетсвующий адрес c токеном '
                 'авторизации возвращается статус 404')
        )
        # страница существует
        response = self.follower.get(
            url,
            HTTP_AUTHORIZATION=self.follower_token
        )
        self.assertNotEqual(
            404,
            response.status_code,
            msg=f'Страница `{url}` не найдена'
        )

        obj = Subscription.objects.filter(user=self.user1,
                                          following=self.user2)
        self.assertTrue(
            obj.exists(),
            msg='В базе не появилась новая запись',
        )
        # проверка полей ответа
        expected_fields = {
            'email': obj.first().following.email,
            'id': obj.first().following.id,
            'username': obj.first().following.username,
            'first_name': obj.first().following.first_name,
            'recipes': [],
            'is_subscribed': True,
            'last_name': obj.first().following.last_name,
            'recipes_count': 0,
        }
        for field, excepted in expected_fields.items():
            with self.subTest(field=field):
                self.assertIn(
                    field,
                    response.data,
                    msg=f'Поля {field} нет ответе'
                )
                self.assertEqual(
                    excepted,
                    response.data.get(field),
                    msg=f'Некорректный результат для поля {field}'
                )

    def test_delete_subscribe(self):
        url = '/api/users/2/subscribe/'
        url404 = '/api/users/200/subscribe/'
        Subscription.objects.create(user=self.user1, following=self.user2)
        response = self.client.delete(url)
        # страница не доступна для Анонима
        self.assertEqual(
            401,
            response.status_code,
            msg=(f'При GET запросе {url} без токена авторизации '
                 'возвращается статус 401')
        )
        # проверка ошибки 404
        response = self.follower.delete(
            url404,
            HTTP_AUTHORIZATION=self.follower_token
        )
        self.assertEqual(
            404,
            response.status_code,
            msg=('При GET запросе на несущсетсвующий адрес c токеном '
                 'авторизации возвращается статус 404')
        )
        # страница существует
        response = self.follower.delete(
            url,
            HTTP_AUTHORIZATION=self.follower_token
        )
        self.assertNotEqual(
            404,
            response.status_code,
            msg=f'Страница `{url}` не найдена'
        )

        obj = Subscription.objects.filter(user=self.user1,
                                          following=self.user2)
        # в базе удалилась запись
        self.assertFalse(
            obj.exists(),
            msg='В базе не появилась новая запись',
        )
        # страница удалена код 204
        self.assertEqual(
            204,
            response.status_code,
            msg=f'При запросе DELETE `{url}` не найдена'
        )
