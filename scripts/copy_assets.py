"""Parses course json and copies any file that doesnt exist
"""
import argparse
from glob import glob
import json
import os.path
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("course_dir", help="Course dir")
parser.add_argument("asset_dir", help="Asset dir")
args = parser.parse_args()

for json_file in glob(args.course_dir + '/**/*.json', recursive=True):
    with open(json_file) as json_f:
        lesson = json.load(json_f)
        for row in lesson['rows']:
            for item in row:
                if item.endswith('.mp3') and not os.path.isfile(os.path.dirname(json_file) + '/' + item):
                    if os.path.isfile(args.asset_dir + '/' + item):
                        shutil.copyfile(args.asset_dir + '/' + item, os.path.dirname(json_file) + '/' + item)
                    else:
                        print('No file: '+item)