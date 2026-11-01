--------------------------- MODULE Computador ---------------------------
EXTENDS Naturals
VARIABLES phase, pc, value
vars == <<phase, pc, value>>
Init == /\ phase = "off" /\ pc = 0 /\ value = 0
PowerOn == /\ phase = "off" /\ phase' = "empty" /\ UNCHANGED <<pc,value>>
Load == /\ phase = "empty" /\ phase' = "ready" /\ UNCHANGED <<pc,value>>
Start == /\ phase = "ready" /\ phase' = "running" /\ UNCHANGED <<pc,value>>
Add == /\ phase = "running" /\ pc = 0 /\ pc' = 1 /\ value' = value + 2 /\ UNCHANGED phase
Multiply == /\ phase = "running" /\ pc = 1 /\ pc' = 2 /\ value' = value * 3 /\ UNCHANGED phase
Store == /\ phase = "running" /\ pc = 2 /\ phase' = "done" /\ pc' = 3 /\ UNCHANGED value
PowerOff == /\ phase # "off" /\ phase' = "off" /\ pc' = 0 /\ value' = 0
Reset == /\ phase = "done" /\ phase' = "ready" /\ pc' = 0 /\ value' = 0
Next == PowerOn \/ Load \/ Start \/ Add \/ Multiply \/ Store \/ PowerOff \/ Reset
TypeOK == /\ phase \in {"off","empty","ready","running","done"} /\ pc \in 0..3 /\ value \in {0,2,6}
VolatileReset == phase \in {"off","empty","ready"} => (pc = 0 /\ value = 0)
ResultOK == phase = "done" => (pc = 3 /\ value = 6)
ExecutionOK == phase = "running" => ((pc = 0 /\ value = 0) \/ (pc = 1 /\ value = 2) \/ (pc = 2 /\ value = 6))
=============================================================================
