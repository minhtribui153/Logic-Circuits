from enum import Enum


# Create a Gate Enum
class GateType(Enum):
    AND = 0
    OR = 1
    NOT = 2
    NAND = 3
    NOR = 4
    XOR = 5
    XNOR = 6

class LogicGate:
    def __init__(self, type: GateType, inputs: list):
        if type == GateType.NOT and len(inputs) != 1:
            raise ValueError("Provide only 1 input")
        elif type != GateType.NOT and len(inputs) != 2:
            raise ValueError("Provide only 2 inputs")

        self.type = type
        self.inputs = inputs

    def __str__(self):
        inp0 = f"'{self.inputs[0]}'" if isinstance(self.inputs[0], str) else f"{self.inputs[0]}"
        if self.type == GateType.NOT:
            return f"NOT {inp0}"
        else:
            inp1 = f"'{self.inputs[1]}'" if isinstance(self.inputs[1], str) else f"{self.inputs[1]}"
            return f"({inp0} {self.type.name} {inp1})"

    def __repr__(self):
        pass
    def get_inputs(self):
        """Gets inputs from this gate"""
        result = []
        for inp in self.inputs:
            if isinstance(inp, LogicGate):
                for another_inp in inp.get_inputs():
                    if another_inp not in result:
                        result.append(another_inp)
            elif inp not in result:
                result.append(inp)
        return result

    def calculate_inputs(self, inputs: list[bool]):
        if self.type == GateType.NOT:
            return not inputs[0]
        elif self.type == GateType.AND:
            return inputs[0] and inputs[1]
        elif self.type == GateType.OR:
            return inputs[0] or inputs[1]
        elif self.type == GateType.NAND:
            return not (inputs[0] and inputs[1])
        elif self.type == GateType.NOR:
            return not (inputs[0] or inputs[1])
        elif self.type == GateType.XOR:
            return inputs[0] != inputs[1]
        elif self.type == GateType.XNOR:
            return inputs[0] == inputs[1]
        else:
            return inputs[0]

    def execute(self, inputs: list[bool]) -> int:
        """Executes this gate with the given inputs"""
        if all(isinstance(x, str) for x in self.inputs):
            return self.calculate_inputs(inputs)

        result_inputs = []
        for inp in self.inputs:
            if isinstance(inp, LogicGate):
                _inputs = [inputs[self.get_inputs().index(x)] for x in inp.get_inputs()]
                result_inputs.append(inp.execute(_inputs))
            elif isinstance(inp, str):
                index = self.get_inputs().index(inp)
                result_inputs.append(inputs[index])

        return self.calculate_inputs(result_inputs)


    def truth(self):
        """Creates a truth table with results in array format."""
        inputs = self.get_inputs()
        result = [inputs]
        result[0] = result[0] + ["Output"]

        rows = 2**len(inputs)
        for i in range(rows):
            row = []
            for j in range(len(inputs)):
                row.append(int(i / (2**(len(inputs) - j - 1))))
                i = i % (2**(len(inputs) - j - 1))
            result.append(row)
        for i in range(1, rows + 1):
            result[i] += [int(self.execute(result[i]))]
        return result

    def truth_bin(self):
        """Creates a truth table with results in binary format."""
        print("\n".join(
            ["\t".join([str(x) for x in row]) for row in self.truth()]))
