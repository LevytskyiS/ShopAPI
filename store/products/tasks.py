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
        print("updated products")
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


def update_current_stock() -> list:
    checked_items = []
    updated = []
    dynamic_stock = []
    token = get_token()
    get_stock(token)

    stock_data = load_stock_data()

    for data in stock_data:
        code = data.get("productSizeCode")
        quantity = data.get("quantity")
        date = data.get("date")

        datetime_obj = parser.parse(date)
        datetime_obj = datetime_obj.astimezone(timezone.utc)
        item = Nomenclature.objects.filter(code=code).first()

        if datetime_obj > datetime.now(timezone.utc) and item:
            item.quantity = 0
            updated.append(item)
            stock_obj = NomenclatureStock(nomenclature=item, quantity=0)
            if code not in checked_items:
                dynamic_stock.append(stock_obj)
                checked_items.append(code)
            continue

        if code and quantity and date and item:
            item.quantity = quantity
            updated.append(item)
            stock_obj = NomenclatureStock(nomenclature=item, quantity=quantity)
            dynamic_stock.append(stock_obj)

    with transaction.atomic():
        Nomenclature.objects.bulk_update(updated, ["quantity"])

    with transaction.atomic():
        NomenclatureStock.objects.bulk_create(dynamic_stock)

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
