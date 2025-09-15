import subprocess
import argparse
import os


def main():
    '''
    This script is for easy cutting of ROSBAGS

    Usage:
    $ rosbag_splitter.py -i  INPUT_ROSBAG_PATH.bag -o (Optional) OUTPUT_ROSBAG_FILE_NAME.bag -b BEGIN_TIME_IN_S -e (Optional) END_TIME_IN_S

    '''
    parser = argparse.ArgumentParser(
        description="This script is used for cutting a rosbag")
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument('-i', '--input_bag', type=str,
                          help="Path to bag to cut", required=True)
    required.add_argument('-e', '--end_time', type=float,
                          help="End time in seconds from begginning of bag", required=True)
    optional.add_argument('-o', '--output_bag', type=str, default="",
                          help="Specify output bag name. Path is the same as input path")
    optional.add_argument('-b', '--begin_time', type=float, default=0.0,
                          help="Starting time in seconds from beginning of bag, default is 0.0")
    args = parser.parse_args()

    input_bag_path = args.input_bag

    # Perform argument validity checks
    if not os.path.exists(input_bag_path):
        raise FileNotFoundError("The input rosbag could not be found")

    # Get the full path to the input file, because we want to save our bag to that dir
    output_dir = os.path.dirname(os.path.abspath(input_bag_path))+'/'

    # Output bag path name creation and validation
    if args.output_bag == "":
        output_bag = os.path.splitext(args.input_bag)[0]+"_cut.bag"
    elif not args.output_bag.endswith(".bag"):
        output_bag = output_dir + args.output_bag+".bag"
    else:
        output_bag = output_dir + args.output_bag

    begin_time = args.begin_time
    end_time = args.end_time

    if end_time <= begin_time:
        raise ValueError("End time cannot be smaller or equal to begin time")

    # Run the  command "rosbag info" to get the UNIX timestamp of the start time
    start_command = ['rosbag', 'info', '-y', '-k start', input_bag_path]
    start_time_of_bag = float(
        subprocess.check_output(start_command).decode('UTF-8'))

    # Generate the time filter of the rosbag
    cut_begin = start_time_of_bag+begin_time
    cut_end = start_time_of_bag + end_time
    time_filter = 't.to_sec() >= {0} and t.to_sec() <= {1}'.format(
        cut_begin, cut_end)
    print("Using Filter:", time_filter)
    print("Saving the cut bag as", output_bag)

    # Execute the filter on the rosbag
    filter_command = ['rosbag', 'filter',
                      input_bag_path, output_bag, time_filter]
    subprocess.run(filter_command)


if __name__ == "__main__":
    main()
