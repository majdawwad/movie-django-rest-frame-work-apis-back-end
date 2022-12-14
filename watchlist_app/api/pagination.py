from rest_framework import pagination

from watchlist_app.models import WatchList


class WatchListPaginationNumber(pagination.PageNumberPagination):
    page_size = 3
    #page_query_param = 'page_number'
    page_size_query_param = 'size'
    max_page_size = 10
    #last_page_strings = 'end'


class WatchListPaginationLimitOffset(pagination.LimitOffsetPagination):
    default_limit = 5
    max_limit = 7
    limit_query_param = 'limit'
    offset_query_param = 'start'


class WatchListPaginationCursor(pagination.CursorPagination):
    page_size = 5
    ordering = 'created'
    #cursor_query_param = 'record'
