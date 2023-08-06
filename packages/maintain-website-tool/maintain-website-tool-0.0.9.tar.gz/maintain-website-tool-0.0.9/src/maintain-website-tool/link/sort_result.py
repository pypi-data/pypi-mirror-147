from .io import write_file, load_file

def sort_result(args):
    """Sort a result by (OR):
    - ok
    - status code
    - latency
    - errors
    """
    result = load_file(args.filename, format=args.in_format if args.in_format is not None else args.format)

    sorted_result = {}
    for url in result:

        if (args.ok is result[url].get("ok", None) and args.ok is not None) or (args.status_code == result[url].get("status_code", None) and args.status_code is not None) or (args.latency is not None and result[url]["latency"] > args.latency) or (args.error and result[url].get("error", None) is not None):
            sorted_result[url] = result[url]
        else:
            sorted_result[url] = {}

    write_file(sorted_result, format=args.out_format if args.out_format is not None else args.format)
