# Private-FariSwap
Experimental Implementation of Private FairSwap

This directory contains the python programs we implemented as part of our experiments to measure the overhead caused 
by our private FiarSwap. Some of these file are designed to be used with the Pinocchio Compiler for Verifiable Computing. This repository is used to generate and execute arithmetic circuits and can be found: https://github.com/corda/msr-vc/tree/master/pinocchio.

This implementation is a proof of concept implementation that implements only the parts of the protocol relevant to the measurments taken and presented in the paper.

experiment-uniHash directory:
- Circuits Directory
--- Contains arithmetic circuit description files.
****************************************************************

- inputs Directory
--- contains files describing the inputs to each circuit.
*****************************************************************

- outputs Directory
--- contains files describing the outputs of each circuit computed on the corresdponding inputs.
*****************************************************************

- protocol Directory
--- contains all the methods we used to execute our protocol.
*****************************************************************

- timing info Directory
--- directory to write timing information for the execution and encoding of circuits
*****************************************************************

- uniHash-source Directory
--- C source code Pinocchio compiles into arithmetic circuit descriptions
*****************************************************************

- wires Directory
--- contains all the files that describe the wire values for each circuit execution executed on corresponding inputs.
*****************************************************************

- encode-inputs-uniHash.py:
--- This python script reads "input" files for the circuit and encodes the input so it can be run with expanded circuits
*****************************************************************

- encode-wires.py:
--- This python script reads "wire" files. These are files created by the Pinocchio compiler and that contain an index of the wire and the value that the wire carries. The encoding process encrypts each wire.
******************************************************************

- execute-circuits-X.py: (X = 89,107,127)
--- executes the original and expanded circuit with for feild size 89 with their respective input files. Note this python script executes aritheval.py from the Pinocchio suit and must be executed useing python version 2.7.13. The wire values of the circuit are written to wire files in the wires directory. The output of the circuits are written to output files in the outputs directory. The execution 	of each circuit is times and timing information is written to the timing info directory. ***NOTE: For each circuit to execute properly we must edit two files in the Pinocchio suit. These files are located in msr-vc/pinocchio/ccompiler/src and are named artiheval.py (line 17 needs to be edited) and BaseEval.py (lines 37 need to be edited).
********************************************************************
aritheval.py:
 def eval_internal(self, ae):
 
 16                 input = ae.lookup(self.wire_id)
 
 17                 ####################################
 
 18                 #Uncomment out the below line and then comment
 
 19                 #out the last return statment to adjust the feild
 
 20                 #Pinocchio used to compute circuits. replace '89'
 
 21                 #with the feild size you would like to use.
 
 22                 ####################################
 23 
 24                 #return(pow(input*self.const,1,(2**89)-1))
 
 25                 return input*self.const


BaseEval.py:
def eval_internal(self, ae):

 36                 input_args = map(ae.lookup, self.wire_list)
 
 37                 ############################
 
 38                 #Uncommet the lines below to execute Pinocchio
 
 39                 #in different feild sizes, replace 89 with
 
 40                 #desired feild size and replave self.pyop
 
 41                 #in return command with modOp
 
 42                 ############################
 
 43                 #def modOp(a,b):
 
 44                         #result = self.pyop(a,b)
 
 45                         #return(pow(result,1,(2**89)-1)
 
 46                 return reduce(self.pyop, input_args)


**********

- generate-pom.py: 
--- This script uses the web3 python package and needs to be executed using python version 3.8.5. This python script takes reads wire files and generates a "dummy" Proof of Misbehaviour (PoM). It writes all the necessary elements of the PoM to a file called PoM. Once we have this file we copy and pasted the elements into the appropriate inputs to our smart contract run and executed on the IDE Remix. In later works we created python scripts that directly send the PoM to a smart contract running locally. But for this paper we manually copy and pasted each element and took the gas measurments from the browser-based IDE. The circuit it generated the PoM for is hardcoded and needs to be changed manually.
*********************************************************************

- transform-uniHash.py:
--- This python script takes the circuit description text files generated by Pinocchio and expands them, producing new text files contain arithmetic circuit descriptions of the expanded circuits.
**********************************************************************

- uniHash.py:
---This is a utility python script that we used to automatically generate the C source code the hash function that Pinocchio compiles into a circuit description. 
***********************************************************************

The Judge.sol file is an Ethereum smart contract that evaluates a Proof of Misbehaviour. We executes this smart contract on the browser based IDE remix. As our implementation was a prototype proof of concept we generated the inputs using the generate-pom.py script and copy and pasted each input into the remix input feilds.

