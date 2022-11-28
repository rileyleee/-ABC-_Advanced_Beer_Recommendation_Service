from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from account.forms import SignupForm

login = LoginView.as_view(template_name="account/login.html")

logout = LogoutView.as_view(next_page="/account/login/")


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 로그인
            return redirect('/account/login/')
    else:
        form = SignupForm()
    return render(request, 'account/signup.html', {
        'form': form,
    })


# 오승이네 코드
# signup = CreateView.as_view(
#     form_class=SignupForm,
#     success_url="/account/login/",
#     template_name="account/signup.html",
# )
@login_required
def mypage_edit(request):
    user = request.user
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            # form.cleaned_data
            user = form.save()
            messages.success(request, "successfully modified")

            return redirect(f"/account/mypage/")  # 마이페이지가 로그인 필수사항이라 로그인 요청 뜸
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


@login_required
def mybeer(request):
    user = request.user
    mybeers = user.like_beers.all()
    return render(request, 'account/mybeerlist.html',
                  {'person': user, 'mybeers': mybeers})
