from .scanning import Scanner, TokenType
from .utils import get_args, setup_tracebacks, EccoFatalException
from .ecco_ast import ASTNode

DEBUG = True
GLOBAL_SCANNER: Scanner

def main():
    """Entrypoint for the compiler"""
    args = get_args()
    global GLOBAL_SCANNER

    GLOBAL_SCANNER = Scanner(args.PROGRAM)
    GLOBAL_SCANNER.open()
    
    setup_tracebacks()
    GLOBAL_SCANNER.scan()

    # Import from .parsing after initialzing GLOBAL_SCANNER
    # To avoid "partially initialized" error (most likely a circular import)
    from .parsing import (
        parse_binary_expression,
    )

    parsed_ast = parse_binary_expression()

    def interpret_ast(root: ASTNode) -> int:
        left_value: int
        right_value: int
        
        if root.left_child:
            left_value = interpret_ast(root.left_child)
        if root.right_child:
            right_value = interpret_ast(root.right_child)

        if root.token.type == TokenType.PLUS:
            return left_value + right_value
        elif root.token.type == TokenType.MINUS:
            return left_value - right_value
        elif root.token.type == TokenType.STAR:
            return left_value * right_value
        elif root.token.type == TokenType.SLASH:
            return left_value // right_value
        elif root.token.type == TokenType.INTEGER_LITERAL:
            return root.token.value
        else:
            raise EccoFatalException(
                "FATAL",
                f'Unknown token "{str(root.token.type)}" encountered'
            )
    
    print(interpret_ast(parsed_ast))

    GLOBAL_SCANNER.close()


if __name__ == "__main__":
    main()
