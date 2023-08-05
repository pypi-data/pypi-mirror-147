from starkware.crypto.signature.signature import pedersen_hash, sign


def str_to_felt(text):
    b_text = bytes(text, "utf-8")
    return int.from_bytes(b_text, "big")


def sign_entry(entry, private_key):
    entry_hash = hash_entry(entry)
    signature_r, signature_s = sign(entry_hash, private_key)
    return signature_r, signature_s


def hash_entry(entry):
    h1 = pedersen_hash(entry.asset, entry.publisher)
    h2 = pedersen_hash(entry.price, h1)
    h3 = pedersen_hash(entry.timestamp, h2)
    return h3


def sign_publisher_registration(
    publisher_public_key, publisher, registration_private_key
):
    publisher_hash = hash_publisher(publisher_public_key, publisher)
    signature_r, signature_s = sign(publisher_hash, registration_private_key)
    return signature_r, signature_s


def hash_publisher(publisher_public_key, publisher):
    publisher_hash = pedersen_hash(publisher_public_key, publisher)
    return publisher_hash


def sign_publisher(publisher, publisher_private_key):
    signature_r, signature_s = sign(publisher, publisher_private_key)

    return signature_r, signature_s
