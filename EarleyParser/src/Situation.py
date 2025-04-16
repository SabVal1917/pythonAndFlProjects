class Situation:
    def __init__(self, left_part="", right_part="", dot_index=0, left_index=0):
        self.left_part = left_part
        self.right_part = right_part
        self.dot_index = dot_index
        self.left_index = left_index

    def __hash__(self):
        return hash((self.left_part, self.right_part, self.dot_index, self.left_index))

    def __eq__(self, other):
        return (self.left_part == other.left_part) and (self.right_part == other.right_part) and (
                    self.dot_index == other.dot_index) and (self.left_index == other.left_index)

    def __str__(self):
        return "(" + str(self.left_part) + "->" + (
                str(self.right_part)[0:self.dot_index] + "." + str(self.right_part)[self.dot_index:]) + ", " + str(
            self.left_index) + ")"
