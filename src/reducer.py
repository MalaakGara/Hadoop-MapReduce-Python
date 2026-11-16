
#!/usr/bin/env python3

import sys
from collections import defaultdict
from decimal import Decimal

# Store the total for every store
totals = defaultdict(Decimal)

for line in sys.stdin:

    line = line.strip()

    if not line:
        continue

    # Separate store and cost
    store, cost = line.split("\t", 1)

    # Add the purchase amount
    totals[store] += Decimal(cost)

# Display the final totals
for store in sorted(totals):
    print(f"{store}\t{totals[store]:.2f}")