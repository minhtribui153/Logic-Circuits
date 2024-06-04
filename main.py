from logic_circuits import GateType, LogicGate

gate = LogicGate(GateType.AND, ["A", LogicGate(GateType.OR, ["B", "C"])])
print(gate)
gate.truth_bin()
