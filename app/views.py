from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.views.decorators.cache import never_cache
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.conf import settings


# Create your views here.
def home(request):
    return render(request, 'home.html')


def SignUp(request):
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        username = request.POST['email']
        
        if User.objects.filter(email=email).exists():
            return redirect('app:SignIn')
        
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)

        login(request, user)  

        return redirect('app:home')

    return render(request, 'SignUp.html')



def SignIn(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'app:home')
            return redirect(next_url)
        
        return redirect('app:SignIn')
    
    return render(request, 'SignIn.html')


@login_required
def SignOut(request):
    logout(request)
    response = HttpResponseRedirect(reverse('app:home'))
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


@login_required
@never_cache  
def profile(request):
    d = {'user': request.user}
    return render(request, 'profile.html', d)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            return redirect('app:profile')
    else:
        form = PasswordChangeForm(request.user)
    
    d = {'form': form}
    return render(request, 'change_password.html', d)


def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            # Generate password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Create reset URL
            reset_url = f"{request.build_absolute_uri('/reset-password/')}{uid}/{token}/"

            # Send email
            subject = "Password Reset Request"
            message = render_to_string('emails/password_reset_email.html', {'reset_url': reset_url, 'user': user})
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

            messages.success(request, "A password reset link has been sent to your email.")
        else:
            messages.error(request, "No account found with this email.")

        return redirect('app:forgot_password')

    return render(request, 'forgot_password.html')