from typing import List

from mnapy import SampleAndHoldLimits
from mnapy import Utils
from mnapy import Wire


class SampleAndHold:
    def __init__(
            self,
            context,
            Input_Voltage2,
            options,
            Input_Voltage1,
            tag,
            units,
            High_Voltage,
            Output_Voltage,
            options_units,
            Low_Voltage,
            option_limits,
    ):
        self.Input_Voltage2 = Input_Voltage2
        self.options = options
        self.Input_Voltage1 = Input_Voltage1
        self.tag = tag
        self.units = units
        self.High_Voltage = High_Voltage
        self.Output_Voltage = Output_Voltage
        self.options_units = options_units
        self.Low_Voltage = Low_Voltage
        self.option_limits = SampleAndHoldLimits.SampleAndHoldLimits(
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

    def reset(self) -> None:
        None
        self.Output_Voltage = 0

    def update(self) -> None:
        None
        if (
                self.context.Params.SystemFlags.FlagSimulating
                and self.context.solutions_ready
                and self.context.simulation_step != 0
        ):
            self.Input_Voltage2 = Utils.Utils.limit(
                self.context.get_voltage(self.Nodes[1], -1),
                self.Low_Voltage,
                self.High_Voltage,
            )
            if self.Input_Voltage2 >= (self.High_Voltage + self.Low_Voltage) / 2:
                self.Input_Voltage1 = self.context.get_voltage(self.Nodes[0], -1)

            self.Output_Voltage = self.Input_Voltage1
        else:
            self.Output_Voltage = 0

    def stamp(self) -> None:
        None
        self.context.stamp_voltage(
            self.Nodes[2],
            -1,
            self.Output_Voltage,
            self.context.ELEMENT_SAH_OFFSET + self.SimulationId,
        )

    def SetId(self, Id: str) -> None:
        None
        self.Id = int(Id)

    def SetNodes(self, Nodes: List[int]) -> None:
        None
        self.Nodes = Nodes

    def SetLinkages(self, Linkages: List[int]) -> None:
        None
        self.Linkages = Linkages

    def SetDesignator(self, Designator: str) -> None:
        None
        self.Designator = Designator

    def GetDesignator(self) -> str:
        None
        return self.Designator

    def SetSimulationId(self, Id: int) -> None:
        None
        self.SimulationId = Id

    def SetWireReferences(self, wires: List[Wire.Wire]) -> None:
        None
        self.WireReferences.clear()
        for i in range(0, len(wires)):
            self.WireReferences.append(wires[i])

    def GetNode(self, i: int) -> int:
        None
        if i < len(self.Nodes):
            return self.Nodes[i]
        else:
            return -1

    def GetElementType(self) -> int:
        None
        return self.ElementType

    def SetElementType(self, setter: int) -> None:
        None
        self.ElementType = setter
