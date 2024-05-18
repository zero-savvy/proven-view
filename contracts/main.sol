pragma solidity >=0.7.0 <0.9.0;
import "@openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol";
import "./spartan_verifier.sol";

contract MediaAuthenticator {
    address private owner;
    uint256[] public validRoots;
    uint256[] public verifiedPubkeys;
    mapping(uint256 => uint256) public verifiedOriginals;   // list of original Merkle roots
    mapping(uint256 => uint256) public verifiedEdits;       // list of trimed videos/ assigned to original hashes
    SpartanVerifier public verifier;

    struct VideoProof {
        SpartanProof order_proof;  // mock
        SpartanProof path_proof;  // mock
        uint256 hOrig;   // merkle root
        uint256 hFirst;   // hash pf trimmed video that user wants to verify it's originality --> hash(first, last) trimmed
        uint256 hLast;
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

    function authenticate(VideoProof memory data, bytes memory sig_alpha) public {
        bool proofVerification;
        uint256 h_orig;
        uint256 h_trim;
        uint256 id_trim;
        uint256 id_orig;   // check the usage???
        uint256 id_owner;
        address addr;


            
        // verify zkSNARK proof
        proofVerification_order = verifier.verifyProof_order(data.order_proof, data.hOrig, data.hFirst, data.hLast);
        require(proofVerification_order, "Incorrect Order Proof!");

        // verify zkSNARK proof
        proofVerification_path = verifier.verifyProof_path(data.path_proof, data.hOrig, data.hFirst, data.hLast);
        require(proofVerification_path, "Incorrect Path Proof!");

        h_orig = data.hOrig;
        h_trim_first = data.hFirst;
        h_trim_last = data.hLast;


        address recovered_signer = ECDSA.recover(h_orig, sig_alpha);

        if (verifiedOriginals[h_orig] == 0) {
            require(verifiedPubkeys[recovered_signer] != 0,
                "UnAuthorizedPubkey: new original must be signed by verified pubkeys only!");
        }

        verifiedOriginals[h_orig] = msg.sender;

        h_trim = keccak256(abi.encodePacked(h_trim_first, h_trim_last));
        verifiedEdits[h_trim] = h_orig;

        return;
    }

    function add_pubkey(uint256 pubkey) external onlyOwner {
        verifiedPubkeys.push(pubkey);
        return; 
    }

}