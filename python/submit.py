from eth_account import Account
import web3
from eth_keys import keys
from eth_account.messages import encode_defunct

w3 = web3.Web3(web3.Web3.HTTPProvider("https://sepolia.infura.io/v3/0776cf37dfb04efdacd478388c7c1dec"))

privkey = '389707fa396b315576e8258b1f6f88e067f383f45a410b71971f49b1a34ca108'

abi = '[{"inputs":[{"internalType":"address","name":"spartan_verifier","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"ECDSAInvalidSignature","type":"error"},{"inputs":[{"internalType":"uint256","name":"length","type":"uint256"}],"name":"ECDSAInvalidSignatureLength","type":"error"},{"inputs":[{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"ECDSAInvalidSignatureS","type":"error"},{"inputs":[{"internalType":"uint256","name":"pubkey","type":"uint256"}],"name":"add_pubkey","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"components":[{"internalType":"uint256[]","name":"proof","type":"uint256[]"}],"internalType":"struct SpartanProof","name":"integrity_proof","type":"tuple"},{"components":[{"internalType":"uint256[]","name":"proof","type":"uint256[]"}],"internalType":"struct SpartanProof","name":"authenticity_proof","type":"tuple"},{"internalType":"uint256","name":"hOrig","type":"uint256"},{"internalType":"uint256","name":"hFirst","type":"uint256"},{"internalType":"uint256","name":"hLast","type":"uint256"}],"internalType":"struct MediaAuthenticator.VideoProof","name":"data","type":"tuple"},{"internalType":"bytes","name":"sig_alpha","type":"bytes"}],"name":"authenticate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"value","type":"uint256"}],"name":"getOwnerEdit","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"value","type":"uint256"}],"name":"getOwnerOriginal","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"validRoots","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"verifiedEdits","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"verifiedOriginals","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"verifiedPubkeys","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"verifier","outputs":[{"internalType":"contract SpartanVerifier","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'
deployed_addr = '0xe52cF7389CD3D536906395F033027479Bf7dC08C'
acc = Account.from_key(privkey)
# print(int(str(acc.address),0))

data = 0x21d6c02c94e0df6306c27e558a0ef4620c0a50d2b73fa8d4c5089ddb5ee28330
msghash = encode_defunct(data)
signed_message = Account.sign_message(msghash, '0x'+privkey)
print(signed_message.signature)
print("FFFFFFFFFFFF", Account.recover_message(msghash, signature=signed_message.signature))

# print([ hex( i) for i in bytes.fromhex("2177a57118c2bdeb90427ba79158693cecdee511cca1d0d6a023ec65604e446357e3199daa43bef08f25cae129f18a5c41ba9b85b7a687f633e5657c7337047e1c")])
# exit()
attestor = w3.eth.contract(address=deployed_addr, abi=abi)
chainId = w3.eth.chain_id

data = {
    "integrity_proof": {
        "proof": [0x21d6c02c94e0df6306c00e558a0ef4620c0a50d2b73fa8d4c5089ddb5ee28330]  # Sample values for the proof array
    },
    "authenticity_proof": {
        "proof": [0x21d6c02c94e0df6306c270058a0ef4620c0a50d2b73fa8d4c5089ddb5ee28330]  # Sample values for the proof array
    },
    "hOrig": 0x21d6c02c94e0df6306c27e558a0ef4620c0a50d2b73fa8d4c5089ddb5ee28330,   # Sample value for hOrig
    "hFirst": 0x82a3f0373ae5f240c9ad5041e6e482ca90d0146a76ba0c64ceb6a071486737d,  # Sample value for hFirst
    "hLast": 0x25f9164c204f893295a620e7f94cccfcb66ea672047d0c0d2c44eabe73a6b2e5    # Sample value for hLast
}

tx = attestor.functions.authenticate(data, signed_message.signature).build_transaction(
    {
        'nonce': w3.eth.get_transaction_count(acc.address),
        'gasPrice': w3.eth.gas_price,
        'gas': 1_000_000,
        'from': acc.address,
        'value': 0,
        'chainId': chainId
    }
)
print(tx)
signed_tx = Account.sign_transaction(tx, privkey)
# print(signed_tx)

tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
print(tx_hash.hex())

# [
#     [
#         [0x21d6c02c94e0df6306c00e558a0ef4620c0a50d2b73fa8d4c5089ddb5ee28330]
#     ],
#     [
#         [0x21d6c02c94e0df6306c270058a0ef4620c0a50d2b73fa8d4c5089ddb5ee28330]
#     ],
#     0x21d6c02c94e0df6306c27e558a0ef4620c0a50d2b73fa8d4c5089ddb5ee28330,
#     0x82a3f0373ae5f240c9ad5041e6e482ca90d0146a76ba0c64ceb6a071486737d,
#     0x25f9164c204f893295a620e7f94cccfcb66ea672047d0c0d2c44eabe73a6b2e5

# ]

# bytes.fromhex