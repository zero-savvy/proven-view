pragma solidity ^0.8.0;

contract SpartanVerifier {
    address public owner;

    constructor(address _owner) {
        owner = _owner;
    }

    function verifyProof_order(uint256 [100] proof, uint256 horig, uint256 hfirst, uint256 hlast) public view returns (bool) {
        return true;
    }

    function verifyProof_path(uint256 [100] proof, uint256 horig, uint256 hfirst, uint256 hlast) public view returns (bool) {
        return true;
    }
}
