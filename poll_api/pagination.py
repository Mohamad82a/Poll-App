from rest_framework.pagination import PageNumberPagination
from django.conf import settings

class CustomPageNumberPagination(PageNumberPagination):
    page_size = getattr(settings, 'PAGINATION_DEFAULT_PAGE_SIZE', 2)

