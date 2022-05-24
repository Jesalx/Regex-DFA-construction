class RENode:
    def __init__(self):
        self.operator = ""  # '*', '.', '+', 'leaf'
        self.symbol = ""  # only for leaf nodes
        self.position = 0  # only for non-^ leaf nodes
        self.left_child: RENode = None
        self.right_child: RENode = None  # only for . and +
        self.nullable = False
        self.firstpos = set()
        self.lastpos = set()

    def to_string(self, indentation_level):
        result = " " * indentation_level
        if self.operator == "leaf":
            result += "SYMBOL: " + self.symbol
            result += " POS: " + str(self.position)
            result += " NULLABLE=" + str(self.nullable)
            result += " FIRSTPOS=" + str(self.firstpos)
            result += " LASTPOS=" + str(self.lastpos) + "\n"
        elif self.operator == "*":
            result += "OPERATOR: STAR"
            result += " NULLABLE=" + str(self.nullable)
            result += " FIRSTPOS=" + str(self.firstpos)
            result += " LASTPOS=" + str(self.lastpos) + "\n"
            result += self.left_child.to_string(indentation_level + 2)
        elif self.operator == ".":
            result += "OPERATOR: DOT"
            result += " NULLABLE=" + str(self.nullable)
            result += " FIRSTPOS=" + str(self.firstpos)
            result += " LASTPOS=" + str(self.lastpos) + "\n"
            result += self.left_child.to_string(indentation_level + 2)
            result += self.right_child.to_string(indentation_level + 2)
        elif self.operator == "+":
            result += "OPERATOR: PLUS"
            result += " NULLABLE=" + str(self.nullable)
            result += " FIRSTPOS=" + str(self.firstpos)
            result += " LASTPOS=" + str(self.lastpos) + "\n"
            result += self.left_child.to_string(indentation_level + 2)
            result += self.right_child.to_string(indentation_level + 2)
        else:
            result += "SOMETHING WENT WRONG"
        return result

    def __str__(self):
        return self.to_string(0)
