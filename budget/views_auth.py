import random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta


def login_view(request):
    if request.user.is_authenticated and request.session.get('otp_verified'):
        return redirect('/')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # Générer et envoyer le code OTP
            code = str(random.randint(100000, 999999))
            request.session['otp_code'] = code
            request.session['otp_expiry'] = str(timezone.now() + timedelta(minutes=10))
            send_mail(
                subject='Votre code de connexion',
                message=f'Votre code OTP est : {code}\n\nIl expire dans 10 minutes.',
                from_email=None,
                recipient_list=[user.email],
            )
            return redirect('/verify-otp/')
        else:
            error = 'Identifiants incorrects.'
    return render(request, 'budget/login.html', {'error': error})


@login_required
def verify_otp_view(request):
    error = None
    if request.method == 'POST':
        token = request.POST.get('token', '').strip()
        code = request.session.get('otp_code')
        expiry = request.session.get('otp_expiry')

        if not code or not expiry:
            return redirect('/login/')

        from datetime import datetime
        expiry_dt = datetime.fromisoformat(expiry)
        if timezone.now() > expiry_dt:
            error = 'Code expiré. Reconnectez-vous.'
        elif token == code:
            request.session['otp_verified'] = True
            del request.session['otp_code']
            del request.session['otp_expiry']
            return redirect('/')
        else:
            error = 'Code incorrect. Réessayez.'

    return render(request, 'budget/verify_otp.html', {'error': error})


def logout_view(request):
    request.session.flush()
    logout(request)
    return redirect('/login/')