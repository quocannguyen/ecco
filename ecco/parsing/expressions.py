from ..ecco_ast import ASTNode, create_ast_leaf
from ..ecco import GLOBAL_SCANNER
from ..scanning import TokenType, Token
from ..utils import EccoSyntaxError
from typing import Dict

OPERATOR_PRECEDENCE: Dict[TokenType, int] = {
    TokenType.LEFT_SHIFT: 11,
    TokenType.RIGHT_SHIFT: 11,
    TokenType.PLUS: 12,
    TokenType.MINUS: 12,
    TokenType.STAR: 13,
    TokenType.SLASH: 13,
}

def parse_terminal_node() -> ASTNode:
    """
    Get an integer literal, and scan the next token into GLOBAL_SCANNER.current_token
    """
    terminal_node: ASTNode
    if GLOBAL_SCANNER.current_token.type == TokenType.INTEGER_LITERAL:
        terminal_node = create_ast_leaf(GLOBAL_SCANNER.current_token)
        GLOBAL_SCANNER.scan()  # Scan the next token
        return terminal_node
    else:
        raise EccoSyntaxError(
            f'Expected terminal Token but got "{str(GLOBAL_SCANNER.current_token.type)}"'
        )
    
def get_operator_precedence(operator_type: TokenType) -> int:
    """Gets an operator's precedence

    Args:
        operator_type (TokenType)

    Raises:
        EccoSyntaxError: If operator_type is a non-operator type

    Returns:
        int: The precedence of the passed operator Token
    """
    if operator_type not in OPERATOR_PRECEDENCE:
        raise EccoSyntaxError(f"Expected operator but got {operator_type}")
    return OPERATOR_PRECEDENCE[operator_type]
    
def parse_binary_expression(previous_operator_precedence: int=0) -> ASTNode:
    """Recursively build the binary expressions' AST
    Args:
        previous_operator_precedence (int)
    Raises:
        EccoSyntaxError: If operator_type is a non-operator type
    Returns:
        ASTNode: The binary expressions' AST
    """
    # Get an integer literal, and scan the next token into GLOBAL_SCANNER.current_token
    left_ast_child = parse_terminal_node()

    operator_type = GLOBAL_SCANNER.current_token.type  # Assume the next token is an operator
    # Loop while not EOF and operator takes precedence over the previous
    while (
        operator_type != TokenType.EOF and
        get_operator_precedence(operator_type) > previous_operator_precedence
    ):
        GLOBAL_SCANNER.scan()  # Scan the next token
        # Recursively build the right AST subtree with operators of higher precedence
        right_subtree = parse_binary_expression(OPERATOR_PRECEDENCE[operator_type])

        # Update left AST subtree
        left_ast_child = ASTNode(Token(operator_type), left_ast_child, right_subtree)
        # Update operator_type
        operator_type = GLOBAL_SCANNER.current_token.type

    return left_ast_child