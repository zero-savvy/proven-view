pragma solidity >=0.7.0 <0.9.0;
import "@openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol";
import "./spartan_verifier.sol";

contract MediaAuthenticator {
    address private owner;
    uint256[] public validRoots;
    uint256[] public verifiedPubkeys;
    mapping(uint256 => uint256) public verifiedOriginals;   // list of original Merkle roots
    mapping(uint256 => uint256) public verifiedEdits;       // list of trimed videos
    SpartanVerifier public verifier;

    struct VideoProof {
        SpartanProof spartproof;  // mock
        uint256[] pubSignals; // assuming pubSignals is an array of uint256 (step_in, step_out)
        uint256 hOrig;   // merkle root
        uint256 hTrim;   // hash pf trimmed video that user wants to verify it's originality
    }
    
    modifier onlyOwner() {
        require(owner == msg.sender);
        _;
    }
        constructor(address spartan_verifier) {
        owner = msg.sender;
        verifier = SpartanVerifier(spartan_verifier);
    }

    function getOwnerOriginal(uint256 value) public view returns (uint256) {
        return verifiedOriginals[value];
    }

    function getOwnerEdit(uint256 value) public view returns (uint256) {
        return verifiedOriginals[verifiedEdits[value]];
    }

    function authenticate(VideoProof memory data, bytes memory sig_alpha, bytes memory sig_owner) public {
        bool proofVerification;
        uint256 h_orig;
        uint256 h_trim;
        uint256 id_trim;
        uint256 id_orig;   // check the usage???
        uint256 id_owner;
        address addr;


            
            // verify zkSNARK proof
        proofVerification = verifier.verify_proof(data[i]);
        require(proofVerification, "Incorrect Proof!");

        h_orig = data.hOrig;
        h_trim = data.hTrim;

        address recovered_signer = ECDSA.recover(h_orig, sig_alpha);

        if (verifiedOriginals[h_orig] == 0) {
            require(verifiedPubkeys[recovered_signer] != 0,
                "UnAuthorizedPubkey: new original must be signed by verified pubkeys only!");
            require(recovered_signer != address(0), "ECDSA: invalid signature");
        }

        if (recovered_signer != msg.sender) {
            bytes32 ownership_msg = keccak256(abi.encodePacked("TRANSFER", h_orig, "TO", msg.sender));
            address recovered_prev_owner = ECDSA.recover(ownership_msg, sig_owner);
            require(recovered_prev_owner == recovered_signer, "Previous owner must sign the original!"); // check if the condition is correct
            require(verifiedOriginals[h_orig] == 0 || verifiedOriginals[id_orig] == recovered_prev_owner, "Previous owner must be valid!");
        }

        id_owner = msg.sender;
        id_orig = h_orig;   // so why??? recovered signer?


        verifiedOriginals[id_orig] = id_owner;
        verifiedEdits[id_tran] = id_orig;
    

        address convertedAddress = address(uint160(data.pubSignals[1]));
        
        // check authenticity of the device address
        if (convertedAddress != msg.sender)
            { revert(); } 

        // check validity of the Merkle root
        if (!checkRoot(data.pubSignals[0])) 
            { revert(); } 
        
        // verify zkSNARK proof
        bool proofVerification;
        proofVerification = verifier.verifyProof(_pA, [_pB1, _pB2], _pC, data.pubSignals);    // verify proof is a function in spartan for verifying proofs.
        if (!proofVerification)
            { revert(); }
    }

    function add_pubkey(uint256 pubkey) external onlyOwner {
        verifiedPubkeys.push(pubkey);
        return; 
    }
}