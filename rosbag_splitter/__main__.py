import argparse
import logging
import os
import sys

from rosbag_splitter import split_rosbag

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def parse_args() -> argparse.Namespace:
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


def validate_args(args: argparse.Namespace) -> bool:
    if not os.path.exists(args.input_bag):
        logger.error(f"The input rosbag at {args.input_bag} could not be found")
        return False
    if args.end_time <= args.begin_time:
        logger.error("End time cannot be smaller or equal to begin time")
        return False
    return True


def main():
    args = parse_args()
    if not validate_args(args):
        logger.error("Input arguments incorrect. Cannot handle this state, exiting...")
        sys.exit(1)
    # Get the full path to the input file, because we want to save our bag to that dir
    output_dir = os.path.dirname(os.path.abspath(args.input_bag)) + "/"
    # Output bag path name creation
    if args.output_bag == "":
        output_bag_path = os.path.splitext(args.input_bag)[0] + "_cut.bag"
    elif not args.output_bag.endswith(".bag"):
        output_bag_path = output_dir + args.output_bag + ".bag"
    else:
        output_bag_path = output_dir + args.output_bag
    try:
        split_rosbag(args.input_bag, output_bag_path, args.begin_time, args.end_time)
    except Exception as e:
        logger.error(f"Failed to split bag: {e}")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
