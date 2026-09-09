# ============================================================
# LAB 3.1 - Hash properties & toy Proof-of-Work
# ============================================================
import hashlib
import time

print("=" * 60)
print("LAB 3.1 - HASH PROPERTIES & TOY PROOF-OF-WORK")
print("=" * 60)

print("\n[Avalanche effect]")

message1 = b"Blockchain 2026"
message2 = b"blockchain 2026"
hash1 = hashlib.sha256(message1).hexdigest()
hash2 = hashlib.sha256(message2).hexdigest()

print("Message 1 :", message1.decode())
print("SHA-256   :", hash1)
print("\nMessage 2 :", message2.decode())
print("SHA-256   :", hash2)
print("\nChanging only one character/case produces a completely")
print("different SHA-256 hash. This demonstrates the avalanche effect.")
print("\n[Toy Proof-of-Work]")

def mine(data: bytes, k: int) -> tuple[int, float]:
    target = "0" * k
    nonce = 0
    t0 = time.time()

    while True:
        h = hashlib.sha256(
            data + str(nonce).encode()
        ).hexdigest()

        if h.startswith(target):
            return nonce, time.time() - t0

        nonce += 1

for k in range(1, 7):
    nonce, dt = mine(
        b"block#1|txroot=abc|",
        k)
    print(f"k={k} | nonce={nonce:>9} | time={dt:.6f}s")

print("\nObservation:")
print("Each additional leading zero multiplies the expected")
print("computational work by approximately 16 times because")
print("SHA-256 output is hexadecimal and each character has")
print("16 possible values.")

# ============================================================
# LAB 3.2 - MERKLE TREE
# ============================================================
print("\n" + "=" * 60)
print("LAB 3.2 - MERKLE TREE")
print("=" * 60)

def H(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()
# TODO 1 - Merkle Root
def merkle_root(leaves: list[bytes]) -> bytes:
    if not leaves:
        return b""

    curr = leaves[:]

    while len(curr) > 1:
        if len(curr) % 2 != 0:
            curr.append(curr[-1])
        curr = [
            H(curr[i] + curr[i + 1])
            for i in range(0, len(curr), 2)]
    return curr[0]
# TODO 2 - Merkle Proof
def merkle_proof(
    leaves: list[bytes],
    index: int
) -> list[tuple[bytes, bool]]:
    if not leaves:
        return []

    if index < 0 or index >= len(leaves):
        raise IndexError("Leaf index out of range")

    proof = []

    curr = leaves[:]
    curr_idx = index

    while len(curr) > 1:
        if len(curr) % 2 != 0:
            curr.append(curr[-1])
        is_left = (curr_idx % 2 != 0)

        if is_left:
            sibling_idx = curr_idx - 1
        else:
            sibling_idx = curr_idx + 1

        proof.append(
            (curr[sibling_idx], is_left))
        curr = [
            H(curr[i] + curr[i + 1])
            for i in range(0, len(curr), 2)]

        curr_idx //= 2

    return proof
# TODO 3 - Verify Merkle Proof
def verify_proof(
    leaf_hash: bytes,
    proof: list[tuple[bytes, bool]],
    root: bytes) -> bool:
    curr_hash = leaf_hash

    for sibling_hash, is_left in proof:

        if is_left:
            curr_hash = H(
                sibling_hash + curr_hash)
        else:
            curr_hash = H(
                curr_hash + sibling_hash)

    return curr_hash == root
print("\n[Testing Merkle Tree]")
leaves = [
    b"tx1",
    b"tx2",
    b"tx3",
    b"tx4"]
leaf_hashes = [
    H(leaf)
    for leaf in leaves]
root = merkle_root(leaf_hashes)
print("Merkle root:")
print(root.hex())
index = 2
proof = merkle_proof(
    leaf_hashes,
    index)
print("\nMerkle proof for tx3:")
for i, (sibling_hash, is_left) in enumerate(proof):
    side = "left" if is_left else "right"

    print(
        f"Level {i + 1}: "
        f"sibling={sibling_hash.hex()} "
        f"side={side}")
valid_result = verify_proof(
    leaf_hashes[index],
    proof,
    root)
print("\nCHECK merkle_root:", "OK" if root else "FAIL")
print(
    "CHECK merkle_proof:",
    "OK" if len(proof) > 0 else "FAIL")
print(
    "CHECK verify_proof valid:",
    "OK" if valid_result else "FAIL")
tampered_leaf = H(b"tx3_modified")

tampered_result = verify_proof(
    tampered_leaf,
    proof,
    root)
print(
    "CHECK verify_proof tampered:",
    "OK" if not tampered_result else "FAIL")
odd_leaves = [
    H(b"tx1"),
    H(b"tx2"),
    H(b"tx3")]
odd_root = merkle_root(odd_leaves)
odd_proof = merkle_proof(
    odd_leaves, 2)
odd_result = verify_proof(
    odd_leaves[2],
    odd_proof,
    odd_root)
print(
    "CHECK odd-number Merkle tree:",
    "OK" if odd_result else "FAIL")
# ============================================================
# LAB 3.3 - SIGN, VERIFY & RECOVER WITH ETH-ACCOUNT
# ============================================================
print("\n" + "=" * 60)
print("LAB 3.3 - SIGN, VERIFY & RECOVER WITH ETH-ACCOUNT")
print("=" * 60)
from eth_account import Account
from eth_account.messages import encode_defunct
acct = Account.create()
print("\n[Account]")
print("Address:", acct.address)
message_text = "I attended Session 3 / Toi da hoc Buoi 3"
msg = encode_defunct(
    text=message_text)
sig = Account.sign_message(
    msg,
    acct.key)
print("\n[Signature]")
print("Message:", message_text)

print("r,s,v:")
print("r =", hex(sig.r))
print("s =", hex(sig.s))
print("v =", sig.v)

print("Signature:")
print(sig.signature.hex())
print("\n[Deterministic Signature Test]")
sig1 = Account.sign_message(
    msg,
    acct.key)

sig2 = Account.sign_message(
    msg,
    acct.key)
same_signature = (
    sig1.signature == sig2.signature)

print("Signature run 1:")
print(sig1.signature.hex())
print("\nSignature run 2:")
print(sig2.signature.hex())

print(
    "\nCHECK same message + same private key:",
    "OK" if same_signature else "FAIL")
who = Account.recover_message(
    msg,
    signature=sig.signature)
print("\n[Recover Address]")
print("Original address :", acct.address)
print("Recovered address:", who)
print(
    "CHECK recovered address:",
    "OK" if who == acct.address else "FAIL")
print("\n[Tampered Message]")
bad_text = "I attended Session 3 / Toi da hoc Buoi 4"
bad_msg = encode_defunct(
    text=bad_text)
bad_recovered = Account.recover_message(
    bad_msg,
    signature=sig.signature)


print("Original message:")
print(message_text)

print("\nTampered message:")
print(bad_text)

print("\nOriginal address:")
print(acct.address)

print("\nRecovered address from tampered message:")
print(bad_recovered)

print(
    "\nCHECK tampered message gives different address:",
    "OK" if bad_recovered != acct.address else "FAIL")
print("\n" + "=" * 60)
print("FINAL CHECK")
print("=" * 60)
all_checks = [
    bool(root),
    len(proof) > 0,
    valid_result,
    not tampered_result,
    odd_result,
    same_signature,
    who == acct.address,
    bad_recovered != acct.address]
if all(all_checks):
    print("ALL CHECKS PASSED - OK")
else:
    print("SOME CHECKS FAILED - PLEASE REVIEW THE CODE")