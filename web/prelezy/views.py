from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import time


def fetch_climber_routes(url, max_retries=3, delay=0.3):
    """
    Fetch climbing routes from lezec.cz with retry logic.
    Returns list of route dicts or None on failure.
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            all_cells = soup.find_all(['td', 'th'])

            header_index = None
            for i, cell in enumerate(all_cells):
                if cell.get_text(strip=True) == 'Datum':
                    header_index = i
                    break

            if header_index is None:
                if attempt < max_retries - 1:
                    time.sleep(delay)
                    continue
                return None

            expected_headers = ['Datum', 'Cesta', 'Oblast', 'Klas', 'Body', 'Styl', 'P']
            actual_headers = [all_cells[header_index + i].get_text(strip=True)
                              for i in range(len(expected_headers))]

            if actual_headers != expected_headers:
                if attempt < max_retries - 1:
                    time.sleep(delay)
                    continue
                return None

            routes = []
            data_start = header_index + 7
            for i in range(10):
                route_start = data_start + (i * 7)
                if route_start + 6 >= len(all_cells):
                    break

                date = all_cells[route_start].get_text(strip=True)
                name = all_cells[route_start + 1].get_text(strip=True)
                sector = all_cells[route_start + 2].get_text(strip=True)
                difficulty = all_cells[route_start + 3].get_text(strip=True)
                style = all_cells[route_start + 5].get_text(strip=True)

                if date == 'Celkem:' or not name:
                    break

                route = {
                    'date': date,
                    'name': name,
                    'sector': sector,
                    'difficulty': difficulty,
                    'style': style
                }
                routes.append(route)

            return routes if routes else None

        except (requests.RequestException, Exception) as e:
            if attempt < max_retries - 1:
                time.sleep(delay)
                continue
            else:
                # Log the error in server logs
                print(f"Error fetching data after {max_retries} attempts: {e}")
                return None

    return None


def prelezy(request):
    """Django view that replicates the Flask prelezy() behavior."""
    climbers_data = [
        {
            'name': 'Honza Koudelka',
            'url': 'https://lezec.cz/denik.php?parn=2&uid=486f6e7a61204b6f7564656c6b61h&ckat=2&crok=9992'
        },
        {
            'name': 'choodi',
            'url': 'https://lezec.cz/denik.php?parn=2&uid=63686f6f6469h&ckat=2&crok=9992'
        },
        {
            'name': 'seqa',
            'url': 'https://lezec.cz/denik.php?parn=2&uid=53657161h&ckat=2&crok=9992'
        },
        {
            'name': '_brouk_',
            'url': 'https://lezec.cz/denik.php?parn=2&uid=5f62726f756b5fh&ckat=2&crok=9992'
        }
    ]

    climbers = []
    for climber in climbers_data:
        routes = fetch_climber_routes(climber['url'])
        climber_info = {
            'name': climber['name'],
            'routes': routes if routes else [],
            'error': None if routes else 'Nepodařilo se načíst data po 3 pokusech'
        }
        climbers.append(climber_info)

    return render(request, 'prelezy/routes.html', {'climbers': climbers})
