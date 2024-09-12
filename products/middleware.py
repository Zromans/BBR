import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class LoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        logger.info(f"Request: {request.method} {request.path}")

    def process_response(self, request, response):
        logger.info(f"Response: {response.status_code}")
        return response
