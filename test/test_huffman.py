import unittest
import os
import io
from unittest.mock import patch
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from src.HuffmanCoding import HuffmanNode, HuffmanCoding

class TestHuffmanCoding(unittest.TestCase):
    def setUp(self):
        self.huffman = HuffmanCoding()
        self.test_files = []

    def tearDown(self):
        for f in self.test_files:
            if os.path.exists(f):
                os.remove(f)

    def test_huffman_node_creation(self):
        """Test HuffmanNode initialization and comparison"""
        node_a = HuffmanNode('A', 5)
        node_b = HuffmanNode('B', 3)
        self.assertTrue(node_a > node_b)
        self.assertTrue(node_b < node_a)
        self.assertEqual(node_a.char, 'A')
        self.assertEqual(node_b.char, 'B')

    def test_build_huffman_tree(self):
        """Test tree construction from character frequencies"""
        # Test with simple input
        self.huffman.text_from_file = "AAABBC"
        self.huffman._build_huffman_tree()
    
        self.assertIsNone(self.huffman.root.char)
        self.assertEqual(self.huffman.root.freq, 6)
   
        left = self.huffman.root.left_child
        right = self.huffman.root.right_child
        self.assertTrue(left is not None or right is not None)

    def test_generate_codes(self):
        """Test code generation from Huffman tree"""
        self.huffman.text_from_file = "AABBCCC"
        self.huffman._build_huffman_tree()
        self.huffman._generate_codes_for_each_char()
        
        codes = self.huffman.codes
        self.assertEqual(len(codes), 3)
        self.assertTrue(all(len(code) > 0 for code in codes.values()))
        
        # Test code lengths
        a_code = codes['A']
        b_code = codes['B']
        c_code = codes['C']
        

        self.assertNotEqual(len(a_code), len(c_code))
        self.assertEqual(len(a_code), len(b_code))
        self.assertLess(len(c_code), len(b_code))

    def test_serialize_deserialize_tree(self):
        """Test tree serialization/deserialization roundtrip"""

        self.huffman.text_from_file = "TEST"
        self.huffman._build_huffman_tree()
        
        serialized = self.huffman._serialize_tree()
        original_root = self.huffman.root
        self.huffman.root, _ = self.huffman._deserialize_tree(serialized)
        
        self.assertEqual(original_root.left_child.char, 
                        self.huffman.root.left_child.char)
        self.assertEqual(original_root.right_child.char, 
                        self.huffman.root.right_child.char)

    def test_compress_decompress_roundtrip(self):
        """Test full compression/decompression cycle"""
        test_text = "Hello, World! "
        input_file = "test_input.txt"
        compressed_file = "test_compressed.huff"
        output_file = "test_output.txt"
        
        self.test_files.extend([input_file, compressed_file, output_file])

        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(test_text)
            
        self.huffman.compress_data(input_file, compressed_file)
        self.huffman.decompress_data(compressed_file, output_file)
        
        # Verify output matches input
        with open(output_file, 'r', encoding='utf-8') as f:
            self.assertEqual(f.read(), test_text)

    def test_edge_cases(self):
        """Test special cases and error handling"""
        # Empty file
        empty_file = "empty.txt"
        self.test_files.append(empty_file)  # Add to test_files for cleanup
        
        # Create empty file
        with open(empty_file, 'w') as f:
            pass
            
        # Test compression of empty file
        with self.assertRaises(ValueError):
            self.huffman.compress_data(empty_file, "dummy.huff")
                
        # Invalid decompression file
        with self.assertRaises(FileNotFoundError):
            self.huffman.decompress_data("nonexistent.huff", "dummy.txt")


    def test_progress_reporting(self):
        """Test progress callback functionality"""
        mock_callback = unittest.mock.Mock()
        test_text = "A" * 1000  # 1000 characters
        
        with patch('builtins.open', unittest.mock.mock_open(read_data=test_text)):
            self.huffman.compress_data("dummy.txt", "dummy.huff", mock_callback)
            
        # Verify callback was called multiple times
        self.assertGreater(mock_callback.call_count, 10)
        
        # Verify final progress is 100%
        args, _ = mock_callback.call_args
        self.assertEqual(args[0], 100)



    def test_byte_conversion(self):
        """Test bit-string to/from bytes conversion"""
        test_bits = "10101010" * 3  # 24 bits
        bytes_data = self.huffman._to_bytes(test_bits)
        reconstructed = self.huffman._from_bytes(bytes_data)
        self.assertEqual(reconstructed, test_bits)

if __name__ == '__main__':
    unittest.main()