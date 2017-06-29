#Huge thanks to sentdex for the awesome tutorial on Youtube https://www.youtube.com/watch?v=jG3bu0tjFbk.
#This tool is based on his tutorial.

import os
import cv2
import urllib
from urlgrabber import urlgrab


#Downloaded images are resized to 100x100
def get_neg_images(url, neg_image_folder):
    images_urls = urllib.urlopen(url).read().decode('utf8')
    pic_num = 1
    for iurl in images_urls.split('\n'):
        try:
            print (iurl)
            urlgrab(iurl, neg_image_folder + "/" + str(pic_num) + ".jpg", timeout = 20)
            img = cv2.imread(neg_image_folder + "/" + str(pic_num) + ".jpg", cv2.IMREAD_GRAYSCALE)
            resize_img = cv2.resize(img, (100, 100))
            cv2.imwrite(neg_image_folder + "/" + str(pic_num) + ".jpg", resize_img)
            pic_num += 1
        except Exception as e:
            print str(e)



def remove_ugly(ugly_folder, neg_image_folder):
    for img in os.listdir(neg_image_folder):
        for ugly_img in os.listdir(ugly_folder):
            try:
                current_img_path = neg_image_folder + "/" + str(img)
                ugly = cv2.imread(ugly_folder + "/" + str(ugly_img))
                question = cv2.imread(current_img_path)
                if not cv2.bitwise_xor(ugly, question).any():
                    print current_img_path
                    os.remove(current_img_path)
            except Exception as e:
                print str(e)



def resize_input_img(input_folder, resize_x, resize_y, output_folder):
    for img_file in os.listdir(input_folder):
        print img_file
        img = cv2.imread(input_folder + "/" + str(img_file))
        resized_img = cv2.resize(img, (resize_x,resize_y), cv2.IMREAD_GRAYSCALE)
        cv2.imwrite(output_folder + "/" + str(img_file), resized_img)


def create_bg(neg_img_dir):
    for img in os.listdir(neg_img_dir):
        line = neg_img_dir + "/" + img + "\n"
        with open ("bg.txt", "a") as f:
            f.write(line)
    f.close()


def create_samples(inp_dir, num):
    for file in os.listdir(inp_dir):
        cmd = "opencv_createsamples -img " + inp_dir + "/" + file +" -bg bg.txt -info positives/info" + file.split('.')[0] +".lst -pngoutput positives -maxxangle 0.5 -maxyangle 0.5 -maxzangle 0.5 -num " + num
        os.system(cmd)



def merge_info_lst():
    for infolst in os.listdir('positives'):
        if "info" in str(infolst):
            with open("positives/"+infolst) as f:
                with open("info.lst", "a") as f1:
                    for line in f:
                        f1.write(line)
            os.remove("positives/"+infolst)
    f1.close()
    f.close()
    os.system("mv info.lst positives/")


while True:
    os.system("clear")
    print "\t\tMain Menu"
    print "\t\t---------"
    print "\nOptions:-\n\n1. Download negative images from Image-net.org using URLs that contain their links\n2. Remove ugly images(in case you downloaded negative images from Image-net.org)\n3. Resize input images"
    print "4. Create positive images (samples) from negative and input images\n5. Start training Haar Cascades\n6. Cleanup all"

    choice = int(raw_input("\n\nChoice: "))

    if choice == 1:
        os.system("clear")
        print "Download negative images from Image-net.org"
        print "-------------------------------------------\n"
        url = str(raw_input("Enter the URL that contains the download links (should look like http://image-net.org/api/text/imagenet.synset.geturls?wnid=n03642806): "))
        download_folder = "negatives"
        if not os.path.isdir(download_folder):
            os.makedirs(download_folder)
        print "\n\nDownloading....\n\n"
        get_neg_images(url, download_folder)
        raw_input("Press ENTER to continue...")

    elif choice == 2:
        os.system("clear")
        print "Remove ugly negative images"
        print "---------------------------\n"
        ugly_folder = "uglies"
        download_folder = "negatives"
        if not os.path.isdir(ugly_folder):
            os.makedirs(ugly_folder)
        raw_input("Put the one of each ugly images in the " + ugly_folder + " folder and press ENTER....")
        neg_image_folder = "negatives"
        remove_ugly(ugly_folder, neg_image_folder)
        raw_input("Removed. Press ENTER to continue...")

    elif choice == 3:
        os.system("clear")
        print "Resize the input images"
        print "-----------------------\n"
        input_img_dir = "input_images"
        output_img_dir = "input_resized_images"
        if not os.path.isdir(output_img_dir):
            os.makedirs(output_img_dir)
        resize_x = int(raw_input("Enter the resize dimension in x-axis (recommended 50): "))
        resize_y = int(raw_input("Enter the resize dimension in y-axis (recommended 50): "))
        resize_input_img(input_img_dir, resize_x, resize_y, output_img_dir)
        raw_input("Press ENTER to continue...")

    elif choice == 4:
        os.system("clear")
        print "Create positive images(samples) from negatives and the input images"
        print "----------------------------------------------------------\n"
        neg_img_dir = "negatives"
        print "Creating bg.txt...."
        create_bg(neg_img_dir)
        input_img_dir = "input_resized_images"
        pics = len(os.listdir(input_img_dir)) * len(os.listdir(neg_img_dir)) * 100
        create_samples(input_img_dir, str(pics))
        print "\n\nMerging every info files into 1 info.lst"
        merge_info_lst()
        raw_input("Press ENTER to continue...")

    elif choice == 5:
    	os.system("clear")
    	print "Train Haar Cascades"
    	print "-------------------\n"
    	print "Creating a vector file for the positive images(samples)....\n"
    	num = len(os.listdir('positives'))
    	cmd = "opencv_createsamples -info positives/info.lst -num " + str(num-1) + " -w 25 -h 25 -vec positives.vec"
        os.system(cmd)
        print "\npositives.vec created.\n"
        print "Training cascades..."
        print "\nThe next 2 inputs determine the amount of time that will be taken to create the cascade file.\nNormally it is better to use 3000 positive images and 1500 negative images i.e 2:1 ratio.\nTry not entering a large number as the time taken will increase exponentially"
        print "Also the number of stages is important.\nBetter keep it between 10-13\n\n"

        print "Number of positive samples available " + str(len(os.listdir('positives')))
        print "Number of negative samples available " + str(len(os.listdir('negatives'))) + "\n"

        pos = raw_input("Enter number of positive samples you want to use for training: ")
        neg = raw_input("Enter number of negative samples you want to use for training: ")
        num = raw_input("Enter number of stages: ")
        if not os.path.isdir("output_cascade"):
        	os.makedirs("output_cascade")
        cmd = "opencv_traincascade -data output_cascade -vec positives.vec -bg bg.txt -numPos " + pos + " -numNeg " + neg + " -numStages " + num + " -w 25 -h 25"
        os.system(cmd)
        raw_input("Press ENTER to continue...")

    elif choice == 6:
    	os.system("clear")
    	print "Cleanup all"
    	print "-----------\n"
    	print "WARNING: This will cleanup the following:-\ninput_images folder\ninput_resized_images folder\nbg.txt\npositives folder\npositive.vec file\nuglies folder\n"
    	c = raw_input("Are you sure to continue?(y/n): ")
    	if c == "y" or c == "Y":
    		os.system("rm -rf input_images input_resized_images positives uglies bg.txt positives.vec")
    	elif c == "n" or c == "N":
    		continue

    else:
    	print "Wrong choice..."
