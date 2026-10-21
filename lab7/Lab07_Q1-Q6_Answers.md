# Lab 07 — Token Standards on Hardhat + TrustKeys
## Written Answers (Q1–Q6)

### Q1. Why do we build on OpenZeppelin instead of writing ERC-20 from scratch?

We use OpenZeppelin because it provides reusable, widely reviewed implementations of common smart-contract standards, including ERC-20. This reduces the chance of introducing bugs in important features such as balances, transfers, allowances, and event emission. It also makes the contract easier to maintain and more consistent with the ERC-20 standard. We still need to implement and test our own requirements, such as the token cap and initial supply. Using OpenZeppelin reduces risk, but it does not automatically guarantee that our complete contract is secure.

### Q2. 'decimals()' returns 18. If Alice's balance is '1900000000000000000', how many CTK is that, and where does the “18” actually live — on-chain or in the UI?

With 18 decimals, one CTK is represented internally as '10^18' base units. Therefore,

'1900000000000000000 / 10^18 = 1.9 CTK'.

The value '18' is returned by the token contract's on-chain 'decimals()' function. Wallets and other user interfaces commonly read this value to display the integer balance in human-readable token units. The balance itself is stored in base units; the UI formats it using the decimals value.

### Q3. Why does a DEX need 'approve' + 'transferFrom' instead of a plain 'transfer'? What is the risk of 'approve(spender, 2**-1)'?

A DEX or another contract cannot move a user's ERC-20 tokens merely by calling 'transfer' from its own address. The token owner can first call 'approve(spender, amount)' to authorize a spender for a specified amount. The spender can then call 'transferFrom(owner, recipient, amount)' to transfer tokens within the allowance. This separates the owner's authorization from the later action performed by the spender.

An unlimited approval is risky because the approved spender may be able to transfer up to the entire token balance covered by that allowance, including tokens received later, until the allowance is used, changed, or revoked. If the spender contract is malicious or compromised, the user could lose tokens. Users should approve only trusted spenders and preferably limit approvals to the amount needed.

### Q4. Where do the JSON and the image live? What did we avoid by NOT using IPFS on TrustKeys?

In this lab, the NFT's metadata JSON is encoded in Base64 and returned as a 'data:application/json;base64,...' URI by the contract's 'tokenURI()' function. The image field inside that JSON is itself a Base64-encoded SVG data URI. The JSON and SVG content are therefore embedded in the returned data URI and generated from data held/constructed by the on-chain contract, rather than being fetched from an IPFS URL.

This approach avoids having to upload the metadata and image to IPFS or depend on an external IPFS gateway to retrieve them for this lab. It also makes the metadata available directly through 'tokenURI()'. However, the encoded content and the logic that constructs it still cost gas when stored or executed on-chain, and Base64 is an encoding format, not encryption.

### Q5. What does the “safe” in '_safeMint' / 'safeTransferFrom' actually check, and why?

For ERC-721, '_safeMint' and 'safeTransferFrom' check whether the recipient is a smart contract and, if so, whether it correctly implements the 'IERC721Receiver' interface by returning the expected receiver selector from 'onERC721Received'. If the contract recipient does not implement the callback correctly or rejects the token, the operation reverts. This helps prevent NFTs from being sent to smart contracts that cannot receive or manage ERC-721 tokens, where the NFTs could otherwise become stuck. For an externally owned account (EOA), there is no contract receiver callback to check.

### Q6. TrustKeys has no public explorer. How did you confirm the 100-CTK transfer landed?

Because TrustKeys has no public block explorer, the transfer should be verified directly through the transaction receipt and on-chain contract state. After sending 100 CTK, obtain the transaction response/hash and wait for its receipt. Check that the receipt has a successful status, then query the token contract's 'balanceOf(sender)' and 'balanceOf(recipient)' values. The recipient's balance should increase by 100 CTK and the sender's balance should decrease by 100 CTK, assuming no other transfers occurred. The ERC-20 'Transfer' event can provide additional confirmation.

For a report, include the transaction hash, successful receipt/status, and before/after balances or the relevant 'Transfer' event. Do not claim that these checks were performed unless you actually ran them.