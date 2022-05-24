import ply.yacc as yacc
from RELexer import tokens
from RENode import RENode


def p_reStart(p):
    "reStart : re SEMI"
    root_node = RENode()
    root_node.operator = "."
    term_child = RENode()
    term_child.operator = "leaf"
    term_child.symbol = ";"
    term_child.nullable = False
    root_node.right_child = term_child
    root_node.left_child = p[1]
    root_node.nullable = p[1].nullable or term_child.nullable
    p[0] = root_node


def p_re_0(p):
    "re : term"
    p[0] = p[1]


def p_re_1(p):
    "re : re PLUS term"
    n = RENode()
    n.operator = "+"
    n.left_child = p[1]
    n.right_child = p[3]
    n.nullable = p[1].nullable or p[3].nullable
    p[0] = n


def p_term_0(p):
    "term : factor"
    p[0] = p[1]


def p_term_1(p):
    "term : term factor"
    n = RENode()
    n.operator = "."
    n.left_child = p[1]
    n.right_child = p[2]
    n.nullable = p[1].nullable and p[2].nullable
    p[0] = n


def p_factor_0(p):
    "factor : unit"
    p[0] = p[1]


def p_factor_1(p):
    "factor : factor STAR"
    n = RENode()
    n.operator = "*"
    n.left_child = p[1]
    n.nullable = True
    p[0] = n


def p_unit_0(p):
    "unit : LETTER"
    n = RENode()
    n.operator = "leaf"
    n.symbol = p[1]
    n.nullable = False
    p[0] = n


def p_unit_1(p):
    "unit : EPSILON"
    n = RENode()
    n.operator = "leaf"
    n.symbol = p[1]
    n.nullable = True
    p[0] = n


def p_unit_2(p):
    "unit : LPAR re RPAR"
    p[0] = p[2]


def p_error(p):
    print("Error in input")


parser = yacc.yacc()
