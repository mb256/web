from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import time
import re


DATE_RE = re.compile(r'^\d{1,2}\.\d{1,2}\.\d{4}$')


def fetch_climber_routes(url, max_retries=3, delay=0.3, date_filter=False):
    """
    Fetch climbing routes from lezec.cz with retry logic.
    Returns dict with 'routes' (list of route dicts) and 'total_points' (int), or None on failure.
    When date_filter=True, only rows whose first cell matches dd.mm.yyyy are parsed (skips difficulty-label rows).
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
            total_points = 0

            if date_filter:
                # Top-10 pages interleave difficulty-label rows; iterate over all remaining
                # cells and collect 7-cell groups that start with a valid date.
                i = data_start
                while i + 6 < len(all_cells):
                    date = all_cells[i].get_text(strip=True)
                    if date == 'Celkem:':
                        break
                    if not DATE_RE.match(date):
                        i += 1
                        continue
                    name = all_cells[i + 1].get_text(strip=True)
                    sector = all_cells[i + 2].get_text(strip=True)
                    difficulty = all_cells[i + 3].get_text(strip=True)
                    style = all_cells[i + 5].get_text(strip=True)
                    if name:
                        routes.append({
                            'date': date,
                            'name': name,
                            'sector': sector,
                            'difficulty': difficulty,
                            'style': style,
                        })
                    i += 7
            else:
                for i in range(10):
                    route_start = data_start + (i * 7)
                    if route_start + 6 >= len(all_cells):
                        break

                    date = all_cells[route_start].get_text(strip=True)

                    if date == 'Celkem:':
                        break

                    name = all_cells[route_start + 1].get_text(strip=True)
                    sector = all_cells[route_start + 2].get_text(strip=True)
                    difficulty = all_cells[route_start + 3].get_text(strip=True)
                    style = all_cells[route_start + 5].get_text(strip=True)

                    if not name:
                        break

                    route = {
                        'date': date,
                        'name': name,
                        'sector': sector,
                        'difficulty': difficulty,
                        'style': style
                    }
                    routes.append(route)

            # Search for 'Celkem:' in all cells to extract total points
            # This handles colspan attribute correctly
            for i, cell in enumerate(all_cells):
                if cell.get_text(strip=True) == 'Celkem:':
                    # The next cell contains the total points
                    if i + 1 < len(all_cells):
                        points_text = all_cells[i + 1].get_text(strip=True)
                        try:
                            total_points = int(points_text)
                        except ValueError:
                            total_points = 0
                    break

            result = {
                'routes': routes if routes else [],
                'total_points': total_points
            }
            return result if routes else None

        except (requests.RequestException, Exception) as e:
            if attempt < max_retries - 1:
                time.sleep(delay)
                continue
            else:
                # Log the error in server logs
                print(f"Error fetching data after {max_retries} attempts: {e}")
                return None

    return None


CLIMBERS_DATA_LAST = [
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
    },
    {
        'name': 'JirkaCh',
        'url': 'https://lezec.cz/denik.php?parn=2&uid=4a69726b614368h&ckat=2&crok=9992'
    },
    {
        'name': 'Luky:o)',
        'url': 'https://lezec.cz/denik.php?parn=2&uid=4c756b793a6f29h&ckat=2&crok=9992'
    },
    {
        'name': 'pelda',
        'url': 'https://lezec.cz/denik.php?parn=2&uid=70656c6461h&ckat=2&crok=9992'
    },
    {
        'name': 'Palec',
        'url': 'https://lezec.cz/denik.php?parn=2&uid=50616c6563h&ckat=2&crok=9992'
    },
    {
        'name': 'ospacek',
        'url': 'https://lezec.cz/denik.php?parn=2&uid=6f7370e1e8656bh&ckat=2&crok=9992'
    },
    {
        'name': 'Erik!',
        'url': 'https://lezec.cz/denik.php?parn=2&uid=4572696b21h&ckat=2&crok=9992'
    },
    {
        'name': 'jirkas',
        'url': 'https://lezec.cz/denik.php?parn=2&uid=6a69726b6173h&ckat=2&crok=9992'
    },
    {
        'name': 'Feld',
        'url': 'https://lezec.cz/denik.php?parn=2&uid=46656c64h&ckat=2&crok=9992'
    },
    {
        'name': 'Sved',
        'url': 'https://lezec.cz/denik.php?parn=2&uid=8a77e964h&ckat=2&crok=9992'
    },
    {
        'name': 'Krvak',
        'url': 'https://lezec.cz/denik.php?parn=2&uid=4b7276e16bh&ckat=2&crok=9992'
    },
    {
        'name': 'blaza',
        'url': 'https://lezec.cz/denik.php?parn=2&uid=626c617a61h&ckat=2&crok=9992'
    },
    {
        'name': 'LukasG',
        'url': 'https://lezec.cz/denik.php?parn=2&uid=4c756b617347h&ckat=2&crok=9992'
    },
]

CLIMBERS_DATA_TOP10 = [
    {
        'name': 'Honza Koudelka',
        'url': 'https://lezec.cz/denik.php?parn=3&par=1&uid=486f6e7a61204b6f7564656c6b61h&ckat=2&crok=9992'
    },
    {
        'name': 'choodi',
        'url': 'https://lezec.cz/denik.php?parn=3&par=1&uid=63686f6f6469h&ckat=2&crok=9992'
    },
    {
        'name': 'seqa',
        'url': 'https://lezec.cz/denik.php?parn=3&par=1&uid=53657161h&ckat=2&crok=9992'
    },
    {
        'name': '_brouk_',
        'url': 'https://lezec.cz/denik.php?parn=3&par=1&uid=5f62726f756b5fh&ckat=2&crok=9992'
    },
    {
        'name': 'JirkaCh',
        'url': 'https://lezec.cz/denik.php?parn=3&par=1&uid=4a69726b614368h&ckat=2&crok=9992'
    },
    {
        'name': 'Luky:o)',
        'url': 'https://lezec.cz/denik.php?parn=3&par=1&uid=4c756b793a6f29h&ckat=2&crok=9992'
    },
    {
        'name': 'pelda',
        'url': 'https://lezec.cz/denik.php?parn=3&par=1&uid=70656c6461h&ckat=2&crok=9992'
    },
    {
        'name': 'Palec',
        'url': 'https://lezec.cz/denik.php?parn=3&par=1&uid=50616c6563h&ckat=2&crok=9992'
    },
    {
        'name': 'ospacek',
        'url': 'https://lezec.cz/denik.php?parn=3&par=1&uid=6f7370e1e8656bh&ckat=2&crok=9992'
    },
    {
        'name': 'Erik!',
        'url': 'https://lezec.cz/denik.php?parn=3&par=1&uid=4572696b21h&ckat=2&crok=9992'
    },
    {
        'name': 'jirkas',
        'url': 'https://lezec.cz/denik.php?parn=3&par=1&uid=6a69726b6173h&ckat=2&crok=9992'
    },
    {
        'name': 'Feld',
        'url': 'https://lezec.cz/denik.php?parn=3&par=1&uid=46656c64h&ckat=2&crok=9992'
    },
    {
        'name': 'Sved',
        'url': 'https://lezec.cz/denik.php?parn=3&par=1&uid=8a77e964h&ckat=2&crok=9992'
    },
    {
        'name': 'Krvak',
        'url': 'https://lezec.cz/denik.php?parn=3&par=1&uid=4b7276e16bh&ckat=2&crok=9992'
    },
    {
        'name': 'blaza',
        'url': 'https://lezec.cz/denik.php?parn=3&par=1&uid=626c617a61h&ckat=2&crok=9992'
    },
    {
        'name': 'LukasG',
        'url': 'https://lezec.cz/denik.php?parn=3&par=1&uid=4c756b617347h&ckat=2&crok=9992'
    },
]


def prelezy(request):
    """Django view that displays climbers sorted by total climbing points."""
    active_view = request.GET.get('view', 'last')
    if active_view == 'top10':
        climbers_data = CLIMBERS_DATA_TOP10
        use_date_filter = True
    else:
        active_view = 'last'
        climbers_data = CLIMBERS_DATA_LAST
        use_date_filter = False

    climbers = []
    for climber in climbers_data:
        result = fetch_climber_routes(climber['url'], date_filter=use_date_filter)
        
        if result is None:
            climber_info = {
                'name': climber['name'],
                'routes': [],
                'total_points': 0,
                'last_climb_date': None,
                'error': 'Nepodařilo se načíst data po 3 pokusech'
            }
        else:
            routes = result['routes']
            total_points = result['total_points']
            
            # Get the last climb date (most recent route, which is first in the list)
            last_climb_date = routes[0]['date'] if routes else None
            
            climber_info = {
                'name': climber['name'],
                'routes': routes,
                'total_points': total_points,
                'last_climb_date': last_climb_date,
                'error': None
            }
        
        climbers.append(climber_info)

    # Sort climbers by total_points descending (highest first)
    climbers.sort(key=lambda x: x['total_points'], reverse=True)

    return render(request, 'prelezy/routes.html', {'climbers': climbers, 'active_view': active_view})
