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
        bit_string = ""
        for byte in data:
            bit_string += f"{byte:08b}"
        return bit_string
    

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

        if node.char is not None:
            self.codes[node.char] = current_code or "0"
            return

        if node.left_child is not None:
            self.generate_codes_for_each_char(node.left_child, current_code + "0")
        if node.right_child is not None:
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

        #test
        print("#################")
        print(encoded_bits)
        a = self._to_bytes(encoded_bits)
        print(encoded_bits)
        print(self._from_bytes(a))
        print(self._from_bytes(a) == encoded_bits) 
    

    def decompress_data(self, file_with_encoded_data : str, direction_for_save_decompress_file : str) -> str:


        try:
            if not file_with_encoded_data:
                raise ValueError("Encoded data is empty")

            decoded_data = ""
            current_node = self.root

            with open(file_with_encoded_data, "rb") as f:
                t_data = f.read()
            
            encoded_data_from_file = self._from_bytes(t_data)
            print(encoded_data_from_file)
            padding : int = int(encoded_data_from_file[:8], 2)
            encoded_data_from_file = encoded_data_from_file[:padding]

            for bit in file_with_encoded_data:
                print(current_node)
                if bit == "0":
                    current_node = current_node.left_child
                else:
                    current_node = current_node.right_child

                if current_node.char is not None:
                    decoded_data += current_node.char
                    current_node = self.root

            
            with open(direction_for_save_decompress_file, "w", encoding="utf-8") as f:
                f.write(decoded_data)
        
        except ArithmeticError as e:
            raise ValueError("Encoded data must contain only 0s and 1s")

a = "11111111"
ba = bytearray()
ba.append(int(a, 2))
f = f"{ba[0]:08b}"
print(type(f))