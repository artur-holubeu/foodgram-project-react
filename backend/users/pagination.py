from rest_framework.pagination import PageNumberPagination


class UsersListPagination(PageNumberPagination):
    page_size_query_param = 'limit'
