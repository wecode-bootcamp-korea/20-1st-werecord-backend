import os, django, csv, sys, random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "werecord.settings")
django.setup()

from records.models import *
from users.models   import *

CSV_PATH_PRODUCTS = './message.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)

    # shoes1_1 = "https://i.postimg.cc/Qd10J6xf/shoes1-1.png"
    # shoes1_2 = "https://i.postimg.cc/Gt4j8K5J/shoes1-2.png"

    # shoes2_1 = "https://i.postimg.cc/cJWT9Qv0/shoes2-1.png"
    # shoes2_2 = "https://i.postimg.cc/SKGdwJ98/shoes2-2.png"

    # shoes3_1 = "https://i.postimg.cc/j2B4zNVV/shoes3-1.png"
    # shoes3_2 = "https://i.postimg.cc/1RdBhx8W/shoes3-2.png"

    # shoes4_1 = "https://i.postimg.cc/vBHhMb7K/shoes4-1.png"
    # shoes4_2 = "https://i.postimg.cc/HxZ2kRBk/shoes4-2.png"

    # for i in range(4, 76, 4):
    #     a = ProductImage.objects.filter(product_id=i).all().first()
    #     a.image_url = shoes4_1
    #     a.save()
    #     a = ProductImage.objects.filter(product_id=i).all().last()
    #     a.image_url = shoes4_2
    #     a.save()

    # for i in range(1, 76):
    #     for j in ["250", "260", "270", "280", "290"]:
    #         ProductOption.objects.create(product_id=i, size=j)

    # 1 3-4-5
    # 2 2-3-4
    # 3 1-2-3

    # for i in range(1, 376, 5):
    #     price = (random.randrange(1, 1001))*10000
    #     selling_informations = ProductOption.objects.get(id=i).sellinginformation_set.all()

    #     while price in [int(selling_information.price) for selling_information in selling_informations]:
    #         price = (random.randrange(1, 1001))*10000

    #     SellingInformation.objects.create(
    #         user_id=3,
    #         product_option_id=i,
    #         status_id=2,
    #         price=price)
    
    # 1 1-2
    # 2 1-5
    # 3 4-5

    # for i in range(5, 376, 5):
    #     price                = (random.randrange(1, 1001))*10000
    #     selling_informations = ProductOption.objects.get(id=i).sellinginformation_set.all()
    #     buying_informations  = ProductOption.objects.get(id=i).buyinginformation_set.all()

    #     prices = []

    #     for selling_information in selling_informations:
    #         prices.append(int(selling_information.price))
    #     for buying_information in buying_informations:
    #         prices.append(int(buying_information.price))

    #     while price in prices:
    #         price = (random.randrange(1, 1001))*10000

    #     BuyingInformation.objects.create(
    #         user_id=3,
    #         product_option_id=i,
    #         status_id=2,
    #         price=price)

    # 1 2, 1 3, 2 1, 2 3, 3 1, 3 2,

    # for i in range(1, 376, 6):
    #     price                = (random.randrange(1, 1001))*10000
    #     selling_informations = ProductOption.objects.get(id=i).sellinginformation_set.all()
    #     buying_informations  = ProductOption.objects.get(id=i).buyinginformation_set.all()

    #     prices = []

    #     for selling_information in selling_informations:
    #         prices.append(int(selling_information.price))
    #     for buying_information in buying_informations:
    #         prices.append(int(buying_information.price))

    #     while price in prices:
    #         price = (random.randrange(1, 1001))*10000

    #     buying = BuyingInformation.objects.create(
    #         user_id=1,
    #         product_option_id=i,
    #         status_id=1,
    #         price=price)

    #     selling = SellingInformation.objects.create(
    #         user_id=2,
    #         product_option_id=i,
    #         status_id=1,
    #         price=price)

    #     Order.objects.create(buying_information=buying, selling_information=selling)

    # for i in range(2, 376, 6):
    #     price                = (random.randrange(1, 1001))*10000
    #     selling_informations = ProductOption.objects.get(id=i).sellinginformation_set.all()
    #     buying_informations  = ProductOption.objects.get(id=i).buyinginformation_set.all()

    #     prices = []

    #     for selling_information in selling_informations:
    #         prices.append(int(selling_information.price))
    #     for buying_information in buying_informations:
    #         prices.append(int(buying_information.price))

    #     while price in prices:
    #         price = (random.randrange(1, 1001))*10000

    #     buying = BuyingInformation.objects.create(
    #         user_id=1,
    #         product_option_id=i,
    #         status_id=1,
    #         price=price)

    #     selling = SellingInformation.objects.create(
    #         user_id=3,
    #         product_option_id=i,
    #         status_id=1,
    #         price=price)

    #     Order.objects.create(buying_information=buying, selling_information=selling)

    # for i in range(3, 376, 6):
    #     price                = (random.randrange(1, 1001))*10000
    #     selling_informations = ProductOption.objects.get(id=i).sellinginformation_set.all()
    #     buying_informations  = ProductOption.objects.get(id=i).buyinginformation_set.all()

    #     prices = []

    #     for selling_information in selling_informations:
    #         prices.append(int(selling_information.price))
    #     for buying_information in buying_informations:
    #         prices.append(int(buying_information.price))

    #     while price in prices:
    #         price = (random.randrange(1, 1001))*10000

    #     buying = BuyingInformation.objects.create(
    #         user_id=2,
    #         product_option_id=i,
    #         status_id=1,
    #         price=price)

    #     selling = SellingInformation.objects.create(
    #         user_id=1,
    #         product_option_id=i,
    #         status_id=1,
    #         price=price)

    #     Order.objects.create(buying_information=buying, selling_information=selling)

    # for i in range(4, 376, 6):
    #     price                = (random.randrange(1, 1001))*10000
    #     selling_informations = ProductOption.objects.get(id=i).sellinginformation_set.all()
    #     buying_informations  = ProductOption.objects.get(id=i).buyinginformation_set.all()

    #     prices = []

    #     for selling_information in selling_informations:
    #         prices.append(int(selling_information.price))
    #     for buying_information in buying_informations:
    #         prices.append(int(buying_information.price))

    #     while price in prices:
    #         price = (random.randrange(1, 1001))*10000

    #     buying = BuyingInformation.objects.create(
    #         user_id=2,
    #         product_option_id=i,
    #         status_id=1,
    #         price=price)

    #     selling = SellingInformation.objects.create(
    #         user_id=3,
    #         product_option_id=i,
    #         status_id=1,
    #         price=price)

    #     Order.objects.create(buying_information=buying, selling_information=selling)

    # for i in range(5, 376, 6):
    #     price                = (random.randrange(1, 1001))*10000
    #     selling_informations = ProductOption.objects.get(id=i).sellinginformation_set.all()
    #     buying_informations  = ProductOption.objects.get(id=i).buyinginformation_set.all()

    #     prices = []

    #     for selling_information in selling_informations:
    #         prices.append(int(selling_information.price))
    #     for buying_information in buying_informations:
    #         prices.append(int(buying_information.price))

    #     while price in prices:
    #         price = (random.randrange(1, 1001))*10000

    #     buying = BuyingInformation.objects.create(
    #         user_id=3,
    #         product_option_id=i,
    #         status_id=1,
    #         price=price)

    #     selling = SellingInformation.objects.create(
    #         user_id=1,
    #         product_option_id=i,
    #         status_id=1,
    #         price=price)

    #     Order.objects.create(buying_information=buying, selling_information=selling)

    # for i in range(6, 376, 6):
    #     price                = (random.randrange(1, 1001))*10000
    #     selling_informations = ProductOption.objects.get(id=i).sellinginformation_set.all()
    #     buying_informations  = ProductOption.objects.get(id=i).buyinginformation_set.all()

    #     prices = []

    #     for selling_information in selling_informations:
    #         prices.append(int(selling_information.price))
    #     for buying_information in buying_informations:
    #         prices.append(int(buying_information.price))

    #     while price in prices:
    #         price = (random.randrange(1, 1001))*10000

    #     buying = BuyingInformation.objects.create(
    #         user_id=3,
    #         product_option_id=i,
    #         status_id=1,
    #         price=price)

    #     selling = SellingInformation.objects.create(
    #         user_id=2,
    #         product_option_id=i,
    #         status_id=1,
    #         price=price)

    #     Order.objects.create(buying_information=buying, selling_information=selling)


    # i = random.randrange(1, 6)
    # while i in [1, 2, 3]:
    #     i = random.randrange(1, 6)
    # print(i)
    # print(type(i))

    for row in data_reader:
        # Brand.objects.create(name=row[0], logo_image=row[1])

        # brand_name = row[0]
        # brand_id = Brand.objects.get(name=brand_name).id
        # Collection.objects.create(name=row[1], brand_id=brand_id)

        # Product.objects.create(collection_id=row[0], english_name=row[1], korean_name=row[2], limited=row[3])

        Message.objects.create(content=row[0])