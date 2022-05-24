import ply.lex as lex

tokens = ["LETTER", "LPAR", "RPAR", "PLUS", "STAR", "SEMI", "EPSILON"]

t_LPAR = r"\("
t_RPAR = r"\)"
t_PLUS = r"\+"
t_STAR = r"\*"
t_SEMI = r";"
t_LETTER = r"[a-zA-Z0-9]"
t_EPSILON = r"\^"


# Ignored characters
t_ignore = " \r\n\t"
t_ignore_COMMENT = r"\#.*"


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    raise Exception("LEXER ERROR")


lexer = lex.lex()
