# Q3
import sys

ARMEMPTY = ("ARMEMPTY",)


def operator(name, a, b=None):
    if name == "PICKUP":
        pre = [("ONTABLE", a), ("CLEAR", a), ARMEMPTY]
        return pre, {("HOLDING", a)}, set(pre)
    if name == "PUTDOWN":
        return [("HOLDING", a)], {("ONTABLE", a), ("CLEAR", a), ARMEMPTY}, {("HOLDING", a)}
    if name == "UNSTACK":
        pre = [("ON", a, b), ("CLEAR", a), ARMEMPTY]
        return pre, {("HOLDING", a), ("CLEAR", b)}, set(pre)
    if name == "STACK":
        return [("CLEAR", b), ("HOLDING", a)], {("ON", a, b), ("CLEAR", a), ARMEMPTY}, \
            {("HOLDING", a), ("CLEAR", b)}
    raise ValueError(name)


def choose_operator(goal, state):
    kind = goal[0]
    if kind == "ON":
        return ("STACK", goal[1], goal[2])
    if kind == "ONTABLE":
        return ("PUTDOWN", goal[1])
    if kind == "HOLDING":
        a = goal[1]
        if ("ONTABLE", a) in state:
            return ("PICKUP", a)
        under = next(p[2] for p in state if p[0] == "ON" and p[1] == a)
        return ("UNSTACK", a, under)
    if kind == "CLEAR":
        a = goal[1]
        if ("HOLDING", a) in state:
            return ("PUTDOWN", a)
        top = next(p[1] for p in state if p[0] == "ON" and p[2] == a)
        return ("UNSTACK", top, a)
    if kind == "ARMEMPTY":
        held = next(p[1] for p in state if p[0] == "HOLDING")
        return ("PUTDOWN", held)
    raise ValueError(goal)


def show(item):
    if item[0] == "AND":
        return " ^ ".join(show(g) for g in item[1])
    if item[0] == "OP":
        return "[" + item[1][0] + "(" + ",".join(item[1][1:]) + ")]"
    return item[0] + ("(" + ",".join(item[1:]) + ")" if len(item) > 1 else "")


def goal_stack_plan(state, goals, verbose=True, max_steps=500):
    state, plan = set(state), []
    stack = [("AND", tuple(goals))] + list(reversed(goals))
    for step in range(max_steps):
        if not stack:
            return plan, state
        if verbose:
            print(f"Step {step + 1:>2} | Stack (top first): " + " / ".join(show(i) for i in reversed(stack)))
        item = stack.pop()
        if item[0] == "OP":
            pre, add, delete = operator(*item[1])
            assert all(p in state for p in pre), f"precondition failed for {show(item)}"
            state = (state - delete) | add
            plan.append(item[1])
            if verbose:
                print(f"        | EXECUTE {show(item)}, State: {sorted(map(show, state))}")
        elif item[0] == "AND":
            missing = [g for g in item[1] if g not in state]
            if missing:
                stack.append(item)
                stack.extend(reversed(missing))
        elif item not in state:
            op = choose_operator(item, state)
            pre = operator(*op)[0]
            stack.append(("OP", op))
            stack.append(("AND", tuple(pre)))
            stack.extend(reversed(pre))
            if verbose:
                print(f"        | {show(item)} is false, push {show(('OP', op))} and its preconditions")
    raise RuntimeError("no plan found within the step limit")


def on_table(*blocks):
    s = {ARMEMPTY}
    for b in blocks:
        s |= {("ONTABLE", b), ("CLEAR", b)}
    return s


def self_test():
    plan, final = goal_stack_plan(on_table("w", "x", "y", "z"),
                                  [("ON", "x", "y"), ("ON", "z", "w")], verbose=False)
    assert plan == [("PICKUP", "x"), ("STACK", "x", "y"), ("PICKUP", "z"), ("STACK", "z", "w")]
    assert {("ON", "x", "y"), ("ON", "z", "w")} <= final
    s0 = {("ON", "A", "B"), ("ONTABLE", "B"), ("CLEAR", "A"), ARMEMPTY}
    goal = [("ON", "B", "A"), ("ONTABLE", "A"), ("CLEAR", "B"), ARMEMPTY]
    plan, final = goal_stack_plan(s0, goal, verbose=False)
    assert plan == [("UNSTACK", "A", "B"), ("PUTDOWN", "A"), ("PICKUP", "B"), ("STACK", "B", "A")]
    assert set(goal) <= final
    print("All Q3 tests passed.")


def main():
    initial = on_table("w", "x", "y", "z")
    goal = [("ON", "x", "y"), ("ON", "z", "w")]
    print("Initial state:", sorted(map(show, initial)))
    print("Goal state   :", " ^ ".join(map(show, goal)), "\n")
    plan, final = goal_stack_plan(initial, goal)
    print("\nPlan:", ", ".join(show(("OP", op)) for op in plan))
    print("Final state:", sorted(map(show, final)))


if __name__ == "__main__":
    self_test() if sys.argv[1:] == ["test"] else main()