# Part A

STATEMENTS = [
    ("Every student studies at least one course.",
     "∀x (Student(x) → ∃y (Course(y) ∧ Studies(x,y)))",
     "AX:(student(X) => EY:(course(Y) & studies(X,Y)))"),
    ("Some student studies every course.",
     "∃x (Student(x) ∧ ∀y (Course(y) → Studies(x,y)))",
     "EX:(student(X) & AY:(course(Y) => studies(X,Y)))"),
    ("Every professor teaches at least one course.",
     "∀x (Professor(x) → ∃y (Course(y) ∧ Teaches(x,y)))",
     "AX:(professor(X) => EY:(course(Y) & teaches(X,Y)))"),
    ("There is a course that every student studies.",
     "∃y (Course(y) ∧ ∀x (Student(x) → Studies(x,y)))",
     "EY:(course(Y) & AX:(student(X) => studies(X,Y)))"),
    ("Every student likes some professor.",
     "∀x (Student(x) → ∃y (Professor(y) ∧ Likes(x,y)))",
     "AX:(student(X) => EY:(professor(Y) & likes(X,Y)))"),
]

if __name__ == "__main__":
    for i, (english, fol, fitch) in enumerate(STATEMENTS, 1):
        print(f"{i}. {english}\n   (a) FOL   : {fol}\n   (b) Fitch : {fitch}\n")