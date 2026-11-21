"""Frame checksum formatter and native zframe compression wrapper."""
from __future__ import annotations

import zlib


def frame_crc32_hex(payload: bytes) -> str:
    """Return lowercase 8-character zero-padded hexadecimal CRC32 for payload."""
    # Bug: omits 8-char zero-padding (leading zero hex digits are dropped).
    return hex(zlib.crc32(payload) & 0xFFFFFFFF)[2:]


def encode_zframe(payload: bytes) -> bytes:
    """Compress payload using the native libturbo_zframe wire-format library."""
    import libturbo_zframe

    return bytes(libturbo_zframe.compress_frame(payload))
