import json
from datetime import datetime, timezone
from dateutil import parser

import requests
from django.db import transaction
from dotenv import dotenv_values
from rest_framework import status

from store.celery import app
from .models import Nomenclature, NomenclatureStock


env_vars = dotenv_values("./.env")
token_vars = dotenv_values("./token.env")
token_env = "./token.env"
products = "./import/data.json"
stock = "./import/stock.json"
import_url = "http://webapp:8000/api/v1/import/"  # for Docker Compose
stock_url = env_vars.get("STOCK_URL")
token_url = env_vars.get("TOKEN_URL")


def load_stock_data():
    with open(stock, "r", encoding="utf-8") as fh:
        stock_data = json.load(fh)
        return stock_data


def get_token():

    username = env_vars.get("USERNAME")
    password = env_vars.get("PASSWORD_SHOP")

    data = {"username": username, "password": password}
    headers = {"Content-Type": "application/json"}
    token_response = requests.post(url=token_url, json=data, headers=headers)
    content = token_response.json()

    access_token = content["access_token"]
    refresh_token = content["refresh_token"]

    with open(token_env, "w") as fp:
        lines = []
        lines.append(f"TOKEN={access_token}")
        lines.append(f"\nREFRESH_TOKEN={refresh_token}")
        fp.writelines(lines)

    return access_token


def get_inner_token():
    api_username = env_vars.get("API_USER_USERNAME")
    api_password = env_vars.get("API_USER_PASSWORD")

    user_data = {"username": api_username, "password": api_password}
    api_response = requests.post(url="http://webapp:8000/api/v1/token/", data=user_data)

    api_token = api_response.json().get("access")
    return api_token


def get_products(token):
    url = "https://api.malfini.com/api/v4/product"
    headers = {"Authorization": f"Bearer {token}"}
    reponse = requests.get(url=url, headers=headers)

    if reponse.status_code != 200:
        access_token = get_token()
        get_products(access_token)

    content = reponse.json()

    with open(products, "w", encoding="utf-8") as fh:
        json.dump(content, fh, indent=4)


def send_products():
    data = None

    with open(products, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    api_token = get_inner_token()
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }
    response = requests.post(url=import_url, json=data, headers=headers)

    return response.status_code


def get_stock(token):
    headers = {"Authorization": f"Bearer {token}"}
    reponse = requests.get(url=stock_url, headers=headers)

    if reponse.status_code != 200:
        access_token = get_token()
        get_stock(access_token)

    content = reponse.json()

    with open(stock, "w", encoding="utf-8") as fh:
        json.dump(content, fh, indent=4)


def update_nomenclature(code, quantity):
    item = Nomenclature.objects.filter(code=code).first()
    if not item:
        return False
    item.quantity = quantity
    return item


def create_nomenclature_stock(code, quantity):
    item = Nomenclature.objects.filter(code=code).first()
    if not item:
        return False
    return NomenclatureStock(nomenclature=item, quantity=quantity)


def update_current_stock() -> list:
    update_nomenclatures = []
    update_nomenclatures_stock = []

    current_date = datetime.now(timezone.utc)

    token = get_token()
    get_stock(token)
    stock_data = load_stock_data()

    imported_nomenclatures = set([code.get("productSizeCode") for code in stock_data])
    db_nomenclatures = [obj for obj in Nomenclature.objects.all()]

    for item in db_nomenclatures:
        if item.code not in imported_nomenclatures:
            item.quantity = 0
            update_nomenclatures.append(item)
            update_nomenclatures_stock.append(
                NomenclatureStock(nomenclature=item, quantity=0)
            )

    nomenclature_dict = {}

    for nomenclature in stock_data:
        product_code = nomenclature.get("productSizeCode")
        object_date = parser.parse(nomenclature["date"]).astimezone(timezone.utc)

        if product_code not in nomenclature_dict:
            nomenclature_dict[product_code] = {"found_today": False, "quantity": 0}

        if object_date < current_date:
            nomenclature_dict[product_code] = {
                "found_today": True,
                "quantity": nomenclature.get("quantity"),
            }

    for product_code, data in nomenclature_dict.items():
        if data["found_today"]:
            updated_item = update_nomenclature(product_code, data["quantity"])
            updated_item_stock = create_nomenclature_stock(
                product_code, data["quantity"]
            )

            if updated_item:
                update_nomenclatures.append(updated_item)
            if updated_item_stock:
                update_nomenclatures_stock.append(updated_item_stock)
        else:
            if product_code not in [
                item.code for item in update_nomenclatures
            ] and product_code not in [
                item.nomenclature for item in update_nomenclatures_stock
            ]:
                updated_item = update_nomenclature(product_code, 0)
                updated_item_stock = create_nomenclature_stock(product_code, 0)

                if updated_item:
                    update_nomenclatures.append(updated_item)
                if updated_item_stock:
                    update_nomenclatures_stock.append(updated_item_stock)

    with transaction.atomic():
        Nomenclature.objects.bulk_update(update_nomenclatures, ["quantity"])

    with transaction.atomic():
        NomenclatureStock.objects.bulk_create(update_nomenclatures_stock)

    return status.HTTP_204_NO_CONTENT


@app.task
def import_products():
    token = get_token()
    get_products(token)
    status_code = send_products()
    return status_code


@app.task
def update_stock():
    return update_current_stock()
