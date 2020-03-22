import argparse
import cv2
import pprint
import steno

def read_text_file(file_name):

    with open(file_name, "rb") as file:
        content = file.read()
        data = bytearray(content)
        return data

def encode(args):
    
    # TODO: Check arguments
    #...

    data = read_text_file(args.text_file)
    image = cv2.imread(args.input_image_file)

    image_buff = image.ravel()
    steno.steno_byte_array(image_buff, data)

    cv2.imwrite(args.output_image_file, image)

def decode(args):

    # TODO: Check arguments
    #...

    image = cv2.imread(args.input_image_file)
    image_buff = image.ravel()

    #print(image_bytes)
    data = steno.unsteno_byte_array(image_buff)

    with open(args.text_file, "wb") as file:
        file.write(data)

# >> Main >>>>>

description="Proof of consept. Encode text file to image file or decode text file from image file"
arg_parser = argparse.ArgumentParser(description=description)

arg_parser.add_argument("-a", required=True, help='action. "encode" or "decode"', dest="action")

arg_parser.add_argument("-i", required=True, help="Input image file name", dest="input_image_file")
arg_parser.add_argument("-o", default="output.png", required=False, help="Output image file name", dest="output_image_file")
arg_parser.add_argument("-t", required=True, help='Text file. Input or output depending on "action"', dest="text_file")

#args = arg_parser.parse_args(["-aencode", "-i1.png", "-ttext_eng.txt"])
args = arg_parser.parse_args()
#print(args)

if args.action == "encode":
    encode(args)
else:
    decode(args)


print("OK")



