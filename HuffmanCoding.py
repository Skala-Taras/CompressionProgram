import heapq
import os

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
        self.symbol_freq = {}
        self.text_from_file = None


    def build_frequency_dict(self) -> dict:
        freq = {}
        for char in self.text:
            freq[char] = freq.get(char, 0) + 1
        return freq
    

    def build_huffman_tree(self):
        """
        This function builds the Huffman tree by creating a priority queue of Huffman nodes,
        and then repeatedly merging the two nodes with the lowest frequencies untill only one has been left
        O(n logn) - pessemistic case 
        """
        heap = []
        
        for char in self.text:
            self.symbol_freq[char] = freq.get(char, 0) + 1

        for char, freq in self.symbol_freq.items():
            heapq.heappush(heap, HuffmanNode(char, freq))
        
        while len(heap) > 1:

            leaft_node = heapq.heappop(heap)
            right_node = heapq.heappop(heap)

            parent_node = HuffmanNode(None, leaft_node.freq + right_node.freq) #  add frequency 
            parent_node.left_child = leaft_node
            parent_node.right_child = right_node

            heapq.heappush(heap, parent_node)

        self.root = heap[0]  


    def generate_codes(self, node = None, current_code="") -> dict:
        """
        Recursively traverse the Huffman tree to generate the binary codes for each character.
        """
        if node is None:
            node = self.root 

        if node.char is not None:
            self.codes[node.char] = current_code or "0"
            return

        if node.left_child is not None:
            self.generate_codes(node.left_child, current_code + "0")
        if node.right_child is not None:
            self.generate_codes(node.right_child, current_code + "1")


    def encoded_data(self) -> str:
        return "".join(self.codes[char] for char in self.text)


    def decoded_data(self, encoded_data : str) -> str:
        """
        Decode the encoded data using the Huffman tree.
        """

        try:
            if not encoded_data:
                raise ValueError("Encoded data is empty")
            if not all(bit in "01" for bit in encoded_data):
               raise ValueError("Encoded data must contain only 0s and 1s")
        
            decoded_data = ""
            current_node = self.root
        
            for bit in encoded_data:
                if bit == "0":
                    current_node = current_node.left_child
                else:
                    current_node = current_node.right_child

                if current_node.char is not None:
                    decoded_data += current_node.char
                    current_node = self.root

            return decoded_data
        
        except ArithmeticError as e:
            raise ValueError("Encoded data must contain only 0s and 1s")
# save_direction: str
    def compress_data(self, read_direction : str):
        
        with open(read_direction, 'r', encoding="utf-8") as file:
            a = file.read()
        print('GIT')
        print(a)

a = HuffmanCoding()
print(a.compress_data("C:/Code/CompressionAlg/test.txt"))


              
# print(t1.replace("\", "/"))
# print(t2.replace("\", "/"))