from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10
    
    def get_paginated_response(self, data):
        return Response({
            'data': data,
            'current_page': self.page.number,
            'next_page': self.get_next_link(),
            'total': self.page.paginator.count,
        })
