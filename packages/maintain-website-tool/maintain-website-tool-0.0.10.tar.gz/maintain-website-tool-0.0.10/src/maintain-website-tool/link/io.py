import sys
import json
import yaml
import csv

def or_none(fn):
    return lambda x: fn(x) if x != "" else None

CSV_FIELDS = {
    "url": or_none(lambda u: u[1:-1]),
    "ok": or_none(lambda o: o == "True"),
    "status_code": or_none(int),
    "latency": or_none(float),
    "occurances": or_none(lambda o: json.loads(o.replace("'", '"'))),
    "error": or_none(str)
}

def load_file(filename, format = "json"):
    """
    Load a file and parse it according to the format
    """
    def open_file_or_stdin(filename):
        if filename == "-":
            return sys.stdin
        else:
            return open(filename)

    with open_file_or_stdin(filename) as f:

        if format == "json":
            return json.load(f)
        elif format in ["yaml", "yml"]:
            return yaml.safe_load(f)
        elif format == "csv":
            reader = csv.DictReader(f)
            result = {}
            for row in reader:
                result[row["url"]] = { r: CSV_FIELDS[r](row[r]) for r in row if r != "url" }
            return result

def write_file(result, file_handler=sys.stdout, format = "json"):
    """
    Write a result to a file (stdout by default) according to the
    format.
    """
    if format == "json":
        return json.dump(result, file_handler)
    elif format in ["yml", "yaml"]:
        return yaml.dump(result, file_handler)
    elif format == "csv":
        fieldnames = CSV_FIELDS.keys()

        writer = csv.DictWriter(file_handler, fieldnames=fieldnames)

        writer.writeheader()

        for url in result:
            writer.writerow({ field: result[url].get(field,None) for field in result[url] } | { "url" : url })
