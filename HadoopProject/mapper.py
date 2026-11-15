
#!/usr/bin/env python3

import sys

for line in sys.stdin:

    line = line.strip()

    if not line:
        continue

    # Split the line into columns
    fields = line.split("\t")

    # Check that there are exactly 6 columns
    if len(fields) != 6:
        continue

    # Extract the useful information
    store = fields[2]
    cost = fields[4]

    # Send store and cost to the Reducer
    print(f"{store}\t{cost}")
