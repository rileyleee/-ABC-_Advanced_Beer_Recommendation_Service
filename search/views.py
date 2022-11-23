from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from search.models import Beer
from math import pi
import matplotlib.pyplot as plt
import random
import logging
import pandas as pd
from search.ml import beer_model

logger = logging.getLogger('tipper')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


# @csrf_exempt  # CSRF Token 체크를 하지 않겠습니다.
def search(request):
    # TODO: 2개의 뷰로 분리하는 것이 낫습니다. => 그럼 아래의 조건문이 필요가 없고, 보다 뷰가 간결해집니다.

    beer_list = Beer.objects.all()
    paginator = Paginator(beer_list, '20')
    page = request.GET.get('page', 1)
    pagenated_beer_list = paginator.get_page((page))
    query = request.GET.get('search', '')  # 일반적으로는 q나 query이름을 씁니다.
    ch_category_list = request.GET.getlist("chCategory")
    ch_country_list = request.GET.getlist("chCountry")
    if query or ch_category_list or ch_country_list:
        if query:
            beer_list = beer_list.filter(
                Q(name__icontains=query) |
                Q(brewery__icontains=query) |
                Q(country__icontains=query)
            )
        if ch_category_list:
            beer_list = beer_list.filter(
                Q(big_kind__in=ch_category_list)
            )
        if ch_country_list:
            beer_list = beer_list.filter(
                Q(country__in=ch_country_list)
            )
        template_name = "search/search_list.html"
    else:
        template_name = "search/search_page.html"

    user_feature = [
        request.GET.get('sweet'),
        request.GET.get('body'),
        request.GET.get('fruit'),
        request.GET.get('hoppy'),
        request.GET.get('malty'),
    ]
    if all(user_feature) is False:
        predict_beer = None
    else:
        user_feature = list(map(float, user_feature))
        predict_beer = beer_model.predict(user_feature)
    kind_list = Beer.objects.all().order_by('-reviews')
    if predict_beer:
        kind_list = kind_list.filter(
            Q(kind__icontains=predict_beer))[:10]

    context_beer_list = {'beer_list': beer_list, 'pagenated_beer_list': pagenated_beer_list, 'search': query,
                         'predict_beer': predict_beer, 'kind_list': kind_list}

    return render(request, template_name, context=context_beer_list)


@login_required
def search_detail(request, pk):
    search_detail = Beer.objects.get(id=pk)

    df = pd.read_csv('final_train_beer_ratings_Ver_rader model.csv', encoding='utf-8', index_col=0)
    aaa = df['Full Name'].iloc[pk]
    cc = df[df['Full Name'] == '%s' % aaa]

    cc = cc[
        ['Astringent', 'Body', 'Alcoholic', 'Bitter', 'Sweet', 'Sour', 'Salty', 'Fruity', 'Hoppy', 'Spices', 'Malty']]
    dfR = cc
    n = 0
    angles = [x / 11 * (2 * pi) for x in range(11)]  # 각 등분점
    angles += angles[:1]  # 시작점으로 다시 돌아와야하므로 시작점 추가
    my_palette = plt.cm.get_cmap("Set2", 11)
    fig = plt.figure(figsize=(8, 8), dpi=100)
    fig.set_facecolor('white')
    color = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])][0]
    labels = dfR.columns[:]

    data = dfR.iloc[0].tolist()
    data += data[:1]

    ax = plt.subplot(1, 1, 1, polar=True)
    ax.set_theta_offset(pi / 2)  # 시작점
    ax.set_theta_direction(-1)  # 그려지는 방향 시계방향

    plt.xticks(angles[:-1], labels, fontsize=13)  # x축 눈금 라벨
    ax.tick_params(axis='x', which='major', pad=15)  # x축과 눈금 사이에 여백을 준다.

    ax.set_rlabel_position(0)  # y축 각도 설정(degree 단위)
    plt.yticks([-4, 0, 4, 7], ['', '', '', ''], fontsize=10)  # y축 눈금 설정
    plt.ylim(-4, 7)

    ax.plot(angles, data, color=color, linewidth=2, linestyle='solid')  # 레이더 차트 출력
    ax.fill(angles, data, color=color, alpha=0.4)  # 도형 안쪽에 색을 채워준다.

    plt.title('', size=13, color=color, x=0.5, y=1, ha='center')  # 타이틀은 캐릭터 클래스로 한다.

    plt.tight_layout(pad=5)  # subplot간 패딩 조절

    plt.savefig('static/beerimg.png')

    return render(request, "search/search_detail.html", {
        "search_details": search_detail,
    })


def recommend(request):
    review_ranking = Beer.objects.all().order_by('-reviews')[:10]
    average_ranking = Beer.objects.all().order_by('-average')[:10]
    return render(
        request,
        'search/recommend.html',
        {'review_ranking': review_ranking, 'average_ranking': average_ranking}
    )
