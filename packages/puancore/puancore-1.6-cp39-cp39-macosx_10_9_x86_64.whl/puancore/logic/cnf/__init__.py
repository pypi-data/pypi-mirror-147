import typing

# propositional logic functions
def parse_cnf_ast(cnf_ast: tuple, lit2var: typing.Callable = None) -> list:

    """
        # parse_ast
        Turns cnf ast-tree expressions on form ('and', ('or', ('lit', -1), ('lit', -2), ...), ...)
        to a more described list view of the cnf ast-tree: [[("a", -1), ("b", -1), ...], ...], if
        1=a, 2=b and -1 is negated.

        The lit2var -function should take a positive integer as input
        and return a string variable name. If no such function is applied, the original value is returned.

        Return:
            list-like: [[("a", -1), ("b", -1), ...], ...]
    """

    if isinstance(cnf_ast, int):
        variable = lit2var(abs(cnf_ast)) if callable(lit2var) else cnf_ast
        return (variable, -1 if cnf_ast < 0 else 1)

    ast = list(cnf_ast)
    op = ast[0]
    if op == "and":
        return [parse_cnf_ast(clause, lit2var) for clause in ast[1:]]
    elif op == "or":
        return [parse_cnf_ast(clause, lit2var) for clause in ast[1:]]
    elif op == "lit":
        return parse_cnf_ast(ast[1], lit2var)
    else:
        raise Exception(f"could not handle operator {op} when parsing ast-tree {ast}")

