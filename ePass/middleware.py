from typing import Any

from django.http import JsonResponse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response


class JsonResponseMiddleware:
    def __init__(self, get_response: Any) -> None:
        self.get_response = get_response

    def __call__(self, request: Request) -> Response | JsonResponse:
        response = self.get_response(request)
        if response.status_code == 404:
            return JsonResponse(data={'error': 'Wrong API endpoint'}, status=status.HTTP_404_NOT_FOUND)
        return response
