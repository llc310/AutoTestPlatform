from rest_framework import pagination
from rest_framework.response import Response


class PageNumberPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'itemCount': self.page.paginator.count,
            'pageCount': self.page.paginator.num_pages,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'list': data,
        })
