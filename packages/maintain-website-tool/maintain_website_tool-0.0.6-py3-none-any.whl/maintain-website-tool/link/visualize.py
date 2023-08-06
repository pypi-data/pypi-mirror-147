from pyvis.network import Network
from urllib.parse import urlparse
from .io import load_file, write_file
from tqdm import tqdm

def visualize(args):
    result = load_file(args.filename, format=args.format if args.in_format is None else args.in_format)

    net = Network()

    domains = {
        "Locations File": {
            "urls": set(),
            "occured":set(),
            "occurances":set(),
            "ok":True,
            "error":True,
        }
    }

    with tqdm(total=3*len(result)) as progress:

        for url in result:
            domain = domain_from_url(url)

            if domain not in domains:
                domains[domain] = {
                    "urls": set(),
                    "occured" : set(),
                    "occurances": set(),
                    "ok": True,
                    "error": True,
                }

            domains[domain]["urls"].add(url)
            domains[domain]["occurances"] |= set(result[url]["occurances"]) if result[url]["occurances"] is not None else set()
            domains[domain]["ok"] = domains[domain]["ok"] and result[url].get("ok", False)
            domains[domain]["error"] = domains[domain]["error"] and result[url].get("error", False)

            if result[url]["occurances"] is None:
                continue

            for link in result[url]["occurances"]:
                domains[domain_from_url(url)]["occured"].add(url)

            progress.update(1)

        for domain in domains:
            net.add_node(domain,
                        title="\n".join(filter(lambda u: not result[u].get("ok", False) or not result[u].get("error", True),  domains[domain]["urls"])),
                        mass=len(domains[domain]["occured"]),
                        shape=node_shape(domain),
                        color=node_color(domains[domain]))

            progress.update(1)

        for domain in domains:
            for link in domains[domain]["occurances"]:
                net.add_edge(domain, domain_from_url(link))

            progress.update(1)

    net.toggle_physics(True)
    net.show(args.output_filename)

def domain_from_url(url):
    if url == "Locations File":
        return url

    return urlparse(url).netloc

def node_shape(domain):
    if "Locations File" == domain:
        return "box"
    else:
        return "ellipse"

def node_color(result):
    if result["error"]:
        return "red"
    elif result["ok"]:
        return "green"
    else:
        return "yellow"
