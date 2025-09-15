#!/usr/bin/env python3
import argparse
import logging
import os

import rosbag
import rospy
import yaml
from tqdm import tqdm

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def parse_args():
    parser = argparse.ArgumentParser(description="This script is used for cutting a rosbag")
    parser._action_groups.pop()
    required = parser.add_argument_group("required arguments")
    optional = parser.add_argument_group("optional arguments")

    required.add_argument("-i", "--input-bag", type=str, help="Path to bag to cut", required=True)
    required.add_argument(
        "-e", "--end-time", type=float, help="End time in seconds from begginning of bag", required=True
    )
    optional.add_argument("-o", "--output-bag", type=str, default="", help="Specify output bag name.")
    optional.add_argument(
        "-b",
        "--begin-time",
        type=float,
        default=0.0,
        help="Starting time in seconds from beginning of bag, defaults to 0.0",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    input_bag_path = args.input_bag

    # Perform argument validity checks
    if not os.path.exists(input_bag_path):
        raise FileNotFoundError("The input rosbag could not be found")

    # Get the full path to the input file, because we want to save our bag to that dir
    output_dir = os.path.dirname(os.path.abspath(input_bag_path)) + "/"

    # Output bag path name creation and validation
    if args.output_bag == "":
        output_bag_path = os.path.splitext(args.input_bag)[0] + "_cut.bag"
    elif not args.output_bag.endswith(".bag"):
        output_bag_path = output_dir + args.output_bag + ".bag"
    else:
        output_bag_path = output_dir + args.output_bag

    begin_time = args.begin_time
    end_time = args.end_time

    if end_time <= begin_time:
        raise ValueError("End time cannot be smaller or equal to begin time")

    logger.info(f"Reading input bag {input_bag_path}")
    with rosbag.Bag(input_bag_path, "r") as input_bag:
        rosbag_info = yaml.safe_load(input_bag._get_yaml_info())
        start_time_of_bag = rosbag_info["start"]
        cut_begin = rospy.Time.from_sec(start_time_of_bag + begin_time)
        cut_end = rospy.Time.from_sec(start_time_of_bag + end_time)

        with rosbag.Bag(output_bag_path, "w") as output_bag:
            logger.info(f"Saving the cut bag as {output_bag_path}")
            for topic, msg, t in tqdm(input_bag.read_messages(start_time=cut_begin, end_time=cut_end)):
                output_bag.write(topic, msg, t)
