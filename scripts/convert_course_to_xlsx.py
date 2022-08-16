# python convert_course_to_xlsx.py E:\sutara_projects\chimple2021\chimple\assets\courses\en\course-en E:\sutara_projects\chimple2021\chimple\assets\courses\en\en\res

from glob import glob
import json
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("course_dir", help="Course dir")
parser.add_argument("course_json", help="Course Json")
args = parser.parse_args()

data = []

print('args.course_json', args.course_json + '\course.json')
chapters = {}
with open(args.course_json + '\course.json', encoding='utf-8') as f:
    courseJsonData = json.load(f)
    for chapter in courseJsonData['chapters']:
        # print('\n' + chapter['id'])
        isChapterNameAdded = True
        for lesson in chapter['lessons']:
            if 'type' not in lesson.keys():
                # print(
                #     lesson['id'], args.course_dir + '/' + lesson['id'] +
                #     '/res/' + lesson['id'] + '.json')

                for json_file in glob(args.course_dir + '/' + lesson['id'] +
                                      '/res/' + lesson['id'] + '.json',
                                      recursive=True):
                    # Process each file here
                    print('json_file', json_file)
                    df = pd.read_json(json_file)
                    if isChapterNameAdded:
                        isChapterNameAdded = False
                        data.append([chapter['name']
                                     ])  # pass Chapter name here
                    data.append(['', lesson['name']])  #pass lesson Name here
                    for row in df['rows']:
                        # print(row)
                        r = ['', '']
                        for item in row:
                            # print(item)
                            r.append(item)
                        data.append(r)

                #Create a DataFrame:
                data_frames = pd.DataFrame(data)

print('data_frames', data_frames)
data_frames.to_excel('curriculum.xlsx', index=False)

# print('args.course_dir', args.course_dir)
# for json_file in glob(args.course_dir + '/**/*.json', recursive=True):
#     # print('json_file', json_file)
#     with open(json_file, 'r', encoding='utf-8') as json_f:
#         # print('json_f', json_f)
#         if len(json_f.readlines()) != 0:
#             json_f.seek(0)
#             lesson = json.load(json_f)
#             # print('lesson', lesson)
#             for row in lesson['rows']:
#                 # print('--------- for rows -----------------------')
#                 for item in row:
#                     # print(item)
#                     data_frames.append(lesson)
#                 # print('data_frames', data_frames)
#         json_f.close()

# print('data_frames', data_frames)
# pd.concat(data_frames).to_csv("data.csv")