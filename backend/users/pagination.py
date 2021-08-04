from rest_framework.pagination import PageNumberPagination


class ListLimitPagination(PageNumberPagination):
    page_size_query_param = 'limit'
