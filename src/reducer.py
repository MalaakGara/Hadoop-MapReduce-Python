
#!/usr/bin/env python3
"""Reducer Hadoop Streaming : calcule le total des ventes par magasin."""

import sys
from decimal import Decimal, InvalidOperation


def parse_line(line):
    """Retourne (store, cost) ou None si la ligne est invalide."""
    line = line.rstrip("\n")

    if not line.strip():
        return None

    parts = line.rsplit("\t", 1)

    if len(parts) != 2:
        return None

    store = parts[0].strip()
    raw_cost = parts[1].strip()

    if not store:
        return None

    try:
        cost = Decimal(raw_cost)
    except InvalidOperation:
        return None

    if not cost.is_finite():
        return None

    return store, cost


def main():
    current_store = None
    total = Decimal("0")

    # Hadoop trie les données par magasin avant le Reducer.
    for line in sys.stdin:
        parsed = parse_line(line)

        if parsed is None:
            continue

        store, cost = parsed

        if store == current_store:
            total += cost
        else:
            if current_store is not None:
                print("{}\t{:.2f}".format(current_store, total))

            current_store = store
            total = cost

    if current_store is not None:
        print("{}\t{:.2f}".format(current_store, total))


if __name__ == "__main__":
    main()
