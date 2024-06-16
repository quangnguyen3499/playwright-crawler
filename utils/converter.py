def convert_parentheses_to_number(s):
    if isinstance(s, str) and s.startswith("(") and s.endswith(")"):
        return int(s[1:-1])
    return s
