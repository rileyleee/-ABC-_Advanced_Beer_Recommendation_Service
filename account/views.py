from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from account.forms import SignupForm

MAX_LIST_CNT = 5
MAX_PAGE_CNT = 1

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
            messages.success(request, "성공적으로 수정되었습니다.")

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
    mybeers = user.like_beers.all()
    paginator = Paginator(mybeers, MAX_LIST_CNT)
    page = request.GET.get('page', 1)
    pagenated_mybeers = paginator.get_page(page)

    last_page_num = 0
    for last_page in paginator.page_range:
        last_page_num = last_page_num + 1
        # 현재 페이지가 몇번째 블럭인지
        current_block = ((int(page) - 1) / MAX_PAGE_CNT) + 1
        current_block = int(current_block)
        # 페이지 시작번호
        page_start_number = ((current_block - 1) * MAX_PAGE_CNT) + 1
        # 페이지 끝 번호
        page_end_number = page_start_number + MAX_PAGE_CNT - 1

    context_mybeers = {'last_page_num': last_page_num,
                         'page_start_number': page_start_number,
                         'page_end_number': page_end_number,
                         'pagenated_mybeers': pagenated_mybeers,
                         'person': user,}
    return render(request, 'account/mypage.html',context=context_mybeers)

