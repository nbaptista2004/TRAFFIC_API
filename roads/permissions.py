from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class HasSensorApiKey(BasePermission):
    API_KEY = "23231c7a-80a7-4810-93b3-98a18ecfbc42"

    def has_permission(self, request, view):
        api_key = request.headers.get("X-API-KEY")
        if api_key != self.API_KEY:
            raise PermissionDenied("Invalid API Key")
        return True
