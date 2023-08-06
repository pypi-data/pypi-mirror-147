-----------------------------------------------------------
DISCLAIMER:
-----------------------------------------------------------
Circuit Solver is developed to make sure it's capable of generating
correct simulation results should the user understand that it's a fixed timestep
solver. PhasorSystems is not liable for any incorrect simulation results.

NOTE: This is only tested w/ file version 1.1.9 and above. There is no gurantee
that it will work for older files.

This engine will allow you to run the simulation engine for circuit solver
without a user interface. It will also allow you to edit parameters when
the simulation is running and in turn do dynamic simulations such as battery
models, buck or boost converters, etc.

-----------------------------------------------------------
Tested On:
-----------------------------------------------------------
Python 3.8.5

-----------------------------------------------------------
Setup:
-----------------------------------------------------------
Note: The demo requires numpy and pandas to work correctly.

pip install mnapy

To get the test files nagivate to: 
https://github.com/SummersEdge23/mnapy/tree/main/test

Download "ACSourceInitial_nl.txt" and "TestBed.py"

Change the FILE_LOCATION in TestBed.py to match where ever your "ACSourceInitial_nl.txt" is located. 
Run Testbed.py. If everything goes well a window should open up with a
waveform that should look like an acsource.

-----------------------------------------------------------
Generating New Files:
-----------------------------------------------------------
In order to load new files into the system, go to www.androidcircuitsolver.com/app.html
or use the desktop version (windows only atm). Build your circuit and
in order to port this to the headless version press: CTRL + P.
This will generate a {FILE_NAME}_nl.txt file that can be loaded into this
headless engine.

Note: Set_Switch_State(setter: str) and Set_Interpolate(setter: str)
can be set by:

Set_Switch_State(engine.Params.SystemConstants.ON) or
Set_Switch_State(engine.Params.SystemConstants.OFF)

if (Get_Switch_State() == engine.Params.SystemConstants.ON) or
if (Get_Switch_State() == engine.Params.SystemConstants.OFF)

The same thing applies for Interpolate.

If you have any issues, contact me at PhasorSys@gmail.com
