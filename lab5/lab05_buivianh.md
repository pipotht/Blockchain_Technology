# Lab 05 – Ethereum Accounts, Gas and the EVM

### Q1. Why is the `chainId` included in a signed transaction?

The `chainId` identifies the blockchain network for which a transaction is intended. Under EIP-155, it is included in the transaction signing process to provide replay protection. This prevents a signed transaction created for one network from being valid on another network with a different chain ID, helping protect users from unintentionally repeating transactions across networks.

### Q2. Why does the base fee stay at the floor?

The average `gasUsedRatio` in my 20-block sample is only 2.29%, which is far below the 50% target utilization implied by a 15M target gas usage and a 30M block gas limit. Under EIP-1559, the base fee decreases when block gas usage is below the target and increases when usage is above the target. In my sample, the base fee remained at 8 wei across all 20 blocks. This suggests that the observed base fee was stable at a very low level during the sampled period. However, the sample alone does not prove that 8 wei is the protocol-enforced minimum base fee.

### Q3. Why does `baseFeePerGas` have N+1 elements?

In `eth_feeHistory`, `baseFeePerGas` contains N+1 values for a request covering N blocks. The first N values correspond to the base fees of the requested blocks, while the final value represents the expected base fee for the block immediately after the newest block in the range. A wallet can use this additional value to estimate the next block's base fee and choose a suitable `maxFeePerGas` that covers the expected base fee and the desired priority fee.

### Q4. If you raise `maxFeePerGas` but keep the same `maxPriorityFeePerGas`, does the effective gas price change?

No, not if the original `maxFeePerGas` is already high enough to cover the block's base fee plus the specified priority fee. For an EIP-1559 transaction, the effective gas price is the block base fee plus the priority fee actually paid, subject to the transaction's fee limits. Increasing `maxFeePerGas` further does not increase the effective gas price when the base fee and the priority fee remain unchanged.

### Q5. Why does a simple ETH transfer usually consume 21,000 gas, and why does a failed transaction still cost gas?

A standard ETH transfer to an externally owned account typically requires 21,000 gas because it involves basic transaction processing without additional smart-contract execution. A failed transaction still consumes gas because the network has already performed computation while processing it. Although the transaction's state changes are reverted, the gas used to execute the transaction must still be paid for.

### Q6. What is a function selector, and how does the EVM use it?

A function selector is the first four bytes of a contract call's calldata. It is derived from the Keccak-256 hash of the function's canonical signature, which consists of the function name and parameter types. For example, the selector for `transfer(address,uint256)` is `0xa9059cbb`. When a contract receives a call, its dispatcher uses the selector to determine which function should handle the call, while the remaining calldata encodes the function arguments according to the ABI.
