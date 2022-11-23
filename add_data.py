# Shop 저장
import csv
import os
import django
import re

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beer_recommend_prj.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
from search.models import Beer

beer = Beer()
beer_list = []

with open('final_proj_train_beer_ratings.csv', encoding='utf8') as csv_file_beer:
    rows = csv.reader(csv_file_beer)
    next(rows, None)
    for row in rows:
        big_kind = row[0]
        kind = row[1]
        name = row[2]
        brewery = row[3]
        country = row[4]
        abv = row[5]
        average = row[6]
        reviews = row[7]
        ratings = row[8]
        status = row[9]
        body = row[12]
        sweet = row[15]
        fruity = row[18]
        hoppy = row[19]
        malty = row[21]

        beer = Beer(
                    big_kind=big_kind,
                    kind=kind,
                    name=name,
                    brewery=brewery,
                    country=country,
                    abv=abv,
                    average=average,
                    ratings=ratings,
                    reviews=reviews,
                    status=status,
                    body=body,
                    sweet=sweet,
                    fruity=fruity,
                    hoppy=hoppy,
                    malty=malty,
        )
        beer_list.append(beer)

        print(name)
print(len(beer_list))
Beer.objects.bulk_create(beer_list)
Beer.objects.all().count()
