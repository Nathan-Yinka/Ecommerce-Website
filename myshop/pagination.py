from rest_framework.pagination import PageNumberPagination as Pagination


class ProductPageNumberPagination(Pagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100