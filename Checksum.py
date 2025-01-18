"""
Function to split a hexadecimal number into 4-bit chunks and pad the leftmost chunk with zeros if necessary.
Author: Nithish K Gnani
"""
def split_hex(hex_str):
    hex_chunks = []
    while len(hex_str) > 0:
        chunk = hex_str[-4:].zfill(4)  # Pad the chunk with zeros if necessary
        hex_chunks.insert(0, chunk)
        hex_str = hex_str[:-4]
    return hex_chunks

# Function to perform sum of a list of hexadecimal numbers
# by converting them to decimal and then to hexadecimal
def sum_hex(hex_list):
    decimal_sum = sum(int(hex_num, 16) for hex_num in hex_list)
    hex_sum = hex(decimal_sum)[2:]    
    return hex_sum

# Function to covert a hexadecimal number to binary
# and do one's complement
def ones_complement(hex_num):
    bin_result = bin(int(hex_num, 16))[2:].zfill(16)
    checksum = hex(int(''.join('1' if bit == '0' else '0' for bit in bin_result), 2))[2:].zfill(4)
    return checksum

# Function to compute the checksum of a hexadecimal number
# using all the above functions
def checksum_calc(hex_number):
    while len(hex_number) > 4:
        hex_list = split_hex(hex_number)
        hex_number = sum_hex(hex_list)
    checksum = ones_complement(hex_number)
    return checksum


hex_number = '0a7240b20a72404900110014138813880014000048656c6c6f2c20776f726c64'

hex_number = input("Enter a hexadecimal number: ")
checksum = checksum_calc(hex_number)
print(f"Checksum: {checksum}")