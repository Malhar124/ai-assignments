# Q1
import re
import sys
RULES = {
    "START": [
        (r"\b(hello|hi|hey)\b", "Hello, what is your name?", "ASK_NAME"),
    ],
    "ASK_NAME": [
        (r"\bpuzzle\b", "Sure, what is the puzzle?", "GET_PUZZLE"),
        (r"\b(?:my name is|i am|i'm)\s+(\w+)", "Nice to meet you, {0}!", "END"),
    ],
    "GET_PUZZLE": [
        (r".+", "Interesting puzzle. Let me think about it. Now, what is your name?", "ASK_NAME"),
    ],
    "END": [],
}
FALLBACK = "Sorry, I did not understand. Please say it again."


def respond(state, text):
    for pattern, reply, nxt in RULES[state]:
        m = re.search(pattern, text.lower())
        if m:
            return reply.format(*(g.capitalize() for g in m.groups())), nxt
    return FALLBACK, state


def chat():
    state = "START"
    while state != "END":
        try:
            text = input("Human: ").strip()
        except EOFError:
            break
        if text.lower() in {"bye", "exit", "quit"}:
            print("Computer: Goodbye!")
            break
        reply, state = respond(state, text)
        print("Computer:", reply)


def self_test():
    s = "START"
    r, s = respond(s, "Hello, I want to chat with you.")
    assert r == "Hello, what is your name?" and s == "ASK_NAME"
    r, s = respond(s, "I may tell my name if you solve a puzzle for me.")
    assert r == "Sure, what is the puzzle?" and s == "GET_PUZZLE"
    r, s = respond(s, "What has keys but no locks?")
    assert s == "ASK_NAME"
    r, s = respond(s, "My name is malhar")
    assert r == "Nice to meet you, Malhar!" and s == "END"
    assert respond("START", "blah") == (FALLBACK, "START")
    print("All Q1 tests passed.")


if __name__ == "__main__":
    self_test() if sys.argv[1:] == ["test"] else chat()