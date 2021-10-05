import os, django, csv, sys, random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "werecord.settings")
django.setup()

from records.models import *
from users.models   import *

from string import ascii_lowercase, ascii_uppercase

CSV_PATH_PRODUCTS = './batch.csv'

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

    # for batch in [18, 19, 21, 22]:
    #     for name in list(ascii_uppercase):
    #         if batch % 2 == 0:
    #             User.objects.create(google_login_id=name+"0"+str(batch), email=name+"@example.com", profile_image_url="image_url", name=name, batch_id=batch, position_id=1, user_type_id=2)
    #         if batch % 2 == 1:
    #             User.objects.create(google_login_id=name+"0"+str(batch), email=name+"@example.com", profile_image_url="image_url", name=name, batch_id=batch, position_id=2, user_type_id=2)

    # for name in list(ascii_uppercase):
    #     user = User.objects.get(name=name, batch_id=18)
    #     for date in ["2021-5-3","2021-5-4","2021-5-6", "2021-5-7"]:
    #         Record.objects.create(start_at=date+" 10:00:00", end_at=date+" 21:00:00", residence_time=39600, user_id=user.id)
    #         DailyRecord.objects.create(user_id=user.id, date=date, total_time=39600)
    #         user.total_time += 39600
    #         user.save()
    #         user.batch.total_time += 39600
    #         user.batch.save()
    #     user.average_start = "10:00:00"
    #     user.average_end = "21:00:00"
    #     user.save()

    # for name in list(ascii_uppercase):
    #     user = User.objects.get(name=name, batch_id=19)
    #     for date in ["2021-5-3","2021-5-4","2021-5-6", "2021-5-7"]:
    #         Record.objects.create(start_at=date+" 10:00:00", end_at=date+" 20:00:00", residence_time=36000, user_id=user.id)
    #         DailyRecord.objects.create(user_id=user.id, date=date, total_time=36000)
    #         user.total_time += 36000
    #         user.save()
    #         user.batch.total_time += 36000
    #         user.batch.save()
    #     user.average_start = "10:00:00"
    #     user.average_end = "20:00:00"
    #     user.save()

    # user = User.objects.get(name="A", batch_id=21)
    # for date in ["2021-7-12","2021-7-13","2021-7-14"]:
    #     Record.objects.create(start_at=date+" 10:00:00", end_at=date+" 22:00:00", residence_time=43200, user_id=user.id)
    #     DailyRecord.objects.create(user_id=user.id, date=date, total_time=43200)
    #     user.total_time += 43200
    #     user.save()
    #     user.batch.total_time += 43200
    #     user.batch.save()
    # user.average_start = "10:00:00"
    # user.average_end = "22:00:00"
    # user.save()

    # user = User.objects.get(name="B", batch_id=21)
    # for date in ["2021-7-12","2021-7-13","2021-7-14"]:
    #     Record.objects.create(start_at=date+" 10:00:00", end_at=date+" 19:00:00", residence_time=32400, user_id=user.id)
    #     DailyRecord.objects.create(user_id=user.id, date=date, total_time=32400)
    #     user.total_time += 32400
    #     user.save()
    #     user.batch.total_time += 32400
    #     user.batch.save()
    # user.average_start = "10:00:00"
    # user.average_end = "19:00:00"
    # user.save()

    # user = User.objects.get(name="C", batch_id=21)
    # for date in ["2021-7-12","2021-7-13","2021-7-14"]:
    #     Record.objects.create(start_at=date+" 9:30:00", end_at=date+" 22:00:00", residence_time=45000, user_id=user.id)
    #     DailyRecord.objects.create(user_id=user.id, date=date, total_time=45000)
    #     user.total_time += 45000
    #     user.save()
    #     user.batch.total_time += 45000
    #     user.batch.save()
    # user.average_start = "9:00:00"
    # user.average_end = "22:00:00"
    # user.save()

    # user = User.objects.get(name="B", batch_id=22)
    # for date in ["2021-7-12","2021-7-13","2021-7-14"]:
    #     Record.objects.create(start_at=date+" 10:00:00", end_at=date+" 22:00:00", residence_time=43200, user_id=user.id)
    #     DailyRecord.objects.create(user_id=user.id, date=date, total_time=43200)
    #     user.total_time += 43200
    #     user.save()
    #     user.batch.total_time += 43200
    #     user.batch.save()
    # user.average_start = "10:00:00"
    # user.average_end = "22:00:00"
    # user.save()

    # user = User.objects.get(name="C", batch_id=22)
    # for date in ["2021-7-12","2021-7-13","2021-7-14"]:
    #     Record.objects.create(start_at=date+" 10:00:00", end_at=date+" 19:00:00", residence_time=32400, user_id=user.id)
    #     DailyRecord.objects.create(user_id=user.id, date=date, total_time=32400)
    #     user.total_time += 32400
    #     user.save()
    #     user.batch.total_time += 32400
    #     user.batch.save()
    # user.average_start = "10:00:00"
    # user.average_end = "19:00:00"
    # user.save()

    # user = User.objects.get(name="A", batch_id=22)
    # for date in ["2021-7-12","2021-7-13","2021-7-14"]:
    #     Record.objects.create(start_at=date+" 9:30:00", end_at=date+" 22:00:00", residence_time=45000, user_id=user.id)
    #     DailyRecord.objects.create(user_id=user.id, date=date, total_time=45000)
    #     user.total_time += 45000
    #     user.save()
    #     user.batch.total_time += 45000
    #     user.batch.save()
    # user.average_start = "9:00:00"
    # user.average_end = "22:00:00"
    # user.save()

    # user = User.objects.get(name="이다슬", batch_id=20)
    # for date in ["2021-8-2","2021-8-3","2021-8-4","2021-8-9","2021-8-10","2021-8-11"]:
    #     Record.objects.create(start_at=date+" 10:00:00", end_at=date+" 22:00:00", residence_time=43200, user_id=user.id)
    #     DailyRecord.objects.create(user_id=user.id, date=date, total_time=43200)
    #     user.total_time += 43200
    #     user.save()
    #     user.batch.total_time += 43200
    #     user.batch.save()
    # user.average_start = "10:00:00"
    # user.average_end = "22:00:00"
    # user.save()

    # user = User.objects.get(name="양미화", batch_id=20)
    # for date in ["2021-8-2","2021-8-3","2021-8-4","2021-8-9","2021-8-10","2021-8-11"]:
    #     Record.objects.create(start_at=date+" 10:00:00", end_at=date+" 19:00:00", residence_time=32400, user_id=user.id)
    #     DailyRecord.objects.create(user_id=user.id, date=date, total_time=32400)
    #     user.total_time += 32400
    #     user.save()
    #     user.batch.total_time += 32400
    #     user.batch.save()
    # user.average_start = "10:00:00"
    # user.average_end = "19:00:00"
    # user.save()

    # user = User.objects.get(name="전용민", batch_id=20)
    # for date in ["2021-8-2","2021-8-3","2021-8-4","2021-8-9","2021-8-10","2021-8-11"]:
    #     Record.objects.create(start_at=date+" 9:30:00", end_at=date+" 22:00:00", residence_time=45000, user_id=user.id)
    #     DailyRecord.objects.create(user_id=user.id, date=date, total_time=45000)
    #     user.total_time += 45000
    #     user.save()
    #     user.batch.total_time += 45000
    #     user.batch.save()
    # user.average_start = "9:30:00"
    # user.average_end = "22:00:00"
    # user.save()

    user = User.objects.get(name="김수연", batch_id=20)
    for date in ["2021-8-2","2021-8-3","2021-8-4","2021-8-9","2021-8-10","2021-8-11"]:
        Record.objects.create(start_at=date+" 9:00:00", end_at=date+" 22:00:00", residence_time=45000, user_id=user.id)
        DailyRecord.objects.create(user_id=user.id, date=date, total_time=45000)
        user.total_time += 46800
        user.save()
        user.batch.total_time += 46800
        user.batch.save()
    user.average_start = "9:00:00"
    user.average_end = "22:00:00"
    user.save()

    # user = User.objects.get(name="A", batch_id=21)
    # for date in ["2021-7-1"]:
    #     Record.objects.create(start_at=date+" 10:00:00", user_id=user.id)
    
    # user = User.objects.get(name="B", batch_id=21)
    # for date in ["2021-7-1"]:
    #     Record.objects.create(start_at=date+" 09:00:00", user_id=user.id)
    
    # user = User.objects.get(name="C", batch_id=21)
    # for date in ["2021-7-1"]:
    #     Record.objects.create(start_at=date+" 10:00:00", user_id=user.id)

    # for row in data_reader:
        # Brand.objects.create(name=row[0], logo_image=row[1])

        # brand_name = row[0]
        # brand_id = Brand.objects.get(name=brand_name).id
        # Collection.objects.create(name=row[1], brand_id=brand_id)

        # Product.objects.create(collection_id=row[0], english_name=row[1], korean_name=row[2], limited=row[3])

        # Message.objects.create(content=row[0])
        # Batch.objects.create(id=int(row[0]), name=row[1], start_day=row[2], end_day=row[3], mentor_name=row[4])

# Position.objects.create(id=1, name='Front-end')
# Position.objects.create(id=2, name='Back-end')
# Position.objects.create(id=3, name='Fullstack')
# Position.objects.create(id=4, name='Undifined')

# UserType.objects.create(id=1, name='멘토')
# UserType.objects.create(id=2, name='수강생')

# User.objects.create(id=1, google_login_id="109819285270419577429", email="gsy4568@gmail.com", profile_image_url="https://werecord.s3.ap-northeast-2.amazonaws.com/30693e94-ad78-4089-9fe8-9ab8d5e40eec", name="김수연", batch_id=20, position_id=1, user_type_id=2)
# User.objects.create(id=2, google_login_id="101275114010733580190", email="hwaya2828@gmail.com", profile_image_url="https://werecord.s3.ap-northeast-2.amazonaws.com/c33fbdf5-25ab-40b4-866b-c301a428cf45", name="양미화", batch_id=20, position_id=2, user_type_id=2)
# User.objects.create(id=3, google_login_id="107970921751732415878", email="dls2tmfs2@gmail.com", profile_image_url="https://werecord.s3.ap-northeast-2.amazonaws.com/643b2cec-c7de-47e8-99bf-851e8f7e6b1f", name="이다슬", batch_id=20, position_id=1, user_type_id=2)
# User.objects.create(id=4, google_login_id="106863072648316411196", email="dydalsdl1414@gmail.com", profile_image_url="https://werecord.s3.ap-northeast-2.amazonaws.com/077508d7-df5a-4bf7-b28b-c6de0ed20770", name="전용민", batch_id=20, position_id=1, user_type_id=2)
# User.objects.create(id=5, google_login_id="103763445972990735196", email="choidaehwan9282@gmail.com", profile_image_url="https://lh3.googleusercontent.com/a-/AOh14GhW5TMc1XFu2Lv3GKZ2eLybZ478dWnJiErUSVlYMg=s96-c", name="최대환", batch_id=20, position_id=1, user_type_id=2)


# Record.objects.create(start_at=datetime.datetime(2021, 6, 28, 10, 20, 0, 0), end_at=datetime.datetime(2021, 6, 28, 22, 0, 0, 0), residence_time=42000, user_id=1)
# Record.objects.create(start_at=datetime.datetime(2021, 6, 29, 10, 20, 0, 0), end_at=datetime.datetime(2021, 6, 29, 22, 0, 0, 0), residence_time=42000, user_id=1)
# Record.objects.create(start_at=datetime.datetime(2021, 6, 30, 10, 20, 0, 0), end_at=datetime.datetime(2021, 6, 30, 22, 0, 0, 0), residence_time=42000, user_id=1)
# Record.objects.create(start_at=datetime.datetime(2021, 7, 1, 10, 20, 0, 0), end_at=datetime.datetime(2021, 7, 1, 22, 0, 0, 0), residence_time=42000, user_id=1)
# Record.objects.create(start_at=datetime.datetime(2021, 7, 2, 10, 20, 0, 0), end_at=datetime.datetime(2021, 7, 2, 22, 0, 0, 0), residence_time=42000, user_id=1)

# Record.objects.create(start_at=datetime.datetime(2021, 7, 5, 10, 20, 0, 0), end_at=datetime.datetime(2021, 7, 5, 22, 0, 0, 0), residence_time=42000, user_id=1)
# Record.objects.create(start_at=datetime.datetime(2021, 7, 6, 10, 20, 0, 0), end_at=datetime.datetime(2021, 7, 6, 22, 0, 0, 0), residence_time=42000, user_id=1)

# 345600 + 374400 + 360000 + 331200 + 336000

# Record.objects.create(start_at=datetime.datetime(2021, 7, 7, 9, 30, 0, 0), user_id=1)