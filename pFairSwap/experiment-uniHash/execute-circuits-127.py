import time
import os

loopCount = 5

def originalCircuit():
    os.system("python ../../msr-vc/pinocchio/ccompiler/src/aritheval.py --wires wires/wires-127 circuits/uniHash-127.arith inputs/inputs-127 outputs/outputs-127")

def expandedCircuit():
    os.system("python ../../msr-vc/pinocchio/ccompiler/src/aritheval.py --wires wires/expanded-wires-127 circuits/expanded-uniHash-127.arith inputs/encoded-inputs-127 outputs/encoded-outputs-127")

timingFile = open("timing-127-new", "w")

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

