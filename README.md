# Huffman Compression Tool

A Python-based file compression and decompression tool using Huffman coding algorithm with a graphical user interface.

## Overview

This application provides a simple and efficient way to compress and decompress files using Huffman coding. It features a user-friendly GUI built with PyQt6 and implements the Huffman coding algorithm for data compression.

## Features

- Graphical User Interface for easy file handling
- File compression using Huffman coding algorithm
- File decompression capability
- Progress tracking during compression/decompression
- Support for any file type
- Custom `.huffc` file format for compressed files

## Technical Details

### Components

1. **UIApp.py**: Contains the graphical user interface implementation
   - Built using PyQt6
   - Features compression and decompression buttons
   - Includes progress tracking
   - Handles file selection and saving

2. **HuffmanCoding.py**: Implements the Huffman coding algorithm
   - `Huffman_node`: Class for creating nodes in the Huffman tree
   - `HuffmanCoding`: Main class implementing compression logic
   - Time complexity: O(n log n) for tree construction

### Algorithm

The compression uses Huffman coding which:
1. Calculates character frequencies in the input
2. Builds a priority queue based on frequencies
3. Constructs a Huffman tree
4. Generates binary codes for each character
5. Encodes/decodes data using generated codes

Time complexity: O(n log n) for this algorithm

### Prerequisites
- Python 3.9+
- PyQt6