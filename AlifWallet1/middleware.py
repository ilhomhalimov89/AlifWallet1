
import hashlib
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_id = request.headers.get('X-UserId')
        digest = request.headers.get('X-Digest')
        if user_id is None or digest is None:
            return JsonResponse({'error': 'Authentication headers missing'}, status=401)
        
        request_body = request.body
        calculated_digest = hashlib.sha1(request_body).hexdigest()
        if digest != calculated_digest:
            return JsonResponse({'error': 'Invalid digest'}, status=401)
