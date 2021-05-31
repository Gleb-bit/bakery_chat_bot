from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import models
from models import Category, Product

keyboard = VkKeyboard()


def handler_category(text):
    query = Category.get(Category.name == text.lower())
    return query.exists()


def handle_first_keyboard(text):
    keyboard = VkKeyboard()
    categories = Category.select()
    for category in categories:
        keyboard.add_button(category.name, color=VkKeyboardColor.SECONDARY)
        if not category.id % 2:
            keyboard.add_line()
    # keyboard.add_button('Мороженое', color=VkKeyboardColor.SECONDARY)
    # keyboard.add_button('Напитки', color=VkKeyboardColor.NEGATIVE)
    #
    # keyboard.add_line()
    #
    # keyboard.add_button('Выпечка', color=VkKeyboardColor.POSITIVE)
    # keyboard.add_button('Сладости', color=VkKeyboardColor.PRIMARY)
    #
    # keyboard.add_line()
    #
    keyboard.add_button('Вернуться на главную', color=VkKeyboardColor.SECONDARY)

    return keyboard


def handle_second_keyboard(text):
    keyboard = VkKeyboard()
    try:
        query = Category.get(Category.name == text.lower())
    except models.Category.DoesNotExist:
        return
    products = Product.select().where(query.id == Product.category_id)
    for product in products:
        keyboard.add_button(product.name, color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Вернуться на главную', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Назад', color=VkKeyboardColor.SECONDARY)
    return keyboard


def handle_third_keyboard(text):
    try:
        query = Product.get(Product.name == text.lower())
    except models.Product.DoesNotExist:
        return
    description = query.description
    picture = query.picture
    return (description, picture)
