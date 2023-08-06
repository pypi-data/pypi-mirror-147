import math
from typing import List

from mnapy import ANDGateLimits
from mnapy import Utils
from mnapy import Wire


class ANDGate:
    def __init__(
        self,
        context,
        options,
        tag,
        units,
        High_Voltage,
        V_1,
        V_1_prime,
        V_in1,
        V_partial1,
        V_2,
        V_2_prime,
        V_in2,
        V_partial2,
        V_out,
        V_eq,
        options_units,
        option_limits,
    ):
        self.options = options
        self.tag = tag
        self.units = units
        self.High_Voltage = High_Voltage
        self.V_1 = V_1
        self.V_1_prime = V_1_prime
        self.V_in1 = V_in1
        self.V_partial1 = V_partial1
        self.V_2 = V_2
        self.V_2_prime = V_2_prime
        self.V_in2 = V_in2
        self.V_partial2 = V_partial2
        self.V_out = V_out
        self.V_eq = V_eq
        self.options_units = options_units
        self.option_limits = ANDGateLimits.ANDGateLimits(
            **Utils.Utils.FixDictionary(option_limits)
        )
        self.Nodes = []
        self.Linkages = []
        self.Designator = ""
        self.Id = -1
        self.SimulationId = -1
        self.ElementType = -1
        self.WireReferences = []
        self.context = context

    def Set_High_Voltage(self, setter: float) -> None:
        if (
            abs(setter) >= abs(self.option_limits.High_Voltage[0])
            and abs(setter) <= abs(self.option_limits.High_Voltage[1])
        ) or abs(setter) == 0:
            self.High_Voltage = setter
        else:
            print(self.Designator + ":=" + setter + " -> Value is outside of limits.")

    def Get_High_Voltage(self) -> float:
        return self.High_Voltage

    def reset(self) -> None:
        self.Output_Voltage = 0

    def vout_and(self, ui: List[float]) -> float:
        sum = 0
        N = 2
        size = len(ui)

        for i in range(0, len(ui)):
            sum += size / (1 + ui[i] + self.context.Params.SystemConstants.ZERO_BIAS)

        return N / sum + self.context.Params.SystemConstants.ZERO_BIAS

    def partial_and(
        self, terminal: float, ui: List[float], ui_prime: List[float]
    ) -> float:
        sum = 0
        N = 2
        size = len(ui)

        for i in range(0, len(ui)):
            sum += size / (1 + ui[i] + self.context.Params.SystemConstants.ZERO_BIAS)

        return (2 * N * ui_prime[terminal]) / math.pow(
            (1 + ui[terminal] + self.context.Params.SystemConstants.ZERO_BIAS) * sum, 2
        )

    def update(self):
        if (
            self.context.Params.SystemFlags.FlagSimulating
            and self.context.solutions_ready
        ):
            self.V_in1 = self.context.get_voltage(self.Nodes[0], -1)
            self.V_1 = math.tanh(10 * (self.V_in1 / self.High_Voltage - 0.5))
            self.V_1_prime = 10 * (1.0 - self.V_1 * self.V_1)
            self.V_in2 = self.context.get_voltage(self.Nodes[1], -1)
            self.V_2 = math.tanh(10 * (self.V_in2 / self.High_Voltage - 0.5))
            self.V_2_prime = 10 * (1.0 - self.V_2 * self.V_2)
            self.V_out = self.vout_and([self.V_1, self.V_2])
            self.V_partial1 = Utils.Utils.limit(
                self.partial_and(
                    0, [self.V_1, self.V_2], [self.V_1_prime, self.V_2_prime]
                ),
                0.0,
                1.0,
            )
            self.V_partial2 = Utils.Utils.limit(
                self.partial_and(
                    1, [self.V_1, self.V_2], [self.V_1_prime, self.V_2_prime]
                ),
                0.0,
                1.0,
            )
            self.V_eq = self.High_Voltage * (
                self.V_partial1 * (self.V_in1 / self.High_Voltage)
                + self.V_partial2 * (self.V_in2 / self.High_Voltage)
                - self.V_out
            )

    def stamp(self):
        self.context.stamp_gate2(
            self.Nodes[2],
            self.V_partial1,
            self.V_partial2,
            self.V_eq,
            self.context.ELEMENT_AND_OFFSET + self.SimulationId,
        )

    def SetId(self, Id: str) -> None:
        self.Id = int(Id)

    def SetNodes(self, Nodes: List[int]) -> None:
        self.Nodes = Nodes

    def SetLinkages(self, Linkages: List[int]) -> None:
        self.Linkages = Linkages

    def SetDesignator(self, Designator: str) -> None:
        self.Designator = Designator

    def GetDesignator(self) -> str:
        return self.Designator

    def SetSimulationId(self, Id: int) -> None:
        self.SimulationId = Id

    def SetWireReferences(self, wires: List[Wire.Wire]) -> None:
        self.WireReferences.clear()
        for i in range(0, len(wires)):
            self.WireReferences.append(wires[i])

    def GetNode(self, i: int) -> int:
        if i < len(self.Nodes):
            return self.Nodes[i]
        else:
            return -1

    def GetElementType(self) -> int:
        return self.ElementType

    def SetElementType(self, setter: int) -> None:
        self.ElementType = setter
