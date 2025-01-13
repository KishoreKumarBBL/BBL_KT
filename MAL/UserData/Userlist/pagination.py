from rest_framework.pagination import PageNumberPagination

class pagestyle(PageNumberPagination):
    page_size = 2
    page_query_param = 'limit'  