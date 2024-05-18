pragma solidity ^0.8.0;

contract SpartanVerifier {
    address public owner;

    constructor(address _owner) {
        owner = _owner;
    }

    struct SpartanProof {
        uint256[] proof;
    }

    function verifyProof_integrity(SpartanProof proof, uint256 horig, uint256 hfirst, uint256 hlast) public view returns (bool) {
        return true;
    }

    function verifyProof_authenticity(SpartanProof proof, uint256 horig, uint256 hfirst, uint256 hlast) public view returns (bool) {
        return true;
    }
}
