# Part B
from itertools import product

STUDENTS = ["s1", "s2"]
COURSES = ["c1", "c2"]


def f1(studies):
    return all(any((x, y) in studies for y in COURSES) for x in STUDENTS)


def f2(studies):
    return any(all((x, y) in studies for x in STUDENTS) for y in COURSES)


def main():
    example = {("s1", "c1"), ("s2", "c2")}
    print("Example model: students", STUDENTS, "courses", COURSES)
    print("Studies =", sorted(example))
    print("F1 =", f1(example), " (s1 studies c1, s2 studies c2)")
    print("F2 =", f2(example), " (no single course is studied by both)")
    print("So F1 and F2 are NOT equivalent.\n")

    pairs = list(product(STUDENTS, COURSES))
    models = [{p for p, keep in zip(pairs, bits) if keep}
              for bits in product([0, 1], repeat=len(pairs))]
    print("F2 ⊨ F1 in all", len(models), "models:", all(f1(m) for m in models if f2(m)))
    print("F1 ⊨ F2 in all", len(models), "models:", all(f2(m) for m in models if f1(m)))


if __name__ == "__main__":
    assert f1({("s1", "c1"), ("s2", "c2")}) and not f2({("s1", "c1"), ("s2", "c2")})
    main()