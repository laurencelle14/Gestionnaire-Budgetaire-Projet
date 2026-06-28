from django.shortcuts import redirect

class OTPRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        exempt = ['/login/', '/verify-otp/', '/setup-otp/', '/logout/']
        if request.path not in exempt:
            if not request.user.is_authenticated:
                return redirect('/login/')
            if not request.session.get('otp_verified'):
                return redirect('/verify-otp/')
        return self.get_response(request)