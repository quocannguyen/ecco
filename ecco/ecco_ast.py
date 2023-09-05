from .scanning import Token
from copy import deepcopy

class ASTNode():
    def __init__(self, token: Token, left=None, right=None) -> None:
        # Copy value, not reference
        self.token: Token = deepcopy(token)

        self.left: ASTNode = left
        if left:
            self.left.parent = self
        self.right: ASTNode = right
        if right:
            self.right.parent = self
        
        self.parent: ASTNode = None

def create_ast_leaf(token: Token) -> ASTNode:
    return ASTNode(token, None, None)