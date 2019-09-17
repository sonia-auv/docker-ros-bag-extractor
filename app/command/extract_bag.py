import os
import sys
import logging
import uuid
from glob import glob


import cv2
import rosbag
from cv_bridge import CvBridge


def __get_bags_name(bag_folder, with_extension=False):
    if os.path.isdir(bag_folder):
        filenames = next(os.walk(bag_folder))[2]
        if with_extension:
            bag_names = [f for f in filenames if len(f) > 0]
        else:
            bag_names = [f.split(".")[0] for f in filenames if len(f.split(".")[0]) > 0]

        if len(bag_names) < 1:
            logging.warning("Exiting...bag folder contains no bag to extract")
            sys.exit(os.EX_OSERR)

        return bag_names

    logging.warning("Exiting...provided bag folder does not exist")
    sys.exit(os.EX_OSERR)


def __create_output_dirs(bag_folder, output_folder):
    bag_names = __get_bags_name(bag_folder)

    folders = [os.path.join(output_folder, bag) for bag in bag_names]

    for folder in folders:
        os.mkdir(folder)


def __generate_image_name(bag_file):
    uuid_name = str(uuid.uuid1())

    bag_filename = bag_file.split(".")[0]

    uuid_formated_name = "frame_{}_{}.jpg".format(bag_filename, uuid_name)

    return uuid_formated_name


def to_images(bag_folder, output_folder, topics):

    __create_output_dirs(bag_folder, output_folder)

    bags = glob("{}/*.bag".format(bag_folder))

    for bag_file in bags:
        for topic in topics:
            with rosbag.Bag(bag_file, "r") as bag:
                logging.info("Extracting images from {} on topic {}".format(bag_file, topic))
                for topic, msg, _ in bag.read_messages(topics=[topic]):

                    img_name = __generate_image_name(bag_file)

                    extraction_path = os.path.join(output_folder, bag_file, img_name)

                    cv_img = CvBridge.compressed_imgmsg_to_cv2(msg, desired_encoding="passthrough")
                    cv2.imwrite(extraction_path, cv_img)
                    logging.info("Extracted image {} to {}".format(img_name, extraction_path))
