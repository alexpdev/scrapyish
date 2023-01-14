import os
import argparse
from scrapyish.crawler import Crawler


def crawl_command(args: argparse.Namespace):
    pass


def build_project(args: argparse.Namespace):
    path = args.project_name
    if os.path.exists(path):
        raise FileExistsError
    os.mkdir(path)
    
