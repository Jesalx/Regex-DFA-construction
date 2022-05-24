import sys
from REParser import parser
from RENode import RENode


def read_input(prompt_text):
    """
    Reads in user input line by line until a ";" is entered.
    """
    result = []
    while True:
        data = input(f"{prompt_text}: ").strip()
        if ";" in data:
            i = data.index(";")
            result += data[0 : i + 1]
            break
        else:
            result.append(data + " ")
    return "".join(result)


def nodepos(root: RENode):
    """
    Takes in a root node and labels the nodes with their position in the tree
    using a post-order traversal where only leaf nodes get labeled.
    """
    position = 1

    def nodepos_helper(node: RENode):
        if not node:
            return
        nodepos_helper(node.left_child)
        nodepos_helper(node.right_child)
        if node.symbol:
            nonlocal position
            node.position = position
            position += 1

    nodepos_helper(root)


def firstpos(node: RENode):
    """
    Caculates firstpos for every node in the tree.
    """
    if not node:
        return
    firstpos(node.left_child)
    firstpos(node.right_child)

    if node.operator == "leaf" and node.symbol != "^":
        node.firstpos.add(node.position)
    elif node.operator == "+":
        node.firstpos = node.left_child.firstpos.union(node.right_child.firstpos)
    elif node.operator == ".":
        if node.left_child.nullable:
            node.firstpos = node.left_child.firstpos.union(node.right_child.firstpos)
        else:
            node.firstpos = node.left_child.firstpos
    elif node.operator == "*":
        node.firstpos = node.left_child.firstpos


def lastpos(node: RENode):
    """
    Calculates finalpos for every node in the tree.
    """
    if node is None:
        return
    lastpos(node.left_child)
    lastpos(node.right_child)

    if node.operator == "leaf" and node.symbol != "^":
        node.lastpos.add(node.position)
    elif node.operator == "+":
        node.lastpos = node.left_child.lastpos.union(node.right_child.lastpos)
    elif node.operator == ".":
        if node.right_child.nullable:
            node.lastpos = node.left_child.lastpos.union(node.right_child.lastpos)
        else:
            node.lastpos = node.right_child.lastpos
    elif node.operator == "*":
        node.lastpos = node.left_child.lastpos


def followpos(node: RENode):
    """
    Calculates followpos for every node in the tree. This function returns
    a dictionary mapping a node's position to a node object in the tree and an
    additional dictionary mapping a node's position to a set of its followpos.
    """
    num_to_node = dict()

    def getpositions(node: RENode, num_to_node: dict):
        if not node:
            return
        getpositions(node.left_child, num_to_node)
        getpositions(node.right_child, num_to_node)

        if node.symbol:
            num_to_node[node.position] = node

    getpositions(node, num_to_node)

    followpos_dict = dict()

    def followpos_helper(node: RENode):
        if not node:
            return
        followpos_helper(node.left_child)
        followpos_helper(node.right_child)

        if node.operator in ("+", "."):
            for position in node.left_child.lastpos:
                if position not in followpos_dict:
                    followpos_dict[position] = set()
                followpos_dict[position] = followpos_dict[position].union(
                    node.right_child.firstpos
                )
        elif node.operator == "*":
            for position in node.lastpos:
                if position not in followpos_dict:
                    followpos_dict[position] = set()
                followpos_dict[position] = followpos_dict[position].union(node.firstpos)

    followpos_helper(node)

    for position in num_to_node:
        if position not in followpos_dict:
            followpos_dict[position] = set()

    return num_to_node, followpos_dict


class DFANode:
    """
    Class for a node in a DFA containing information including information
    about the state of the node, the states that this node can transition to,
    and whether or not this node is a start or final state.
    """

    alphabet = set()

    def __init__(self, state=None, start=False):
        if state is None:
            self.state = set()
        self.state = state
        self.marked = False
        self.transitions = dict()
        self.start = start
        self.final = False


def dfa(node: RENode, tree_followpos: dict, num_to_node: dict, should_print: bool):
    """
    Constructs the DFA when provided the root RENode of the tree, the followpos
    dictionary, the num_to_node dictionary, and a boolean indicating whether or
    not the DFA should be printed. This function returns the DFANode representing
    the start state of the DFA.
    """

    def find_unmarked(states: dict):
        for node in states.values():
            if not node.marked:
                return node
        return None

    states = dict()
    start_transition = tuple(sorted(node.firstpos))
    states[start_transition] = DFANode(node.firstpos, start=True)

    while find_unmarked(states):
        current_state = find_unmarked(states)
        current_state.marked = True
        letters_in_state = set()
        for pos in current_state.state:
            letters_in_state.add(num_to_node[pos].symbol)
        if ";" in letters_in_state:
            current_state.final = True
        transitions = dict()
        for letter in letters_in_state:
            transitions[letter] = set()
            DFANode.alphabet.add(letter)
        for pos in current_state.state:
            letter = num_to_node[pos].symbol
            transitions[letter] = transitions[letter].union(tree_followpos[pos])
        for letter, transition in transitions.items():
            hashable_transition = tuple(sorted(transition))
            if hashable_transition not in states:
                states[hashable_transition] = DFANode(transition)
            current_state.transitions[letter] = states[hashable_transition]
        if should_print:
            if current_state.start:
                print(f"start_state({current_state.state})")
            for letter, transition in transitions.items():
                if letter == ";":
                    continue
                print(f"delta({current_state.state},{letter},{transition})")
    if should_print:
        for node in states.values():
            if node.final:
                print(f"final_state({node.state})")

    return states[start_transition]


def follow_dfa(node: DFANode, input_string: str, idx: int):
    """
    Follows the DFA as long as possible where we will either find
    a character that has no valid transitions or we will consume
    # the string and see if we end on a final state.
    """
    if not input_string or idx >= len(input_string):
        if node.final:
            return "MATCH"
        return "NO MATCH"

    letter = input_string[idx]
    if letter in DFANode.alphabet:
        if letter in node.transitions:
            return follow_dfa(node.transitions[letter], input_string, idx + 1)
        else:
            return "NO MATCH"
    else:
        return "NO MATCH: Invalid input character"


def main():
    """
    Program loop to keep gathering regular expressions and input strings
    to return whether or not they match the regular expression.
    """
    print_dfa = False
    for arg in sys.argv[1:]:
        if arg == "-dfa":
            print_dfa = True
    while True:
        data = read_input("REGEX")
        if data == "exit;":
            break
        try:
            tree = parser.parse(data)
        except Exception as inst:
            print(inst.args[0])
            continue
        try:
            nodepos(tree)
            firstpos(tree)
            lastpos(tree)
            num_to_node, tree_followpos = followpos(tree)
            start = dfa(tree, tree_followpos, num_to_node, print_dfa)
            while True:
                input_data = read_input("  INPUT STRING")
                if input_data == "exit;":
                    break
                try:
                    print("  " + follow_dfa(start, input_data[:-1], 0))
                except Exception as inst:
                    print(inst)
        except Exception as inst:
            print(inst)


if __name__ == "__main__":
    main()
