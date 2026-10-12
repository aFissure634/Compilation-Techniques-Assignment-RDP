
tokens = []
pos = 0

def consume():
    global pos
    token = tokens[pos]
    pos += 1
    return token


# Expr -> BExpr ? Expr : Expr
def expr():
    condition = bexpr()

    if consume() != "?":
        raise ValueError("Expected ?")

    true_branch = arithmetic()

    if consume() != ":":
        raise ValueError("Expected :")

    false_branch = arithmetic()

    if condition:
        return true_branch
    else:
        return false_branch


# BExpr -> BTerm { OR BTerm }
def bexpr():
    result = bterm()

    while pos < len(tokens) and tokens[pos] == "OR":
        consume()
        right = bterm()
        result = result or right

    return result


# BTerm -> BFactor { AND BFactor }
def bterm():
    result = bfactor()

    while pos < len(tokens) and tokens[pos] == "AND":
        consume()
        right = bfactor()
        result = result and right

    return result


# BFactor -> true | false | (BExpr)
def bfactor():
    token = consume()

    if token == "true":
        return True

    if token == "false":
        return False

    if token == "(":
        result = bexpr()

        if consume() != ")":
            raise ValueError("Expected )")

        return result

    raise ValueError("Invalid Boolean factor")


# Simple arithmetic for the branches
def arithmetic():
    result = int(consume())

    while pos < len(tokens) and tokens[pos] in ["+", "-", "*"]:
        operator = consume()
        number = int(consume())

        if operator == "+":
            result += number
        elif operator == "-":
            result -= number
        else:
            result *= number

    return result


# Run the parser
def evaluate(text):
    global tokens, pos

    tokens = text.replace("(", " ( ").replace(")", " ) ").split()
    pos = 0

    answer = expr()

    if pos != len(tokens):
        raise ValueError("Unexpected extra tokens")

    return answer


print(evaluate("true ? 10 : 20"))
print(evaluate("false ? 3 + 4 : 5 * 2"))
