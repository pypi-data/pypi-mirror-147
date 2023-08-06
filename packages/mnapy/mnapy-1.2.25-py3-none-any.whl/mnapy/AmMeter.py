from typing import List

from mnapy import AmMeterLimits
from mnapy import Utils
from mnapy import Wire


class AmMeter:
    def __init__(
            self,
            context,
            Test_Voltage,
            options,
            tag,
            units,
            Current,
            options_units,
            option_limits,
    ):
        self.Test_Voltage = Test_Voltage
        self.options = options
        self.tag = tag
        self.units = units
        self.Current = Current
        self.options_units = options_units
        self.option_limits = AmMeterLimits.AmMeterLimits(
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
        self.Current = 0

    def update(self) -> None:
        None

    def stamp(self) -> None:
        None
        self.context.stamp_voltage(
            self.Nodes[0],
            self.Nodes[1],
            self.Test_Voltage,
            self.context.ELEMENT_AMMETER_OFFSET + self.SimulationId,
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

    def GetSimulationId(self) -> int:
        None
        return self.SimulationId

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

    def push_current(self, current: float) -> None:
        None
        if (
                self.context.Params.SystemFlags.FlagSimulating
                and self.context.simulation_time >= self.context.time_step
                and self.context.solutions_ready
        ):
            self.Current = current

    def get_simulation_index(self) -> int:
        None
        return (
                self.context.node_size
                + self.context.ELEMENT_AMMETER_OFFSET
                + self.SimulationId
        )

    def Get_Current(self) -> float:
        None
        return self.Current

    def GetElementType(self) -> int:
        None
        return self.ElementType

    def SetElementType(self, setter: int) -> None:
        None
        self.ElementType = setter
