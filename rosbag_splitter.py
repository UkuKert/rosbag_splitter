import subprocess
import sys
import argparse
import os
# Embag is a drop in replacement for rosbag with faster runtimes.
import embag as rosbag

# Test input bag: bags/_2022-05-26-16-27-52_1.bag

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This script is used for cutting a rosbag")
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument('-i', '--input_bag', type=str,
                          help="Path to bag to cut", required=True)
    required.add_argument('-e', '--end_time', type=float,
                          help="End time in seconds from begginning of bag", required=True)
    optional.add_argument('-o', '--output_bag', type=str, default="cut.bag",
                          help="Specify output bag path and name, default is in the same folder with suffix '_cut'")
    optional.add_argument('-b', '--begin_time', type=float, default=0.0,
                          help="Starting time in seconds from beginning of bag, default is 0.0")
    args = parser.parse_args()

    # We could probably do without the extra variable declaration
    input_bag_path = args.input_bag
    output_bag = args.output_bag
    begin_time = args.begin_time
    end_time = args.end_time

    # Perform argument validity checks

    if not os.path.exists(input_bag_path):
        raise FileNotFoundError("The input rosbag could not be found")

    if end_time <= begin_time:
        raise ValueError("End time cannot be smaller or equal to begin time")

    # Run the  command "rosbag info" to get the UNIX timestamp of the start time
    start_command = ['rosbag', 'info', '-y', '-k start', input_bag_path]
    start_time_of_bag = float(
        subprocess.check_output(start_command).decode('UTF-8'))

    cut_begin = start_time_of_bag+begin_time
    cut_end = cut_begin+end_time

    time_filter = 't.to_sec() >= {0} and t.to_sec() <= {1}'.format(
        cut_begin, cut_end)
    print(time_filter)
    filter_command = ['rosbag', 'filter',
                      input_bag_path, output_bag, time_filter]
    subprocess.run(filter_command)
