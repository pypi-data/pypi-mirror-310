from __future__ import annotations

import sys

import yaml

from .openapi import OpenAPI


def main():
    specfile = sys.argv[1]

    with open(specfile) as f:
        spec = yaml.safe_load(f.read())

    o = OpenAPI(spec, validate=True)

    errors = o.errors()

    if errors:
        # print errors
        for e in errors:
            print("{}: {}".format(".".join(e.path), e.message[:300]))
        print()
        print(f"{len(errors)} errors")
        sys.exit(1)  # exit with error status
    else:
        print("OK")


if __name__ == "__main__":
    main()
