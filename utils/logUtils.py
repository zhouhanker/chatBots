import random

from utils import config


def log_warn_group_prefix():
	return random.choice(config.get_yaml()['msg_group_warn_prefix'])