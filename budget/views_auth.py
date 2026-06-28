import io, base64, qrcode
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django_otp.plugins.otp_totp.models import TOTPDevice


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
            if not TOTPDevice.objects.filter(user=user, confirmed=True).exists():
                return redirect('/setup-otp/')
            return redirect('/verify-otp/')
        else:
            error = 'Identifiants incorrects.'
    return render(request, 'budget/login.html', {'error': error})


@login_required
def verify_otp_view(request):
    device = TOTPDevice.objects.filter(user=request.user, confirmed=True).first()
    if not device:
        return redirect('/setup-otp/')
    error = None
    if request.method == 'POST':
        token = request.POST.get('token', '').replace(' ', '')
        if device.verify_token(token):
            request.session['otp_verified'] = True
            return redirect('/')
        else:
            error = 'Code incorrect. Réessayez.'
    return render(request, 'budget/verify_otp.html', {'error': error})


@login_required
def setup_otp_view(request):
    user = request.user
    device, _ = TOTPDevice.objects.get_or_create(user=user, defaults={'name': 'default'})
    if request.method == 'POST':
        token = request.POST.get('token', '').replace(' ', '')
        if device.verify_token(token):
            device.confirmed = True
            device.save()
            request.session['otp_verified'] = True
            return redirect('/')
        return render(request, 'budget/setup_otp.html', {
            'error': 'Code incorrect. Scannez à nouveau le QR.',
            'qr_url': _get_qr(device, user)
        })
    return render(request, 'budget/setup_otp.html', {'qr_url': _get_qr(device, user)})


def _get_qr(device, user):
    uri = device.config_url
    img = qrcode.make(uri)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()


def logout_view(request):
    request.session.flush()
    logout(request)
    return redirect('/login/')