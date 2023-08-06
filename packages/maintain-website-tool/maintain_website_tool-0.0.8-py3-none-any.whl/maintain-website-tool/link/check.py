import multiprocessing
from urllib.parse import urlparse
from .io import write_file, load_file
from .extract_links import extract_links
from tqdm import tqdm
import time
import requests
import sys

def lookup_urls(locations, processes=6, estimate_total=None):
    """Run a manager to hold:
    - a set (as dict) of all unchecked urls,
    - a dict of urls to responses or exceptions occuring when getting those URLs
    - a dict of urls to a list of urls where that url occured in the HTML Plain Text.

    Then start processes (defaults to 6) to pop urls from the unchecked
    set, fetch the contents at that url and if possible extract links from
    those contents and add them to unchecked - if they share a domain with
    one of the locations provided as input.
    """

    domains = { urlparse(location).netloc for location in locations }

    urls = {}

    occurances = { location: ["Locations File"] for location in locations }

    with multiprocessing.Manager() as manager:

        unchecked = manager.dict({ location: None for location in locations }) # Acts as a set.

        urls = manager.dict()

        occurances = manager.list([(location, "Locations File") for location in locations])

        with multiprocessing.Pool(processes) as pool:
            loading = pool.map_async(check_url, [(unchecked, urls, occurances, domains, id) for id in range(processes)])

            with tqdm(unit="sites", total=estimate_total) as progress_checked:
                with tqdm(unit="sites", total=estimate_total) as progress_total:
                    progress_checked.set_description_str("Checked URLs")
                    progress_total.set_description_str("Total URLs found")

                    dt = 0.1
                    urls_len = len(urls)
                    total = len(unchecked) + len(urls)

                    while not loading.ready():
                        progress_checked.update(len(urls) - urls_len)
                        progress_total.update(len(unchecked) + len(urls) - total)

                        urls_len = len(urls)
                        total = len(unchecked) + urls_len

                        time.sleep(dt)

        occurances_ = {}

        for (link, origin) in occurances:
            if occurances_.get(link, None) is None:
                occurances_[link] = set()

            occurances_[link].add(origin)

        occurances = occurances_

        result = {}

        for url in urls:
            result[url] = urls[url].copy()

            response = result[url]["response"]
            del result[url]["response"]

            if isinstance(response, Exception):
                result[url]["error"] = str(response.__cause__)

            else:
                result[url]["ok"] = response.ok
                result[url]["status_code"] = response.status_code
                result[url]["occurances"] = list(occurances[url])

        return result

def check_url(arg):
    unchecked, urls, occurances, domains, id = arg

    while len(unchecked) != 0:
        try:
            url,_ = unchecked.popitem()

            before = time.time()
            response = requests.get(url)
            latency = time.time() - before

            urls[url] = {
                "response": response,
                "latency": latency,
            }

        except KeyError:
            continue
        except requests.exceptions.RequestException as e:
            urls[url] = {
                "response": e,
                "latency": time.time() - before
            }

        else:
            if not response.headers.get("Content-Type", default = "text/plain").startswith("text/html"):
                continue

            parsed = urlparse(url)

            if parsed.netloc in domains:
                links = extract_links(response.text, domain=parsed.netloc)

                for link in links:
                    occurances.append((link, url))

                    if link not in urls:
                        unchecked[link] = None

def check_locations(args):
    file_handler = open(args.locations) if args.locations not in ["", "-"] else sys.stdin
    locations = file_handler.read().strip().split("\n")

    result = lookup_urls(locations, processes = args.num_processes, estimate_total = args.estimate_total)

    write_file(result, format=args.out_format if args.out_format is not None else args.format)
