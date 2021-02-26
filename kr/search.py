import requests
from bs4 import BeautifulSoup

from .config import BASE_URL
from .consoles import consoles


def verify_console_name(console_name):
    try:
        console_code = consoles[console_name]
    except KeyError:
        raise KeyError(f"Console {console_name} is not available.")

    return console_code


def search(console_code, query, order_by="downloads", asc=False, page=0):
    order = f"{order_by}${'ASC' if asc else 'DESC'}"

    response = requests.post(
        f"{BASE_URL}/ajax.php?m=roms_j",
        data={
            "sort": order,
            "page": page,
            "search": query,
            "rom_concole": console_code,
        },
    )

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.select("table > tbody tr")
    result = [parse_row(row) for row in table]

    return result


def parse_row(row):
    columns = row.select("td")

    parsed_row = dict(
        title=columns[0].text.strip("\n"),
        genre=columns[1].text.strip("\n"),
        rating=columns[2].text.strip("\n"),
        downloads=columns[3].text.strip("\n"),
        size=columns[4].text.strip("\n"),
        link=f"{BASE_URL}{columns[0].find('a')['href']}",
    )

    return parsed_row
