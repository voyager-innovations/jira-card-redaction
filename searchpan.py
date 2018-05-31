from PIL import Image
import pytesseract
import cv2
import os
import sys
import re
import time
import datetime
import argparse

text = "--"
global num_files_processed, num_images_processed, num_images_with_pan
global start_time, end_time, elapsed_time


def get_params():
    global params
    global date_yesterday

    # - gets script/command-line parameters and perform some validations
    try:
        parser = argparse.ArgumentParser(description="Outputs a list of suspected image files with PAN")
        parser.add_argument("-v", '--version', action='version', version='%(prog)s 1.0')
        parser.add_argument("-l", '--less', action='store_true', default=False, dest='is_print_less_details',
                            help='print less details on the screen  ')
        parser.add_argument("-d", '--dir', action='store', type=valid_dir, dest='root_dir',
                            help='root directory to start traversing. Defaults to current working directory.')

        params = parser.parse_args()

        return params

    except Exception as e:
        print(e)
        sys.exit(0)

def valid_dir(dir):
    # - returns date in YYYY-MM-DD format if valid. Otherwise, raises argument type error.
    if os.path.isdir(dir):
        return dir
    else:
        raise argparse.ArgumentTypeError("Directory does not exist")


def image_to_string(file):
    text = ""
    try:
        # print("processing...")

        img = cv2.imread(file, cv2.IMREAD_UNCHANGED)

        # print('Original Dimensions : ',img.shape)

        scale_percent = 300 # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)

        # resize image
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        # print('Resized Dimensions : ',resized.shape)

        #cv2.imshow("Resized image", resized)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        cv2.imwrite(file + "_r.png", resized)

        im = Image.open(file + "_r.png")

        text = pytesseract.image_to_string(im, lang = 'eng')
        file=file + "_r.png"
        os.remove(file)


        # os.remove(file + "_r.png")

    except :
        print("an error was encountered")

    return text
    
def get_elapsed_time():
    end_time = time.time()
    temp_time = end_time - start_time
    hours = temp_time // 3600
    temp_time = temp_time - 3600 * hours
    minutes = temp_time // 60
    seconds = temp_time - 60 * minutes
    elapsed_time = '%d:%d:%d' % (hours, minutes, seconds)

    # print("Elapsed time = ", elapsed_time)
    return elapsed_time

def find_card_number(string):
    pattern = r"(^|\s+)(\d{4}[ -]\d{4}[ -]\d{4}[ -]\d{4})(?:\s+|$)"

    match = re.search(pattern, string)

    if match:
        credit_card_num = match.group(0).strip()
        credit_card_num = credit_card_num.replace(" ", '')
        # mask
        credit_card_num = credit_card_num[:6] + 'X' * 6 + credit_card_num[-4:]
        if not params.is_print_less_details:
            print(credit_card_num)
        return credit_card_num
    else:
        return ""    

def check_image_with_pil(file):
    try:
       Image.open(file)
    except IOError:
       return False
    return True


def main():
    global start_time, end_time, elapsed_time, params
    card_number = ""
    num_files_processed = 0
    num_images_processed = 0
    num_images_with_pan = 0
    run_result = "\n"
    start_time = time.time()

    results_file = open("results.txt", "w")

    results_file.write("Suspected image files with PAN: \r\n")

    # get script/command-line parameters
    params = get_params()

    # traverse root directory, and list directories as dirs and files as files
    # print(os.getcwd())
    for root, dirs, files in os.walk(params.root_dir):
        if "thumbs" in dirs:
            dirs.remove("thumbs")
        if ".DS_Store" in files:
            files.remove(".DS_Store")

        path = root.split(os.sep)
        # print( os.path.abspath(root))
        os.chdir( os.path.abspath(root))
        if not params.is_print_less_details:
            print((len(path) - 1) * '---', os.path.abspath(root))
        # results_file.write("---%s\r\n" % os.path.abspath(root))
        for file in files:
            # print("file= ", file)
            num_files_processed += 1
            if not params.is_print_less_details:
                print(len(path) * '---', file)
            # results_file.write('---%s\r\n' %  file)
            if check_image_with_pil(file):
                num_images_processed += 1
                text = image_to_string(file)
                # print(text)
                card_number = find_card_number(text)
                if card_number != "":
                    num_images_with_pan += 1
                    # print(len(path) * '-->', os.path.abspath(file), "\n", card_number)
                    abspath = str(os.path.abspath(file))
                    results_file.write("%s\r\n" % abspath)
                    results_file.write("--> %s\r\n" % card_number)

    # num_files_processed less 1 (reslts.txt)
    num_files_processed -= 1
    results_file.write("Number of files processed : %d\r\n" %  num_files_processed)
    results_file.write("Number of images processed : %d\r\n" % num_images_processed)
    results_file.write("Number of images with PAN : %d\r\n" %  num_images_with_pan)
    results_file.write("Elapsed time: " + get_elapsed_time() )

    results_file.close()

    print("Number of files processed : ", num_files_processed)
    print("Number of images processed : ", num_images_processed)
    print("Number of images with PAN : ", num_images_with_pan)

    run_result += 'Elapsed time: %s' % get_elapsed_time() + '\n'

    print (run_result)

main()
sys.exit(0)

print(text)
