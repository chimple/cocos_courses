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
parser.add_argument("--audio", action='store_true', help="Process audio")
parser.add_argument("--images", action='store_true', help="Process images")
parser.add_argument("--overwrite", action='store_true', help="overwrite existing files (default: do not overwrite)")
args = parser.parse_args()

available_images = {}
if args.images:
    for filename in glob(args.asset_dir + '/images/*'):
        available_images[filename] = 0

available_audio = {}
if args.audio:
    for filename in glob(args.asset_dir + '/audio/*'):
        available_audio[filename] = 0

for json_file in glob(args.course_dir + '/**/*.json', recursive=True):
    with open(json_file) as json_f:
        lesson = json.load(json_f)
        for row in lesson['rows']:
            for item in row:
                if args.audio and item.endswith('.mp3'):
                    if args.overwrite or not os.path.isfile(os.path.dirname(json_file) + '/' + item):
                        if os.path.isfile(args.asset_dir + '/audio/' + item):
                            shutil.copyfile(args.asset_dir + '/audio/' + item, os.path.dirname(json_file) + '/' + item)
                            available_audio[args.asset_dir + '/audio/' + item] = 1
                        else:
                            if not os.path.isfile(os.path.dirname(json_file) + '/' + item):
                                print('No audio file: '+item)
                if args.images and (item.endswith('.png') or item.endswith('.jpg')):
                    if args.overwrite or not os.path.isfile(os.path.dirname(json_file) + '/' + item):
                        if os.path.isfile(args.asset_dir + '/images/' + item):
                            shutil.copyfile(args.asset_dir + '/images/' + item, os.path.dirname(json_file) + '/' + item)
                            available_images[args.asset_dir + '/images/' + item] = 1
                        else:
                            if not os.path.isfile(os.path.dirname(json_file) + '/' + item): 
                                print('No image file: '+item)
if args.audio:
    new_dict = {k: v for k, v in available_audio.items() if v == 0}
    print(new_dict)

if args.images:
    new_dict = {k: v for k, v in available_images.items() if v == 0}
    print(new_dict)    