from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from search.models import Beer
from math import pi
import matplotlib.pyplot as plt
import random
import logging
import pandas as pd
from search.ml import beer_model

MAX_LIST_CNT = 30
MAX_PAGE_CNT = 5

logger = logging.getLogger('tipper')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


def keyword(request):
    beer_list = Beer.objects.all()
    keyword = request.GET.get('keyword', '')

    if keyword:
        beer_list = beer_list.filter(
            Q(name__icontains=keyword) |
            Q(brewery__icontains=keyword) |
            Q(country__icontains=keyword)
        )

        template_name = "search/keyword_list.html"
    else:
        template_name = "search/keyword_page.html"

    paginator = Paginator(beer_list, MAX_LIST_CNT)
    page = request.GET.get('page', 1)
    pagenated_beer_list = paginator.get_page(page)

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

    context_beer_list = {'last_page_num': last_page_num,
                         'page_start_number': page_start_number,
                         'page_end_number': page_end_number,
                         'pagenated_beer_list': pagenated_beer_list,
                         'keyword': keyword}
    # print(keyword)
    return render(request, template_name, context=context_beer_list)


# @csrf_exempt  # CSRF Token 체크를 하지 않겠습니다.
def search(request):
    beer_list = Beer.objects.all()
    ch_category_list = request.GET.getlist("chCategory")
    ch_country_list = request.GET.getlist("chCountry")
    search_keyword = request.GET.get('search_keyword', '')

    if ch_category_list or ch_country_list:
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

        if search_keyword:
            beer_list = beer_list.filter(
                Q(name__icontains=search_keyword) |
                Q(brewery__icontains=search_keyword) |
                Q(country__icontains=search_keyword)
            )
            template_name = "search/keyword_list.html"
        else:
            template_name = "search/search_page.html"

    paginator = Paginator(beer_list, MAX_LIST_CNT)
    page = request.GET.get('page', 1)
    pagenated_beer_list = paginator.get_page(page)

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

    if ch_category_list or ch_country_list:
        if ch_category_list:
            ch_category_list = ch_category_list[0]
        if ch_country_list:
            ch_country_list = ch_country_list[0]
    else:
        pass

    context_beer_list = {'last_page_num': last_page_num,
                         'page_start_number': page_start_number,
                         'page_end_number': page_end_number,
                         'ch_category_list': ch_category_list,
                         'ch_country_list': ch_country_list,
                         'keyword': search_keyword,
                         'pagenated_beer_list': pagenated_beer_list}

    return render(request, template_name, context=context_beer_list)


def predict(request):
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

        df = pd.read_csv('final_proj_train_beer_ratings.csv')
        gf = ''
        print(df)
        df = df.drop(['스타일대분류', '양조장명', '제조국가명', '도수', '평균점수', '리뷰수', '현재상태', '평가수', 'Full Name'], axis=1)
        df['스타일소분류'] = df['스타일소분류'].str.replace(' ', '')
        print(predict_beer)
        gf = df[df['스타일소분류'] == predict_beer]
        print(gf)
        my_favor = pd.DataFrame(columns=['Body', 'Sweet', 'Fruity', 'Hoppy', 'Malty'])
        my_input = user_feature
        my_favor.loc[my_favor.shape[0] + 1] = my_input
        gf = gf.drop(['Astringent', 'Alcoholic', 'Bitter', 'Sour', 'Salty', 'Spices'], axis=1)
        print(gf)
        df_ac = pd.concat([gf, my_favor])
        df_ac.fillna(0)
        df_ac.fillna({'스타일소분류': 'recommand'}, inplace=True)
        df_ac = df_ac.astype({'Body': 'float64'})  ## 데이터 타입 바꿔 주기
        df_ac = df_ac.astype({'Sweet': 'float64'})
        df_ac = df_ac.astype({'Fruity': 'float64'})  ## 데이터 타입 바꿔 주기
        df_ac = df_ac.astype({'Hoppy': 'float64'})
        df_ac = df_ac.astype({'Malty': 'float64'})

        df_ab = df_ac.reset_index()

        a = df_ab['스타일소분류'].str.contains('recommand')
        # 해당 지역의 인덱스 찾기
        df2 = df_ab[a]
        print(df2.iloc[0])
        df2 = df2.drop(['index'], axis=1)
        print(df2)
        df3 = df2.drop(['스타일소분류', '맥주명'], axis=1)
        print("--------------------")
        df_ac = df_ac.sub(df3.iloc[0], axis=1)
        df_ad = df_ac.sum(axis=1)
        print(df_ab)
        print(df_ad)

        df_name = df_ab['맥주명']

        df_final = pd.DataFrame(df_name, columns=['맥주명']).reset_index(drop=True)

        df_af = pd.DataFrame(df_ad, columns=['수치']).reset_index(drop=True)

        e = pd.concat([df_final, df_af], axis=1)

        e['수치'] = e['수치'].abs()
        f = e.sort_values(by=['수치']).reset_index(drop=True)

        ffinal = f['맥주명'].iloc[1:6].to_list()
        print(ffinal)

        prename_list = Beer.objects.all()

        if ffinal:
            prename_list = prename_list.filter(
                Q(name__in=ffinal))[:5]

    else:
        prename_list = ''
    return render(request, "search/recommend.html",
                  {'predict_beer': predict_beer, 'kind_list': kind_list, 'prename_list': prename_list})


@login_required
def search_detail(request, pk):
    name_list = ''

    search_detail = Beer.objects.get(id=pk)

    import matplotlib
    import matplotlib.font_manager as fm

    fm.get_fontconfig_fonts()
    font_location = 'C:\Windows\Fonts\malgun.ttf'  # For Windows
    font_name = fm.FontProperties(fname=font_location).get_name()
    matplotlib.rc('font', family=font_name)

    df = pd.read_csv('final_train_beer_ratings_Ver_rader model1.csv', encoding='utf-8-sig', index_col=0)
    aaa = df['Full Name'].iloc[pk]
    cc = df[df['Full Name'] == '%s' % aaa]

    cc = cc[
        ['Body', 'Sweet', 'Fruity', 'Hoppy', 'Malty']]
    cc = cc.rename(columns={'Body': '바디감', 'Sweet': '당도', 'Fruity': '과일향', 'Hoppy': '홉향', 'Malty': '맥아향'})
    dfR = cc
    n = 0
    angles = [x / 5 * (2 * pi) for x in range(5)]  # 각 등분점
    angles += angles[:1]  # 시작점으로 다시 돌아와야하므로 시작점 추가
    my_palette = plt.cm.get_cmap("Set2", 5)
    fig = plt.figure(figsize=(8, 8), dpi=100)
    fig.set_facecolor('white')
    color = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])][0]
    labels = dfR.columns[:]

    data = dfR.iloc[0].tolist()
    data += data[:1]

    ax = plt.subplot(1, 1, 1, polar=True)
    ax.set_theta_offset(pi / 2)  # 시작점
    ax.set_theta_direction(-1)  # 그려지는 방향 시계방향

    plt.xticks(angles[:-1], labels, fontsize=27)  # x축 눈금 라벨
    ax.tick_params(axis='x', which='major', pad=30)  # x축과 눈금 사이에 여백을 준다.

    ax.set_rlabel_position(0)  # y축 각도 설정(degree 단위)
    plt.yticks([-1, 0, 1, 3, 5], ['', '', '', '', ''], fontsize=10)  # y축 눈금 설정
    plt.ylim(-1, 5)

    ax.plot(angles, data, color=color, linewidth=2, linestyle='solid')  # 레이더 차트 출력
    ax.fill(angles, data, color=color, alpha=0.4)  # 도형 안쪽에 색을 채워준다.

    plt.title('', size=20, color=color, x=0.5, y=1, ha='center')  # 타이틀은 캐릭터 클래스로 한다.

    plt.tight_layout(pad=5)  # subplot간 패딩 조절

    plt.savefig('static/beerimg.png')

    # ------------------------------

    df = pd.read_csv('final_proj_train_beer_ratings.csv')
    gn = ''

    df = df.drop(['스타일대분류', '양조장명', '제조국가명', '도수', '평균점수', '리뷰수', '현재상태', '평가수', 'Full Name'], axis=1)

    gf = df[df['스타일소분류'] == search_detail.kind]

    my_favor = pd.DataFrame(columns=['맥주명', 'Body', 'Sweet', 'Fruity', 'Hoppy', 'Malty'])
    f0 = search_detail.name
    f1 = search_detail.body  # value 넣기
    f2 = search_detail.sweet
    f3 = search_detail.fruity
    f4 = search_detail.hoppy
    f5 = search_detail.malty
    my_input = [f0, f1, f2, f3, f4, f5]
    my_favor.loc[my_favor.shape[0] + 1] = my_input
    gf = gf.drop(['Astringent', 'Alcoholic', 'Bitter', 'Sour', 'Salty', 'Spices'], axis=1)
    df_ac = pd.concat([gf, my_favor])
    df_ac = df_ac.astype({'Body': 'int64'})  ## 데이터 타입 바꿔 주기
    df_ac = df_ac.astype({'Sweet': 'int64'})
    df_ac = df_ac.astype({'Fruity': 'int64'})  ## 데이터 타입 바꿔 주기
    df_ac = df_ac.astype({'Hoppy': 'int64'})
    df_ac = df_ac.astype({'Malty': 'int64'})

    df_ab = df_ac.reset_index()

    a = df_ab['맥주명'].str.contains(search_detail.name)  # 해당 지역의 인덱스 찾기

    df2 = df_ab[a]

    df2 = df2.drop(['index'], axis=1)
    df3 = df2.drop(['스타일소분류', '맥주명'], axis=1)
    print("--------------------")
    df_ac = df_ac.sub(df3.iloc[0], axis=1)
    df_ad = df_ac.sum(axis=1)

    df_name = df_ab['맥주명']

    df_final = pd.DataFrame(df_name, columns=['맥주명']).reset_index(drop=True)

    df_af = pd.DataFrame(df_ad, columns=['수치']).reset_index(drop=True)

    e = pd.concat([df_final, df_af], axis=1)

    e['수치'] = e['수치'].abs()
    f = e.sort_values(by=['수치'])
    f.drop_duplicates()
    for ex in f['맥주명']:
        if search_detail.name not in ex:
            final = f
        else:
            final = ''

    ffinal = final.iloc[0:11]

    fffinal = ffinal['맥주명'].to_list()
    print(fffinal)
    name_list = Beer.objects.all()
    # ---------------------
    if fffinal:
        name_list = name_list.filter(
            Q(name__in=fffinal))[:10]

    return render(request, "search/search_detail.html", {
        "search_details": search_detail, "name_list": name_list
    })


def ranking(request):
    review_ranking = Beer.objects.all().order_by('-reviews')[:10]
    average_ranking = Beer.objects.all().order_by('-average')[:10]

    return render(
        request,
        'search/ranking_beer.html',
        {'review_ranking': review_ranking, 'average_ranking': average_ranking}
    )


@login_required  # 좋아요 구현
def like(request, pk):
    beer = get_object_or_404(Beer, id=pk)

    if request.user in beer.like_users.all():
        beer.like_users.remove(request.user)
        beer.like_count -= 1
        beer.save()
    else:
        beer.like_users.add(request.user)
        beer.like_count += 1
        beer.save()

    return redirect('search:beerprofile', pk)
