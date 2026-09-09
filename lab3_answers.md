### Lab 3.1 — Hash properties & toy Proof-of-Work

Q1: Each extra leading zero multiplies expected work by = how much? Why?
Answer: The expected computational work increases by exactly 16 times.
Explanation: The SHA-256 hash function returns a hexadecimal string, which consists of 16 possible characters (0-9 and a-f). The probability of getting a 0 randomly at any specific position is 1/16. Therefore, to find a hash with an additional leading zero, the algorithm will need to try (on average) 16 times more hashes.

Q2: Verifying your found nonce takes how many hash calls? What does this say about PoW?
Answer: Verifying the found nonce always takes exactly 1 hash call.
Explanation: This perfectly demonstrates the most critical property of Proof-of-Work: Finding the solution (mining) is incredibly difficult and computationally expensive, but verifying the solution is trivial, extremely fast, and costs almost nothing for any node in the network.

---

### Lab 3.2 — Merkle tree

Q3: For n=1,000,000 transactions, how many hashes does one proof contain?
Answer: One proof will contain 20 hashes.
Explanation: The number of hashes in a Merkle proof (the path from the leaf to the root) corresponds to the height of the binary tree, calculated using the formula ceil(log2(n)). For n = 1,000,000, we have log2(1,000,000) roughly equal to 19.931. Rounding up gives a tree height of 20.

Q4: Explain one real system that uses exactly this mechanism (SPV, airdrop claim, proof-of-reserves...).
Answer: This exact mechanism is used in SPV (Simplified Payment Verification) for Bitcoin light clients/wallets.
Explanation: Mobile light wallets cannot download the entire Blockchain (hundreds of GBs). Instead, they only download Block Headers (which contain the Merkle Root). When needing to verify if a transaction exists in a block, the light wallet requests a Merkle Proof from a Full Node. By hashing upward using the proof to see if it matches the Merkle Root, the transaction is proven valid without downloading millions of other transactions.

---

### Lab 3.3 - Sign, verify & recover with eth-account

Task 1: Run twice with the same message - is the signature identical? Which RFC explains this?
Answer: Yes, the signature is completely identical across multiple runs.
Explanation: This behavior is explained by RFC 6979 (Deterministic Usage of the Digital Signature Algorithm). Unlike the older ECDSA standard which used a random nonce (k) for each signature, RFC 6979 generates the k value deterministically based on the hash of the private key and the message content. Therefore, the same message and the same private key will always yield a unique, identical signature.

Task 2: Show the TA: the tampered message recovers a different address. Explain why this proves integrity.
Execution Result: The original message successfully recovered the original address.
Explanation: The 'recover_message' function uses the signature and the hash of the current message to mathematically derive the Public Key (and thus, the address). Because hash functions have an "avalanche effect," altering even a single character completely changes the message's hash. When this invalid hash is combined with the original signature, the algorithm outputs a random address that does not match the sender's. Therefore, any data tampering is instantly detected, proving the absolute integrity of the original message.