import heapq

class HuffmanNode:
    """
       A node in the Huffman tree.
       
       Attributes:
           char: The character stored in the node
           freq: The frequency of the character
           left_child: Left child node
           right_child: Right child node
       """
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left_child = None
        self.right_child = None
    
    def is_leaf(self):
        return self.char is not None
     
    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanCoding:
    """ 
    A class that implements the Huffman coding algorithm.
    """

    def __init__(self):
        self.root = None
        self.codes = {}
        self.symbols_freq = {}
        self.text_from_file = None


    def _to_bytes(self, data : str):
        b = bytearray()
        for i in range(0, len(data), 8):
            b.append(int(data[i:i+8], 2))
        return bytes(b)
    

    def _from_bytes(self, data: bytes) -> str:
        return "".join(f"{byte:08b}" for byte in data)


    def _serialize_tree(self) -> str:
        if not self.root:
            return ""
        
        def pre_order(node):
            bits = []
            if node.char is not None:
                bits.append('1')
                char_bytes = node.char.encode('utf-32-be')
                for byte in char_bytes:
                    bits.append(f"{byte:08b}")
            else:
                bits.append('0')
                bits.append(pre_order(node.left_child))
                bits.append(pre_order(node.right_child))
            return "".join(bits)
        
        return pre_order(self.root)

    
    def _deserialize_tree(self, bit_stream :str, index=0) -> tuple[HuffmanNode | None , int]:
        
        if index >= len(bit_stream):
            return None, index

        bit = bit_stream[index]
        index += 1 

        if bit == '0':
            node = HuffmanNode(None, 0) #Frequency is not necessary
            node.left_child, index = self._deserialize_tree(bit_stream, index)
            node.right_child, index = self._deserialize_tree(bit_stream, index)
            return node , index
        
        elif bit == '1':
            char_bits = bit_stream[index: index+32]
            index += 32 #because our symbol size consists of 4 bytes
            byte_list = [int(char_bits[i:i+8], 2) for i in range(0, 32, 8)]
            char = bytes(byte_list).decode('utf-32-be')
            print(f"---> {char}")
            return HuffmanNode(char, 0), index #Frequency is not necessary

        else: raise ValueError("Invalid bit in tree deserialization") 


    def _build_huffman_tree(self):
        """
        This function builds the Huffman tree by creating a priority queue of Huffman nodes,
        and then repeatedly merging the two nodes with the lowest frequencies untill only one has been left
        O(n logn) - pessemistic case 
        """
        heap = []
        
        for char in self.text_from_file:
            self.symbols_freq[char] = self.symbols_freq.get(char, 0) + 1

        for char, freq in self.symbols_freq.items():
            heapq.heappush(heap, HuffmanNode(char, freq))
        
        while len(heap) > 1:

            leaft_node = heapq.heappop(heap)
            right_node = heapq.heappop(heap)

            parent_node = HuffmanNode(None, leaft_node.freq + right_node.freq) #  add frequency 
            parent_node.left_child = leaft_node
            parent_node.right_child = right_node

            heapq.heappush(heap, parent_node)

        self.root = heap[0]  


    def _generate_codes_for_each_char(self, node = None, current_code="") -> None:
        """
        Recursively traverse the Huffman tree to generate the binary codes for each character.
        """
        if node is None:
            node = self.root 

        if node.char is not None:
            self.codes[node.char] = current_code or "0"
            return

        if node.left_child is not None:
            self._generate_codes_for_each_char(node.left_child, current_code + "0")
        if node.right_child is not None:
            self._generate_codes_for_each_char(node.right_child, current_code + "1")


    def compress_data(self, read_path : str, write_path : str) -> None:

        with open(read_path, 'r', encoding="utf-8") as file:
            self.text_from_file = file.read()
        
        self._build_huffman_tree()
        self._generate_codes_for_each_char()

        bits_tree = self._serialize_tree()
        tree_length = len(bits_tree)
        
        tree_length_bytes = tree_length.to_bytes(4, 'big')

        padded_tree : str = bits_tree + '0' * ((8 - (len(bits_tree) % 8)) % 8)
        tree_bytes : bytes = self._to_bytes(padded_tree)

        encoded_data : str = "".join(self.codes[char] for char in self.text_from_file)

        #convert extra_pading to byte and than add extra_padding before main encoded_bit
        data_padding = (8 - (len(encoded_data) % 8)) % 8
        encoded_data += '0' * data_padding

        data_bytes = self._to_bytes(encoded_data)

        all_bytes = (
                tree_length_bytes +
                tree_bytes + 
                bytes([data_padding]) + 
                data_bytes
            )
              
        with open(write_path, 'wb') as f:
            f.write(all_bytes)  


    def decompress_data(self, file_with_encoded_data : str, write_path : str) -> str:

        try:
            if not file_with_encoded_data:
                raise ValueError("Encoded data is empty")

            with open(file_with_encoded_data, "rb") as f:
                data = f.read()

            data_bits : str = self._from_bytes(data)

            if len(data_bits) < 32:
                raise ValueError("Invalid compressed data: Missing tree length header.")
            
            len_tree = int(data_bits[:32], 2)   # First element (32 bits) in the data is len tree 
            data_bits = data_bits[32:]
            
            tree_bytes_count = (len_tree + 7) // 8  # Number of bytes used for the tree
            tree_bits_padded_length = tree_bytes_count * 8  # Total bits (with padding)

            # Extract the tree bits (including padding) and truncate to original length
            if len(data_bits) < tree_bits_padded_length:
                raise ValueError("Invalid compressed data: Tree data corrupted.")
            
            tree_bits_padded = data_bits[:tree_bits_padded_length]
            tree_bits = tree_bits_padded[:len_tree]  # Remove padding
            data_bits = data_bits[tree_bits_padded_length:]
                
            self.root, _ = self._deserialize_tree(tree_bits)

            extra_padding = int(data_bits[:8], 2)
            data_bits = data_bits[8:]  # Skip the 8-bit padding header.
            
            if extra_padding > 0:
                data_bits = data_bits[:-extra_padding]

            decoded_data = ""
            current_node = self.root

            for bit in data_bits:
                if bit == "0":
                    current_node = current_node.left_child
                else:
                    current_node = current_node.right_child

                if current_node.char is not None:
                    decoded_data += current_node.char
                    current_node = self.root

            
            with open(write_path, "w", encoding="utf-8") as f:
                f.write(decoded_data)
        
        except ArithmeticError as e:
            raise ValueError("Encoded data must contain only 0s and 1s")





