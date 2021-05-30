from models import Product, Category, UserState
import peewee

# Product.create_table()
# Category.create_table()
UserState.create_table()


def add_category(name):
    row = Category(
        name=name.lower().strip(),
    )
    row.save()


def add_product(name, description, category_name):
    try:
        category = Category.select().where(Category.name == category_name.strip()).get()
    except peewee.DoesNotExist:
        category = None
    path_to_picture = 'pictures/'
    with open(f"{path_to_picture}/{category_name}/{name}.jpg", "rb") as image:
        file = image.read()
        byte_image = bytearray(file)
    if category:
        row = Product(
            name=name.lower().strip(),
            description=description,
            category=category,
            picture=byte_image
        )
        row.save()


categories_and_products = {'мороженое': [{'эскимо': ''}, {'стаканчик': ''}], 'напитки': [{'кола': ''}, {'спрайт': ''}],
                           'выпечка': [{'булка': ''}, {'пицца': ''}, {'круассан': ''}],
                           'сладости': [{'конфеты': ''}, {'мармелад': ''}]}
# for category, products in categories_and_products.items():
#     add_category(category)
#     for item in products:
#         for product, description in item.items():
#             add_product(product, description, category)
