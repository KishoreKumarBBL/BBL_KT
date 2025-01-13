from rest_framework.pagination import PageNumberPagination

class Custompagesettings(PageNumberPagination):
    page_size = 2
    page_query_param = 'page_limit'
    max_page_size =20
    