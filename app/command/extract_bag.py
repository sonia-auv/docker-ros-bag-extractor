import os
import shutil
import sys
import uuid
from glob import glob

import cv2

import rosbag
from cv_bridge import CvBridge


def __get_filename(filepath):
    filepath = os.path.basename(filepath)
    filename = filepath.split(".")[0]

    return filename


def __get_bags_name(bag_folder):
    if os.path.isdir(bag_folder):
        filenames = next(os.walk(bag_folder))[2]
        bag_names = [f.split(".")[0] for f in filenames if len(f.split(".")[0]) > 0]

        if len(bag_names) < 1:
            raise SystemExit("[ERROR]:Exiting...bag folder contains no bag to extract")
        return bag_names
    raise SystemExit("[ERROR]:[Exiting...provided bag folder does not exist")


def __create_output_dirs(bag_folder, output_folder):
    bag_names = __get_bags_name(bag_folder)

    folders = [os.path.join(output_folder, bag) for bag in bag_names]

    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)
        os.mkdir(folder)
        print(f"[INFO]:Created folder {folder}")


def __generate_image_name(bag_file):
    uuid_name = str(uuid.uuid1())

    bag_filename = __get_filename(bag_file)

    uuid_formated_name = "frame_{}_{}.jpg".format(bag_filename, uuid_name)

    return uuid_formated_name


def to_images(bag_folder, output_folder, topics):

    __create_output_dirs(bag_folder, output_folder)

    bags = glob("{}/*.bag".format(bag_folder))

    bridge = CvBridge()

    for bag_file in bags:
        for topic in topics:
            with rosbag.Bag(bag_file, "r") as bag:
                print("[INFO]:Extracting images from {} on topic {}".format(bag_file, topic))
                for topic, msg, _ in bag.read_messages(topics=[topic]):

                    img_filename_with_ext = __generate_image_name(bag_file)
                    bag_filename = __get_filename(bag_file)

                    extraction_path = os.path.join(
                        output_folder, bag_filename, img_filename_with_ext
                    )

                    cv_img = bridge.compressed_imgmsg_to_cv2(msg, desired_encoding="passthrough")

                    img_saved = cv2.imwrite(extraction_path, cv_img)

                    if not img_saved:
                        raise SystemExit(
                            f"[ERROR]: An error occured while saving image file {extraction_path}"
                        )

                    print("[INFO]:Extracted image {} to {}".format(img_name, extraction_path))
