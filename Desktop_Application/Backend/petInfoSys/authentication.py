from rest_framework.authentication import SessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    Session authentication without CSRF validation for cross-site API calls.
    Use this for JSON APIs where the frontend is on a different domain.
    """
    def enforce_csrf(self, request):
        return  # Skip CSRF check
