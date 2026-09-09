# Lab 04 - Real Bitcoin Blocks: PoW, Fees & Merkle Root

## Q1
The target has approximately 19 leading zero hexadecimal digits.
A valid header represents approximately 2^78 hashes of expected work.

## Q2
SHA-256 creates this asymmetry because finding a valid hash requires repeatedly trying different nonces and hashing the block header until the hash is below the target.

However, verifying a solution only requires hashing the given 80-byte header twice and comparing the resulting hash with the target. Therefore, finding the solution is computationally expensive, while verification is very fast.

## Q3
The transaction paid an extremely high fee because block 840,000 was mined on Bitcoin's 2024 halving day, when the Runes protocol launched.
The launch created very high demand for limited block space, so users competed by paying extremely high transaction fees. This shows that Bitcoin transaction fees are determined by supply and demand for block space.

## Q4
The difference comes from transaction fees.
The coinbase transaction receives both the block subsidy and the transaction fees collected from the transactions included in the block.
Therefore:
4,075,061,499 - 312,500,000
= 3,762,561,499 sat

So the difference is 3,762,561,499 satoshis in transaction fees.

## Q5
The computed Merkle root exactly matches the Merkle root stored in the block header. This proves that the transaction list was combined according to Bitcoin's Merkle tree rules and corresponds to the transaction commitment in the header.

This relies on the collision resistance and avalanche effect of double SHA-256. If a transaction were changed, its hash and consequently the Merkle root would also change.