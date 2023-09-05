from .scanning import Token
from copy import deepcopy

class ASTNode():
    def __init__(self, token: Token, left_child=None, right_child=None) -> None:
        # Copy value, not reference
        self.token: Token = deepcopy(token)

        self.left_child: ASTNode = left_child
        if left_child:
            self.left_child.parent = self
        self.right_child: ASTNode = right_child
        if right_child:
            self.right_child.parent = self
        
        self.parent: ASTNode = None

def create_ast_leaf(token: Token) -> ASTNode:
    return ASTNode(token, None, None)