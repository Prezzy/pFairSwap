pragma solidity >=0.4.22 <0.7.0;

/**
 * @title Judge
 * @dev To experiment with Gas cost of various Proof of misbehaviour
 */
contract Storage {

    uint256 constant depth = 15;
    
    uint256 Mp = 89;
    
    uint256 gateIdx;
    string gateDes;
    bytes32[depth] gateProof;
    bytes32 gateType;
        
    uint256 outIdx;
    bytes32 outEnc;
    bytes32[depth] outProof;    

    uint256 in1Idx;
    bytes32 in1Enc;
    bytes32[depth] in1Proof;
        
    uint256 in2Idx;
    bytes32 in2Enc;
    bytes32[depth] in2Proof;


    
    function dec(uint256 idx, bytes32 key, bytes32 ciphertext) public pure returns (bytes32) {
    
        bytes32 key_i_hash = keccak256(abi.encodePacked(key, idx));
        
        return ciphertext ^ key_i_hash;
        
    }
    
    function modComp(uint256 val1, uint256 val2) public view returns (uint256){
        
        uint256 product = val1 * val2;
        
        uint256 result = (product & (2**Mp)-1) + (product >> Mp);
        
        return result;
    }
    
    function mVrfyGate(uint256 idx, string memory element, bytes32[depth] memory proof, bytes32 root) public pure returns (bool){
        
        bytes32 hash1 = keccak256(abi.encodePacked(element));
        
        for(uint i = 0; i < depth; i++){
            if((idx / uint256(2**i) % 2) == 0){
                hash1 = keccak256(abi.encodePacked(hash1, proof[i]));
            } else {
                hash1 = keccak256(abi.encodePacked(proof[i], hash1));
            }
        }
        
        if(hash1 == root){
            return true;
        } else {
            return false;
        }
    }
    
      function mVrfy(uint256 idx, bytes32 element, bytes32[depth] memory proof, bytes32 root) public pure returns (bool){
        
        bytes32 hash1 = keccak256(abi.encodePacked(element));
        
        for(uint i = 0; i < depth; i++){
            if((idx / uint256(2**i) % 2) == 0){
                hash1 = keccak256(abi.encodePacked(hash1, proof[i]));
            } else {
                hash1 = keccak256(abi.encodePacked(proof[i], hash1));
            }
        }
        
        if(hash1 == root){
            return true;
        } else {
            return false;
        }
    }
    
    function storeGateProof(uint256 idx, string calldata element, bytes32[depth] memory proof) public {
        gateIdx = idx;
        gateDes = element;
        gateProof = proof;
    }
    
    function storeOutProof(uint256 idx, bytes32 element, bytes32[depth] memory proof) public {
        outIdx = idx;
        outEnc = element;
        outProof = proof;
    }
    
    function storeIn1Proof(uint256 idx, bytes32 element, bytes32[depth] memory proof) public {
        in1Idx = idx;
        in1Enc = element;
        in1Proof = proof;
    }
    
    function storeIn2Proof(uint256 idx, bytes32 element, bytes32[depth] memory proof) public {
        in2Idx = idx;
        in2Enc = element;
        in2Proof = proof;
    }
    
    function judge(bytes32 key, bytes32 zRoot, bytes32 phiRoot) public view returns (bool){
        
        if(mVrfyGate(gateIdx, gateDes, gateProof, phiRoot) == false){
            
            return false;
        }
        
        
        if(mVrfy(outIdx, outEnc, outProof, zRoot) == false){
            
            return false;
        }
        
        
        bytes32 outPlain = dec(outIdx, key, outEnc);
        
        if(mVrfy(in1Idx, in1Enc, in1Proof, zRoot) == false){
            
            return false;
        }
        
        if(mVrfy(in2Idx, in2Enc, in2Proof, zRoot) == false){
            
            return false;
        }
       
        
        bytes32 in1Plain = dec(in1Idx, key, in1Enc);
        
        bytes32 in2Plain = dec(in2Idx, key, in2Enc);
        
        uint256 result = modComp(uint256(in1Plain), uint256(in2Plain));
    
        if(result != uint256(outPlain)){
            return false;
        } else {
            return true;   
        }
        
    }
    
    
}
