import requests
from bs4 import BeautifulSoup
import time
import random
import urllib.parse

def is_valid_link(link):
    if not link.startswith(("http://", "https://")):
        return False

    unwanted_patterns = [
        "support.google.com",
        "www.google.com",
        "accounts.google.com",
        "www.google.co",
    ]
    for pattern in unwanted_patterns:
        if pattern in link:
            return False

    return True

def filter_links_by_keyword(links, keyword):
    return [link for link in links if keyword.lower() in link.lower()]

def filter_links_by_domain(links, domain):
    return [link for link in links if domain.lower() in urllib.parse.urlparse(link).netloc.lower()]

def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'
    ]
    return random.choice(user_agents)

def search(query, limit=20, file_type=None, keyword=None, domain=None, lang=None, interval=None, proxy=None, ssl_verify=True, advanced=False, skip_invalid=False):
    if file_type:
        query = '+'.join(query.split()) + f"+filetype:{file_type}"
    else:
        query = '+'.join(query.split())

    url = f"https://www.google.com/search?q={query}"
    if lang:
        url += f"&hl={lang}"

    headers = {
        "User-Agent": get_random_user_agent()
    }

    retry_count = 0
    max_retries = 5
    links_found = []

    while retry_count < max_retries and len(links_found) < limit:
        try:
            response = requests.get(url, headers=headers, proxies={"http": proxy, "https": proxy} if proxy else None, verify=ssl_verify)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                links = soup.find_all("a")

                for link in links:
                    href = link.get("href")
                    if href:
                        href = href.split("&")[0].replace("/url?q=", "")
                        if is_valid_link(href):
                            links_found.append(href)

                    if len(links_found) >= limit:
                        break

                if len(links_found) >= limit:
                    break

            elif response.status_code == 429:
                retry_count += 1
                time.sleep(random.randint(10, 30))
            else:
                break
        except requests.exceptions.RequestException:
            retry_count += 1
            headers["User-Agent"] = get_random_user_agent()
            time.sleep(random.randint(5, 15))
        except Exception:
            retry_count += 1
            headers["User-Agent"] = get_random_user_agent()
            time.sleep(random.randint(5, 15))

    if skip_invalid:
        links_found = [link for link in links_found if len(link) > 20]

    if keyword:
        links_found = filter_links_by_keyword(links_found, keyword)
    if domain:
        links_found = filter_links_by_domain(links_found, domain)

    if interval:
        time.sleep(interval)

    if advanced:
        links_found = [link for link in links_found if len(link) > 20]

    return links_found[:limit]
