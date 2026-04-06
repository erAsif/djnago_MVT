from django.shortcuts           import render, redirect
from django.contrib.auth        import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib              import messages
from .forms                     import SignupForm, LoginForm, ProfileUpdateForm
from django.views.decorators.cache import never_cache


# ── 1. HOME VIEW ────────────────────────────────────────────────
def home_view(request):
    return render(request, 'accounts/home.html')


# ── 2. SIGNUP VIEW ──────────────────────────────────────────────
def signup_view(request):

    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()                   #  save in DB
            # login(request, user,                  # auto login after signup
            #       backend='accounts.backends.EmailBackend')
            messages.success(request,
                f'Welcome {user.username}! Account created!')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = SignupForm()  # GET request → empty form

    return render(request, 'accounts/signup.html', {'form': form})


# ── 3. LOGIN VIEW (Email + Password) ────────────────────────────
def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email    = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request,
                       username=email,   # email as username!
                       password=password)
            if user is not None:
                login(request, user)

                # Remember Me — session expiry for browser close
                if not form.cleaned_data.get('remember_me'):
                    request.session.set_expiry(0)  # browser band = logout

                messages.success(request,
                    f'Welcome back, {user.username}!')
                return redirect('accounts:profile')
            else:
                messages.error(request,
                    'Invalid email or password.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


# ── 4. LOGOUT VIEW ──────────────────────────────────────────────
@login_required
def logout_view(request):
    if request.method == 'POST':  # POST only — security!
        logout(request)
        messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')


# ── 5. PROFILE VIEW ─────────────────────────────────────────────
@never_cache
@login_required  # not allow without login
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST,
            # request.FILES,          # for profile_img 
            instance=request.user   # update current user's data
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request,
        'accounts/profile.html',
        {'form': form, 'user': request.user})
    