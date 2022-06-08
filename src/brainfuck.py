import time

class BrainfuckInterpreter:
    def __init__(self, bfcode):
        self.ptr = 0
        self.array = [0 for _ in range(30000)]
        self.validchars = (">", "<", "+", "-", ".", ",", "[", "]")
        self.bfcode = bfcode
        self.runningloops = []
        self.loops = self.all_loops(self.bfcode)
        self.t = time.time()
        self.interpret()

    def interpret(self):
        position = 0
        count = 0
        while position < len(self.bfcode):
            instruction = self.bfcode[position]

            if instruction not in self.validchars:
                position += 1
                continue
            
            count += 1
            
            if instruction == ".":
                self.output += chr(self.array[self.ptr])

            if instruction == ",":
                new_input = input()
                if len(new_input) != 1:
                    print("invalid input")
                    break
                self.array[self.ptr] = ord(new_input)
            
            if instruction == ">":
                self.ptr = self.ptr if self.ptr == 29999 else self.ptr + 1
            
            if instruction == "<":
                self.ptr = self.ptr if self.ptr == 0 else self.ptr - 1
            
            if instruction == "+":
                self.array[self.ptr] = 0 if self.array[self.ptr] == 255 else self.array[self.ptr] + 1
            
            if instruction == "-":
                self.array[self.ptr] = 255 if self.array[self.ptr] == 0 else self.array[self.ptr] - 1

            if instruction == "[":
                if self.array[self.ptr] == 0:
                    position = self.loops[position] + 1
                    continue
            
            if instruction == "]":
                if self.array[self.ptr] == 0:
                    position += 1
                    continue
                position = self.loops[position]

            position += 1

    def all_loops(self, code):
        loops = {}
        left_loops = []
        for position, instruction in enumerate(code):
            if instruction == "[":
                left_loops.append(position)
            elif instruction == "]":
                left = left_loops.pop()
                right = position
                loops[left] = right
                loops[right] = left
        return loops