import time
import os

loopCount = 5

def originalCircuit():
    os.system("python ../../msr-vc/pinocchio/ccompiler/src/aritheval.py --wires wires/wires-107 circuits/uniHash-107.arith inputs/inputs-107 outputs/outputs-107")

def expandedCircuit():
    os.system("python ../../msr-vc/pinocchio/ccompiler/src/aritheval.py --wires wires/expanded-wires-107 circuits/expanded-uniHash-107.arith inputs/encoded-inputs-107 outputs/encoded-outputs-107")

timingFile = open("timing-107-new", "w")

ogTimeSum = 0
for i in range(loopCount):
    start_time = time.time()
    originalCircuit()
    ogTimeSum += time.time() - start_time


timingFile.write("original circuit time averaged {} times {}\n".format(loopCount, ogTimeSum/loopCount))
print("original circuit time averaged {} times {}\n".format(loopCount, ogTimeSum/loopCount))
exTimeSum = 0
for i in range(loopCount):
    start_time = time.time()
    expandedCircuit()
    exTimeSum += time.time() - start_time

timingFile.write("expanded circuit time averaged {} times {}".format(loopCount, exTimeSum/loopCount))
print("expanded circuit time averaged {} times {}".format(loopCount, exTimeSum/loopCount))

