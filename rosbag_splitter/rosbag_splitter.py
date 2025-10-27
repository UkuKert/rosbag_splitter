import logging

import rosbag
import rospy
import yaml
from tqdm import tqdm

logger = logging.getLogger(__name__)


def split_rosbag(input_bag_path, output_bag_path, begin_time, end_time):
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
