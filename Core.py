from json import load
from PIL import Image
from Functions import verify_data, digit_encoding, alphadigit_encoding, UTF8_encoding, determine_version, fill_data, split_into_blocks, RS_encoding, draw_info_codes, apply_data, choose_mask
from Masks import MASKS


CORRECTION_LEVELS = ['L', 'M', 'Q', 'H']
ENCODING_TYPES = {'digit': '0001', 'alphadigit': '0010', 'UTF8': '0100'}

with open('lengthes of service fields.json', 'r') as input_file:
    SERVICE_FIELDS_LENGTHES = load(input_file)

    
def main(raw_input, encoding_type, choice):
    if not verify_data(raw_input, encoding_type):
        return (0, None)
    
    else:
        if encoding_type == 'digit':
            bit_input = digit_encoding(raw_input)
        
        elif encoding_type == 'alphadigit':
            bit_input = alphadigit_encoding(raw_input.upper())
        
        if encoding_type == 'UTF8':
            bit_input = UTF8_encoding(raw_input)
            
        correction_level = CORRECTION_LEVELS[int(choice)]
        flag, version, index = determine_version(correction_level, encoding_type, len(bit_input))
        
        if not flag:
            return (1, None)
            
        else:
            if encoding_type == 'UTF8':
                bit_input = ENCODING_TYPES[encoding_type] + bin(len(bit_input) // 8)[2:].zfill(SERVICE_FIELDS_LENGTHES[encoding_type][index]) + bit_input + '0000'
            
            else:
                bit_input = ENCODING_TYPES[encoding_type] + bin(len(raw_input))[2:].zfill(SERVICE_FIELDS_LENGTHES[encoding_type][index]) + bit_input + '0000'
                
            byte_input = fill_data(correction_level, version, bit_input)
            
            blocks = split_into_blocks(correction_level, version, byte_input)
            
            RS_encoded_blocks = []
            
            for block in blocks:
                RS_encoded_blocks.append(RS_encoding(correction_level, version, block))
            
            bin_output = ''
            
            for i in range(len(blocks[-1])):
                for j in range(len(blocks)):
                    if i != len(blocks[j]):
                        bin_output += blocks[j][i]
                        
            for i in range(len(RS_encoded_blocks[-1])):
                for j in range(len(RS_encoded_blocks)):
                    if i != len(RS_encoded_blocks[j]):
                        bin_output += RS_encoded_blocks[j][i]
                
            
            white = (255, 255, 255, 255)
            black = (0, 0, 0, 255)
            
            path = 'frames/frame_' + str(version) + '.png'
            image = Image.open(path)
            size = image.size
            pixels = image.load()
            
            choose_mask(image, correction_level, size, pixels, bin_output, white, black)
            
            background = Image.new('RGBA', (image.width + 8, image.width + 8), color='white')
            background.paste(image, (4, 4, image.width + 4, image.width + 4))
            image = background.resize((800, 800), Image.NEAREST)
            
            return (2, image)