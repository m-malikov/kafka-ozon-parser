import requests
from flask import current_app


def get_category_data(category_url):
    expected_prefix = "https://www.ozon.ru"
    if not category_url.startswith(expected_prefix):
        raise ValueError("expected url to start with " + expected_prefix)
    category_url = category_url[len(expected_prefix):]

    result = []
    for i in range(current_app.config["FETCH_PAGES"]):
        base_url = current_app.config["BASE_URL"]

        paginated_category_url = "{}?page={}".format(category_url, i+1)
        response = requests.get(
            base_url,
            headers={
                "User-Agent": current_app.config["USER_AGENT"]
            },
            params={"url": paginated_category_url}
        )
        response.raise_for_status()
        result.append(response.text)
    return result
