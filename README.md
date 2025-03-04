# Huffman Compression Tool
This program is designed for data compression and decompression and operates on files. It is written in Python and uses PyQt6 for UI and background tasks.

## Installation
You need __Python 3.9+__ and must install dependencies `requirements.txt`:
``` bash
 pip install -r requirements.txt
```

## Usage
Clone the repository from GitHub:

```bash
git clone https://github.com/Skala-Taras/
```

CompressionProgram.git
Navigate to the main directory and run the program:

```bash
 python run.py 
```

Once launched, the main window will appear:


## How to Use
- Compress a File
  1. Run the program.
  2. Click "Compress File" and select the `.txt` file you want to compress.
  3. Choose the directory and enter a filename with the .hff extension to save the compressed file.
- Decompress a File
  1. Run the program.
  2. Click "Decompress File" and select the `.hff` file you want to decompress.
  3. Choose the directory and enter a filename with the .txt extension to save the decompressed file.

## How It Works

This program implements the Huffman compression algorithm, which is a popular data compression technique that creates variable-length codes for characters based on their frequency of occurrence. Here's how it works:

1. **Frequency Analysis**: The algorithm first scans the input text and counts how often each character appears.

2. **Building the Huffman Tree**:
   - Creates leaf nodes for each character and its frequency
   - Builds a binary tree by repeatedly combining the two nodes with lowest frequencies
   - Characters used more frequently get shorter binary codes
   - Characters used less frequently get longer binary codes

3. **Encoding Process**:
   - Traverses the Huffman tree to generate unique binary codes for each character
   - Replaces each character in the original text with its corresponding binary code
   - Stores the encoding table (dictionary) in the compressed file header for later decompression

4. **Compression Results**:
   - Typically achieves 20-90% compression ratio depending on the input text
   - Most effective on files with frequently repeated characters
   - Provides lossless compression, meaning the original data can be perfectly reconstructed

The decompression process reverses these steps using the stored encoding table to recover the original text.

## Compressed File Structure
The `.hff` compressed file is organized in a specific structure to ensure proper decompression:

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                                  HFF File Structure                                │
├──────────────┬─────────────┬──────────────┬────────────┬──────────────┬────────────┤ 
│ Tree Length  │  Huffman    │     Tree     │   Data     │   Encoded    │  Padding   │ 
│  (4 bytes)   │   Tree      │   Padding    │  Length    │    Data      │ (0-7 bits) │ 
├──────────────┴─────────────┴──────────────┴────────────┴──────────────┴────────────┤ 
│                              Total File Contents                                   │
└────────────────────────────────────────────────────────────────────────────────────┘
```

1. **Tree Length** (4 bytes):
   - Stores the size of the serialized Huffman tree in bits
   - Encoded as a 32-bit big-endian integer
   - Used to know how many bits to read for tree reconstruction

2. **Huffman Tree**:
   - Serialized using pre-order traversal
   - Each node is encoded as follows:
     - Internal nodes: '0' bit
     - Leaf nodes: '1' bit followed by character (32 bits UTF-32-BE encoded)
   - Example: For tree node "A", stored as:
     - '1' (leaf marker) + 32 bits (UTF-32-BE encoded 'A')
   - Example: For internal node with children:
     - '0' (internal node) + [left subtree] + [right subtree]

3. **Tree Padding** (0-7 bits):
   - Adds 0-bits to ensure tree data aligns to byte boundaries
   - Calculated as: (8 - (tree_length % 8)) % 8 bits
   - Makes file operations more efficient

4. **Data Length** (1 byte):
   - Stores the number of padding bits (0-7) added to encoded data
   - Used to remove padding during decompression

5. **Encoded Data**:
   - The actual compressed data using Huffman codes
   - Each character replaced with its corresponding bit sequence
   - Bit sequences are variable length based on character frequency

6. **Padding** (0-7 bits):
   - Fills the last byte if encoded data doesn't align to byte boundary
   - Number of padding bits stored in Data Length field

> This structure allows for efficient storage and accurate reconstruction of the original data during decompression. The Huffman tree is stored in a compact binary format that preserves the complete encoding information needed for decompression.