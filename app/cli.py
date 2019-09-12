import argparse

from command import extract_bag


def setup_cli():
    parser = argparse.ArgumentParser(description='A simple utility library to extract content of ROS bag')

    parser.add_argument('-b',
                        '--bag-folder',
                        type=str,
                        help="The path of the folder containing the bags to be extracted",
                        required=True)

    parser.add_argument('-o',
                        '--output-folder',
                        type=str,
                        help="The path of the folder where the extracted files will be located",
                        required=True)
    parser.add_argument(
                        '-t',
                        '--topics',
                        nargs='+',
                        help="The topics from which content must be extracted",
                        required=True)

    return parser


def extract(bag_folder, output_folder, topics):
    extract_bag.to_images(bag_folder, output_folder, topics)

if __name__ == "__main__":
    parser = setup_cli()
    parsed_args = parser.parse_args()

    extract(parsed_args.bag_folder, parsed_args.output_folder, parsed_args.topics)
