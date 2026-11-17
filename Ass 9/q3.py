# Part D
RULES_STRONG = [
    (["Robot"], "Agent"),
    (["Agent", "DetectsObstacle"], "TakesAction"),
]
FACTS = {("Robot", "R1"), ("DetectsObstacle", "R1")}


def forward_chain(facts, rules, verbose=True):
    facts = set(facts)
    while True:
        new = set()
        for premises, conclusion in rules:
            for obj in {o for _, o in facts}:
                if all((p, obj) in facts for p in premises) and (conclusion, obj) not in facts:
                    new.add((conclusion, obj))
                    if verbose:
                        used = " ∧ ".join(f"{p}({obj})" for p in premises)
                        rule = " ∧ ".join(f"{p}(x)" for p in premises)
                        print(f"  From {used} and rule {rule} → {conclusion}(x),"
                              f" with {{x/{obj}}}: infer {conclusion}({obj})")
        if not new:
            return facts
        facts |= new


def main():
    print("Q2. Forward chaining (Universal Elimination + Modus Ponens):")
    kb = forward_chain(FACTS, RULES_STRONG)
    print("  TakesAction(R1) proved:", ("TakesAction", "R1") in kb, "\n")

    print("Q3. Weak KB: ∃x (Agent(x) ∧ DetectsObstacle(x) ∧ TakesAction(x))")
    weak_facts = FACTS | {("Agent", "A1"), ("DetectsObstacle", "A1"), ("TakesAction", "A1")}
    kb = forward_chain(weak_facts, [(["Robot"], "Agent")], verbose=False)
    print("  TakesAction(R1) proved:", ("TakesAction", "R1") in kb)
    print("  Reason: the existential talks about some agent A1, not necessarily R1.")
    print("  Needed: R1 is one of those agents (TakesAction(R1) directly), or the universal rule back.")


if __name__ == "__main__":
    assert ("TakesAction", "R1") in forward_chain(FACTS, RULES_STRONG, verbose=False)
    main()