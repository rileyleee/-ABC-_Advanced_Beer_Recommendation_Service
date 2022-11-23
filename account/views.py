from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from account.forms import SignupForm

login = LoginView.as_view(template_name="search/search_page.html")

logout = LogoutView.as_view(next_page="/account/login/")

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 로그인
            return redirect('/search/')
    else:
        form = SignupForm()
    return render(request, 'account/signup.html', {'form': form})

def mypage_edit(request):
    user = request.user
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            # form.cleaned_data
            user = form.save()
            messages.success(request, "successfully modified")

            return redirect(f"/account/mypage/")
    else:
        form = SignupForm(instance=user)

    return render(request, "account/mypage_edit.html", {
        "form": form,
    })

@login_required
@require_http_methods(['GET', 'POST'])
def mypage(request):
    user = request.user
    return render(request, 'account/mypage.html',
                  {'person': user})