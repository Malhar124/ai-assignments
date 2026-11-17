# Q2
import sys
from itertools import product

ATOMS = ["p", "q", "r", "s"]
COMPOUND = {
    "p^q": lambda v: v["p"] and v["q"],
    "p^r^s": lambda v: v["p"] and v["r"] and v["s"],
    "(p^r)->s": lambda v: (not (v["p"] and v["r"])) or v["s"],
    "s<->r": lambda v: v["s"] == v["r"],
}
QUESTION = {
    "p": "is a student",
    "q": "has an id no.",
    "r": "gets good skills",
    "s": "has a good package",
}


def tf(b):
    return "T" if b else "F"


def ask_bool(prompt):
    while True:
        a = input(prompt).strip().upper()
        if a in {"T", "F"}:
            return a == "T"
        print("  Please type T or F.")


def row(v):
    return [tf(v[a]) for a in ATOMS] + [tf(f(v)) for f in COMPOUND.values()]


def print_table(rows, first_col):
    header = [first_col] + ATOMS + list(COMPOUND)
    widths = [max(len(str(c)) for c in col) for col in zip(header, *rows)]
    for line in [header] + rows:
        print(" | ".join(str(c).ljust(w) for c, w in zip(line, widths)))


def main():
    n = input("How many persons (x)? ").strip()
    while not n.isdigit() or int(n) < 1:
        n = input("  Please type a positive whole number: ").strip()
    n = int(n)
    rows = []
    for _ in range(n):
        name = input("Name of x: ").strip() or "x"
        v = {a: ask_bool(f"  {a}({name}): {name} {QUESTION[a]}? (T/F) ") for a in ATOMS}
        rows.append([name] + row(v))
    print("\nTruth values for the given persons:")
    print_table(rows, "x")
    print("\nFull truth table (all combinations):")
    full = [[i + 1] + row(dict(zip(ATOMS, bits)))
            for i, bits in enumerate(product([True, False], repeat=4))]
    print_table(full, "#")


def self_test():
    v = {"p": True, "q": False, "r": True, "s": False}
    assert row(v) == ["T", "F", "T", "F", "F", "F", "F", "F"]
    v = {"p": False, "q": True, "r": False, "s": False}
    assert row(v)[4:] == ["F", "F", "T", "T"]
    assert len(list(product([True, False], repeat=4))) == 16
    print("All Q2 tests passed.")


if __name__ == "__main__":
    self_test() if sys.argv[1:] == ["test"] else main()