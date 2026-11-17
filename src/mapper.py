
#!/usr/bin/env python3
"""Mapper Hadoop Streaming : extrait le magasin et le coût de chaque achat."""

import re
import sys
from decimal import Decimal, InvalidOperation

# Separateur : tabulations ou deux espaces ou plus.
SEPARATOR = re.compile(r"\t+|\s{2,}")
EXPECTED_COLUMNS = 6


def parse_line(line):
    """Retourne (store, cost) ou None si la ligne est invalide."""
    line = line.strip()

    if not line:
        return None

    fields = [field.strip() for field in SEPARATOR.split(line)]

    if len(fields) != EXPECTED_COLUMNS:
        return None

    store = fields[2]

    if not store:
        return None

    try:
        cost = Decimal(fields[4])
    except InvalidOperation:
        return None

    if not cost.is_finite():
        return None

    return store, cost


def main():
    for line in sys.stdin:
        parsed = parse_line(line)

        if parsed is None:
            continue

        store, cost = parsed
        print("{}\t{}".format(store, cost))


if __name__ == "__main__":
    main()
