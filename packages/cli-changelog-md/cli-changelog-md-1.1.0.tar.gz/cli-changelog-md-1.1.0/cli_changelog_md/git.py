import configparser
import os


def get_branch(git_path):
    return open(os.path.join(git_path, 'HEAD'), 'r').read().split('heads/')[-1]


def get_url(git_path):
    config_path = os.path.join(git_path, 'config')
    config = configparser.ConfigParser()
    config.read(config_path)
    full_url = config.get('remote "origin"', "url")
    return f'https://{full_url.split("@")[-1].replace(":", "/")}'
