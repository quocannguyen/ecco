from ..ecco_ast import ASTNode, create_ast_leaf
from ..ecco import GLOBAL_SCANNER
from ..scanning import TokenType, Token
from ..utils import EccoSyntaxError

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
    
def parse_binary_expression() -> ASTNode:
    # Get an integer literal, and scan the next token into GLOBAL_SCANNER.current_token
    left = parse_terminal_node()

    if GLOBAL_SCANNER.current_token.type == TokenType.EOF:
        return left
    
    # If we haven't reached EOF, we're looking at an operator (hopefully)
    # We want to store this value so we can make an AST operator node
    # with integer literals (or sub-expressions) as children
    operator_type = GLOBAL_SCANNER.current_token.type

    # Scan the next token
    GLOBAL_SCANNER.scan()

    # Recursively parses the expression to the right child node
    right = parse_binary_expression()

    return ASTNode(Token(operator_type), left, right)