"""Lab: Score table extraction at cell, row, and table level.

What this teaches: "the parser is 80% accurate" is meaningless until
you say at which level. Cell level counts individual values. Row
level counts records that survive whole. Table level counts
documents that are fully right. The same system posts three very
different numbers, and the level you report should match the level
your users consume.

How to run: python3 extraction_accuracy.py
"""

# Gold tables: what the documents actually say.
GOLD_TABLES = [
    [  # invoice 1042
        ["Item", "Qty", "Price"],
        ["Widget", "2", "100"],
        ["Gadget", "1", "50"],
    ],
    [  # invoice 1043
        ["Item", "Qty", "Price"],
        ["Cable", "5", "10"],
        ["Adapter", "2", "25"],
    ],
    [  # invoice 1044
        ["Item", "Qty", "Price"],
        ["Sensor", "3", "70"],
    ],
]

# Extracted tables: what the parser produced. Errors planted:
# table 1 has one wrong cell, table 2 lost a row, table 3 is perfect.
EXTRACTED_TABLES = [
    [
        ["Item", "Qty", "Price"],
        ["Widget", "2", "100"],
        ["Gadget", "1", "55"],
    ],
    [
        ["Item", "Qty", "Price"],
        ["Cable", "5", "10"],
    ],
    [
        ["Item", "Qty", "Price"],
        ["Sensor", "3", "70"],
    ],
]


def cell_accuracy(gold, extracted):
    """Fraction of gold cells reproduced exactly, position by position.
    A missing row makes every cell in it wrong."""
    correct = 0
    total = 0
    for g_table, e_table in zip(gold, extracted):
        for r, g_row in enumerate(g_table):
            e_row = e_table[r] if r < len(e_table) else []
            for c, g_cell in enumerate(g_row):
                total += 1
                if c < len(e_row) and e_row[c] == g_cell:
                    correct += 1
    return correct, total


def row_accuracy(gold, extracted):
    """Fraction of gold rows reproduced exactly and completely."""
    correct = 0
    total = 0
    for g_table, e_table in zip(gold, extracted):
        for r, g_row in enumerate(g_table):
            total += 1
            if r < len(e_table) and e_table[r] == g_row:
                correct += 1
    return correct, total


def table_accuracy(gold, extracted):
    """Fraction of tables with every cell right. One wrong cell fails
    the whole table, because a downstream user gets the whole table."""
    correct = sum(1 for g, e in zip(gold, extracted) if g == e)
    return correct, len(gold)


def main():
    c_ok, c_total = cell_accuracy(GOLD_TABLES, EXTRACTED_TABLES)
    r_ok, r_total = row_accuracy(GOLD_TABLES, EXTRACTED_TABLES)
    t_ok, t_total = table_accuracy(GOLD_TABLES, EXTRACTED_TABLES)

    print(f"Tables scored: {len(GOLD_TABLES)}")
    print()
    print(f"  Cell level:  {c_ok}/{c_total} cells right    = {c_ok / c_total:.0%}")
    print(f"  Row level:   {r_ok}/{r_total} rows right     = {r_ok / r_total:.0%}")
    print(f"  Table level: {t_ok}/{t_total} tables fully right = {t_ok / t_total:.0%}")
    print()
    print("Same parser, three numbers. Cell level flatters: one wrong price")
    print("in a big table barely moves it. Table level is the harshest and")
    print("often the honest one, because users load whole tables into")
    print("reports. Pick the level your users consume, state it every time")
    print("you quote the number, and never compare numbers across levels.")


if __name__ == "__main__":
    main()
