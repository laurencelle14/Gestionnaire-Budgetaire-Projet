from django.shortcuts import redirect

class OTPRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    EXEMPT_PREFIXES = (
        '/login/',
        '/verify-otp/',
        '/setup-otp/',
        '/logout/',
        '/admin/',
        '/static/',
        '/media/',
        '/favicon.ico',
    )

    def __call__(self, request):
        if not any(request.path.startswith(p) for p in self.EXEMPT_PREFIXES):
            if not request.user.is_authenticated:
                return redirect('/login/')
            if not request.session.get('otp_verified'):
                return redirect('/verify-otp/')

        return self.get_response(request)