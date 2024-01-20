import requests
import asyncio
from datetime import datetime


def post_exit_api(today_date):
    api_url = "https://tizimswag.astrolab.uz/v1/get-workers-by-day"
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.get(f"{api_url}/{today_date}", headers=headers)
        response.raise_for_status()
        result = response.json()
        return result
    except requests.exceptions.RequestException as err:
        print(f"Request exception: {err}")


if __name__ == '__main__':
    today_date = datetime.now().strftime("20%y-%m-%d")
    data = post_exit_api(today_date)
    for user in data["came"]:
        print(user["id"])
        # print(user)
