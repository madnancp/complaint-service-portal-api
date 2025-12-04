from hashlib import sha256


def get_checksum(message: str) -> str:
    return sha256(message.encode()).hexdigest()


def match_checksum(message: str, checksum: str) -> bool:
    return get_checksum(message) == checksum
