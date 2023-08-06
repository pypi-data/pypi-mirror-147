from .io import load_file, write_file

def diff_results(args):
    filename_a = args.filename_a
    filename_b = args.filename_b

    if filename_a == "-":
        raise Exception("Only one file can be stdin")


    result_a = load_file(filename_a, format=args.format if args.in_format is None else  args.in_format)
    result_b = load_file(filename_b, format=args.format if args.in_format is None else args.in_format)

    diff = {}

    for url in result_a:
        diff[url] = { field: take_diff(result_a[url][field], result_b[url][field]) for field in result_a[url] }

    write_file(diff, format=args.format if args.out_format is None else args.out_format)

def take_diff(a, b):
    print(f"Diffing {a} {b}")
    if type(a) == list:
        return a > b
    elif b is None:
        return a
    elif a is None:
        return b
    elif type(a) is str and type(b) is str:
        return a > b
    else:
        return a - b
