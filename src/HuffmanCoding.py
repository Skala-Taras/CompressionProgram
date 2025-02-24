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


    def _to_bytes(self, data):
        b = bytearray()
        for i in range(0, len(data), 8):
            b.append(int(data[i:i+8], 2))
        return bytes(b)
    

    def _from_bytes(self, data: bytes) -> str:
        return "".join(f"{byte:08b}" for byte in data)


    def _serialize_tree(self) -> str:
        if not self.root:
            return ""
        
        bits = ""

        def pre_order(node):
            if self.node.is_leaf():
                bits += '1'
                char_bytes = self.node.char.encode('utf-32-be')
                # bits += f"{bit}"
            else:
                bits += '0'
                pre_order(node.left_child)
                pre_order(node.right_child)
        pre_order(self.root)
        return bits

    
    def _deserialize_tree(self, data, index=0):
        ...

            


    def build_huffman_tree(self):
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


    def generate_codes_for_each_char(self, node = None, current_code="") -> None:
        """
        Recursively traverse the Huffman tree to generate the binary codes for each character.
        """
        if node is None:
            node = self.root 

        if node.char.is_leaf():
            self.codes[node.char] = current_code or "0"
            return

        if node.left_child.is_leaf():
            self.generate_codes_for_each_char(node.left_child, current_code + "0")
        if node.right_child.is_leaf():
            self.generate_codes_for_each_char(node.right_child, current_code + "1")


    def compress_data(self, read_direction : str, direction_for_save_data : str):
        
        with open(read_direction, 'r', encoding="utf-8") as file:
            self.text_from_file = file.read()
        

        self.build_huffman_tree()
        self.generate_codes_for_each_char()

        encoded_bits = "".join(self.codes[char] for char in self.text_from_file)

        extra_padding = 8 - (len(encoded_bits) % 8) if len(encoded_bits) % 8 != 0 else 0

        encoded_bits += "0" * extra_padding
        #convert extra_pading to byte and than add extra_padding before main encoded_bit
        encoded_bits = ("{0:08b}".format(extra_padding)) + encoded_bits

        with open(direction_for_save_data, 'wb') as binary_encoded_file:
            binary_encoded_file.write(self._to_bytes(encoded_bits))  


    def decompress_data(self, file_with_encoded_data : str, direction_for_save_decompress_file : str) -> str:


        try:
            if not file_with_encoded_data:
                raise ValueError("Encoded data is empty")

            
            current_node = self.root

            with open(file_with_encoded_data, "rb") as f:
                data = f.read()
            
            bit_string  = self._from_bytes(data)

            extra_padding  : int = int(bit_string[:8], 2)
            encoded_data = bit_string[8:]

            if extra_padding > 0:
                encoded_data = bit_string[:-extra_padding]

            decoded_data = ""
            current_node = self.root
            for bit in encoded_data:
                if bit == "0":
                    current_node = current_node.left_child
                else:
                    current_node = current_node.right_child

                if current_node.char.is_leaf():
                    decoded_data += current_node.char
                    current_node = self.root

            
            with open(direction_for_save_decompress_file, "w", encoding="utf-8") as f:
                f.write(decoded_data)
        
        except ArithmeticError as e:
            raise ValueError("Encoded data must contain only 0s and 1s")


