import argparse
import os

from command import extract_bag


BAGS_FOLDER = os.environ["BAGS_FOLDER"]
IMAGES_FOLDER = os.environ["IMAGES_FOLDER"]


def setup_cli():
    parser = argparse.ArgumentParser(
        description="A simple utility library to extract content of ROS bag"
    )

    parser.add_argument(
        "-m",
        "--media",
        type=str,
        choices=["image"],
        help="The type of content that will be extracted e.g : image",
        required=True,
    )
    parser.add_argument(
        "-t",
        "--topics",
        nargs="+",
        help="The topics from which content must be extracted",
        required=True,
    )

    return parser


def extract(media, topics):
    if media == "image":
        extract_bag.to_images(BAGS_FOLDER, IMAGES_FOLDER, topics)


if __name__ == "__main__":
    parser = setup_cli()
    parsed_args = parser.parse_args()

    extract(parsed_args.type, parsed_args.topics)
