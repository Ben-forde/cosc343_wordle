from platform import node

import my_agent


class node:
    def __init__(self, s, parent=None, g=0, h=0, action=None):
        self.s = s
        self.parent = parent
        self.g = g
        self.f = g + h
        self.action = action


init_state = len(my_agent.get_dictionary("dictionaries/english.txt"))
goal_state = 1
root_node = node(s=init_state, parent=None, g=0, h=len(my_agent.delete_words()))

print(init_state)
