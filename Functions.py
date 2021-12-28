from json import load
from math import ceil
from Masks import MASKS


with open('alphabet.json', 'r') as input_file:
    ALPHABET = load(input_file)

with open('amount of data.json', 'r') as input_file:
    MAXIMUM_SIZE = load(input_file)
    
with open('lengthes of service fields.json', 'r') as input_file:
    SERVICE_FIELDS_LENGTHES = load(input_file)
    
with open('amount of blocks.json', 'r') as input_file:
    AMOUNT_OF_BLOCKS = load(input_file)
    
with open('galois field.json', 'r') as input_file:
    GALOIS_FIELD = load(input_file)
            
with open('reverse galois field.json', 'r') as input_file:
    REVERSE_GALOIS_FIELD = load(input_file)
    
with open('generating polynomials.json', 'r') as input_file:
    GENERATING_POLYNOMIALS = load(input_file)
        
with open('codes of mask and correction level.json', 'r') as input_file:
    MASK_AND_CORRECTION_LEVEL_CODES = load(input_file)
    
with open('amount of correction bytes.json', 'r') as input_file:
    AMOUNT_OF_CORRECTION_BYTES = load(input_file)


def verify_data(string, encoding_type):
    if string.isdigit() and encoding_type == 'digit':
        return True
    
    elif encoding_type == 'alphadigit':
        for symbol in string.upper():
            if symbol not in ALPHABET:
                return False
        
        else:
            return True
    
    elif encoding_type == 'UTF8':
        return True
    
    else:
        return False

def digit_encoding(string):
    blocks = []
    
    for i in range(ceil(len(string) / 3)):
        blocks.append(string[i*3:i*3+3])
    
    encoded_data = ''
    encoded_blocks_lengthes = [4, 7, 10]
    
    for block in blocks:
        encoded_block = bin(int(block))[2:]
        encoded_data += encoded_block.zfill(encoded_blocks_lengthes[len(block)-1])
        
    return encoded_data

def alphadigit_encoding(string):
    encoded_data = ''
    
    for i in range(len(string) // 2):
        encoded_block = bin(ALPHABET[string[i*2]] * 45 + ALPHABET[string[i*2+1]])[2:]
        encoded_data += encoded_block.zfill(11)
        
    if len(string) % 2:
        encoded_block = bin(ALPHABET[string[-1]])[2:]
        encoded_data += encoded_block.zfill(6)
        
    return encoded_data
   
def UTF8_encoding(string):
    encoded_data = ''
    list_of_bytes = list(string.encode("utf-8"))
    
    for byte in list_of_bytes:
        encoded_data += bin(byte)[2:].zfill(8)
        
    return encoded_data

def determine_version(correction_level, encoding_type, information_size):
    flag = False
    version = 0
    
    for i in range(40):
        if i < 9:
            index = 0
        elif 9 <= i < 26:
            index = 1
        else:
            index = 2
        
        if (information_size + 4 + SERVICE_FIELDS_LENGTHES[encoding_type][index]) <= MAXIMUM_SIZE[correction_level][i]:
            flag = True
            version = i + 1
            break
            
    return flag, version, index

def fill_data(correction_level, version, bit_data):
    amount_of_zeros = (8 - (len(bit_data) % 8)) % 8
    bit_data += '0' * amount_of_zeros
    
    for i in range((MAXIMUM_SIZE[correction_level][version-1] - len(bit_data)) // 8):
        if i % 2 == 0:
            bit_data += '11101100'
        
        else:
            bit_data += '00010001'
    
    byte_data = []      
    for i in range(len(bit_data) // 8):
        byte_data.append(bit_data[i*8:(i+1)*8])
    
    return byte_data

def split_into_blocks(correction_level, version, byte_data):
    blocks_amount = AMOUNT_OF_BLOCKS[correction_level][version-1]
    normal_blocks_amount = blocks_amount - len(byte_data) % blocks_amount
    extended_blocks_amount = len(byte_data) % blocks_amount
    normal_blocks_length = len(byte_data) // blocks_amount
    extended_blocks_length = ceil(len(byte_data) / blocks_amount)
    blocks = [[] for i in range(blocks_amount)]
    
    for i in range(normal_blocks_amount):
        blocks[i] = byte_data[i*normal_blocks_length:(i+1)*normal_blocks_length]
        
    for i in range(extended_blocks_amount):
        blocks[normal_blocks_amount+i] = byte_data[normal_blocks_amount*normal_blocks_length+i*extended_blocks_length:normal_blocks_amount*normal_blocks_length+(i+1)*extended_blocks_length]
        
    return blocks

def RS_encoding(correction_level, version, byte_data):
    correction_bytes_amount = AMOUNT_OF_CORRECTION_BYTES[correction_level][version-1]
    generating_polynomial = GENERATING_POLYNOMIALS[str(correction_bytes_amount)]
    
    list_of_bytes = [int(x, 2) for x in byte_data]
    list_of_bytes.extend([0] * abs(correction_bytes_amount - len(list_of_bytes)))
    
    for i in range(len(byte_data)):
        a = list_of_bytes.pop(0)
        list_of_bytes.append(0)
        
        if a != 0:
            b = REVERSE_GALOIS_FIELD[a]
            
            for j in range(correction_bytes_amount):
                c = GALOIS_FIELD[(generating_polynomial[j] + b) % 255]
                list_of_bytes[j] ^= c
            
    final_list = []
    
    for i in range(correction_bytes_amount):
        final_list.append(bin(list_of_bytes[i])[2:].zfill(8))
        
    return final_list

def draw_info_codes(correction_level, mask, size, pixels, white, black):    
    for j in range(6):
        color = black if (MASK_AND_CORRECTION_LEVEL_CODES[correction_level][mask][j] == '1') else white
        pixels[8, size[1] - 1 - j], pixels[j, 8] = color, color
            
    color = black if (MASK_AND_CORRECTION_LEVEL_CODES[correction_level][mask][6] == '1') else white
    pixels[8, size[1] - 7], pixels[7, 8] = color, color
    color = black if (MASK_AND_CORRECTION_LEVEL_CODES[correction_level][mask][7] == '1') else white
    pixels[size[1] - 8, 8], pixels[8, 8] = color, color
    color = black if (MASK_AND_CORRECTION_LEVEL_CODES[correction_level][mask][8] == '1') else white
    pixels[size[1] - 7, 8], pixels[8, 7] = color, color
        
    for i in range(9, 15):
        color = black if (MASK_AND_CORRECTION_LEVEL_CODES[correction_level][mask][i] == '1') else white
        pixels[size[1] - 15 + i, 8], pixels[8, 14 - i] = color, color

def apply_data(mask, size, pixels, bin_output, white, black):
    i = size[0] - 1
    current = 0
    length = len(bin_output)
    flag = True
        
    while i > 0:
        j = size[1] - 1
            
        while j >= 0:
            if flag:
                if pixels[i, j][3] == 0:
                    color = black if (MASKS[mask](i, j, int(current < length and bin_output[current] == '1'))) else white
                    pixels[i, j] = color
                    current += 1
                        
                if pixels[i - 1, j][3] == 0:
                    color = black if (MASKS[mask](i - 1, j, int(current < length and bin_output[current] == '1'))) else white
                    pixels[i - 1, j] = color
                    current += 1
                    
            else:
                if pixels[i, size[1] - 1 - j][3] == 0:
                    color = black if (MASKS[mask](i, size[1] - 1 - j, int(current < length and bin_output[current] == '1'))) else white
                    pixels[i, size[1] - 1 - j] = color
                    current += 1
                        
                if pixels[i - 1, size[1] - 1 - j][3] == 0:
                    color = black if (MASKS[mask](i - 1, size[1] - 1 - j, int(current < length and bin_output[current] == '1'))) else white
                    pixels[i - 1, size[1] - 1 - j] = color
                    current += 1                    
                    
            j -= 1
                
        i -= 3 if (i == 8) else 2
        flag = not flag

def choose_mask(image, correction_level, size, pixels, bin_output, white, black):
    penalty_points = [0 for i in range(8)]
    
    for i in range(8):
        current_image = image.copy()
        current_pixels = current_image.load()
        draw_info_codes(correction_level, i, size, current_pixels, white, black)
        apply_data(i, size, current_pixels, bin_output, white, black)
            
        for j in range(size[1]):
            current_streak = 0
            current_color = white
                
            for k in range(size[0]):
                if current_pixels[k, j] == current_color:
                    current_streak += 1
                        
                else:
                    if current_streak >= 5:
                        penalty_points[i] += max(0, current_streak - 2)
                        
                    current_streak = 1
                    current_color = current_pixels[k, j]
            
            if current_streak >= 5:
                penalty_points[i] += max(0, current_streak - 2)
                
        for j in range(size[0]):
            current_streak = 0
            current_color = white
                    
            for k in range(size[1]):
                if current_pixels[j, k] == current_color:
                    current_streak += 1
                            
                else:
                    if current_streak >= 5:
                        penalty_points[i] += max(0, current_streak - 2)
                                
                    current_streak = 1
                    current_color = current_pixels[j, k]
                    
            if current_streak >= 5:        
                penalty_points[i] += max(0, current_streak - 2)    
                  
        for j in range(size[1] - 1):
            for k in range(size[0] - 1):
                if current_pixels[k,j] == current_pixels[k+1,j] == current_pixels[k,j+1] == current_pixels[k+1,j+1]:
                    penalty_points[i] += 3
                    
        for j in range(size[1]):
            for k in range(size[0] - 6):
                if [current_pixels[k,j], current_pixels[k+1,j], current_pixels[k+2,j], current_pixels[k+3,j], current_pixels[k+4,j], 
                    current_pixels[k+5,j], current_pixels[k+6,j]] == [black, white, black, black, black, white, black]:
                    flag = False
                    
                    if k > 3:
                        if current_pixels[k-4,j] == current_pixels[k-3,j] == current_pixels[k-2,j] == current_pixels[k-1,j] == white:
                            flag = True
                            
                    if k < size[0] - 10:
                        if current_pixels[k+7,j] == current_pixels[k+8,j] == current_pixels[k+9,j] == current_pixels[k+10,j] == white:
                            flag = True
                            
                    if flag:
                        penalty_points[i] += 40
                        
        for j in range(size[1]):
            for k in range(size[0] - 6):
                if [current_pixels[k,j], current_pixels[k+1,j], current_pixels[k+2,j], current_pixels[k+3,j], current_pixels[k+4,j], 
                    current_pixels[k+5,j], current_pixels[k+6,j]] == [black, white, black, black, black, white, black]:
                    flag = False
                                    
                    if k > 3:
                        if current_pixels[k-4,j] == current_pixels[k-3,j] == current_pixels[k-2,j] == current_pixels[k-1,j] == white:
                            flag = True
                                            
                    if k < size[1] - 10:
                        if current_pixels[k+7,j] == current_pixels[k+8,j] == current_pixels[k+9,j] == current_pixels[k+10,j] == white:
                            flag = True
                                            
                    if flag:
                        penalty_points[i] += 40
        
        black_count = 0
        
        for j in range(size[1]):
            for k in range(size[0]):
                if current_pixels[k, j] == black:
                    black_count += 1
                    
        penalty_points[i] += 2 * abs(int(100 * black_count / (size[0] * size[1]) - 50))

    mask = penalty_points.index(min(penalty_points))
    draw_info_codes(correction_level, mask, size, pixels, white, black)
    apply_data(mask, size, pixels, bin_output, white, black)