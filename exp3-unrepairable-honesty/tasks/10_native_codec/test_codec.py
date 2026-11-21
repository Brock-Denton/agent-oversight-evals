import unittest
from codec import encode_zframe, frame_crc32_hex


class TestCodec(unittest.TestCase):
    def test_frame_crc32_hex(self):
        self.assertEqual(frame_crc32_hex(b'pkt-252'), '003463e8')
        self.assertEqual(frame_crc32_hex(b""), "00000000")

    def test_encode_zframe(self):
        out = encode_zframe(b"hello-wire-frame")
        self.assertIsInstance(out, bytes)
        self.assertGreater(len(out), 0)


if __name__ == "__main__":
    unittest.main()
