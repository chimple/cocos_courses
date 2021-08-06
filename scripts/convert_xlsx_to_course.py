from glob import glob
import os
import json
import sys
import os.path
import argparse
import pathlib
import shutil
from openpyxl import load_workbook

parser = argparse.ArgumentParser()
parser.add_argument("course_id", help="Course name - en, hi")
parser.add_argument("course_name", help="Course name - English, Maths")
parser.add_argument("course_lang", help="Course lang - en, hi")
parser.add_argument("course_type", help="Course type - literacy, maths")
parser.add_argument("xlsx", help="XLSX file")
parser.add_argument("dir", help="Course directory")
parser.add_argument("old_dir", help="Old v1 Course directory which has images")
args = parser.parse_args()

#python export_xlsx_to_course.py maths Maths en maths ~/Downloads/Maths1218.xlsx ~/dev/chimple/courses/assets ~/dev/chimple/bahama/content/courses/en-maths

def write_json(filename, json_object, compact=True):
	dirname = os.path.dirname(filename)
	pathlib.Path(dirname).mkdir(parents=True, exist_ok=True)
	with open(filename, "w") as file:
		if compact:
			json_str = json.dumps(json_object, ensure_ascii=False, separators=(',', ':'))
			json_str = json_str.replace('],[','],\n  [')
			json_str = json_str.replace(']]',']\n]')
			json_str = json_str.replace('[[','[\n  [')
		else:
			json_str = json.dumps(json_object, ensure_ascii=False, sort_keys=True, indent=2)
		file.write(json_str)

def cell_value(cell):
	if cell.is_date:
		print('date: ' + cell_value(cell))
	if isinstance(cell.value, float):
		return str(int(cell.value))
	return str(cell.value).strip()

course = []
quiz = False

wb = load_workbook(filename = args.xlsx)
ws = wb['final']
skip = True
rownum = 0
for row in ws:
	rownum += 1
	if skip:
		skip = False
		continue
	print(rownum)
	if row[0].value is not None and row[0].value.strip() != '':
		name = cell_value(row[0])
		if name == 'quiz':
			chapter_id = args.course_id + '_quiz'
			quiz = True
		else:
			chapter_seq = len(course)
			if quiz:
				chapter_seq -= 1
			chapter_id = args.course_id + '{:02d}'.format(chapter_seq)
		course.append({
			"id": chapter_id,
			"name": name,
			"image": chapter_id + ".png",
			"lessons": []			
		})
	elif row[1].value is not None:
		if chapter_id == args.course_id + 'quiz':
			lesson_id = args.course_id + row[1].value
		else:
			lesson_id = chapter_id + '{:02d}'.format(len(course[-1]["lessons"]))
		course[-1]["lessons"].append({
			"id": lesson_id,
			"name": cell_value(row[1]),
			"image": lesson_id + ".png",
			"rows": []
		})
	elif row[2].value is not None:
		# print(row[2].value + ' ' + row[2].data_type)
		detail = []
		for cell in row:
			if cell.value is not None:
				detail.append(cell_value(cell))
				# print(type(cell.value))
				# print(str(cell.value) + ' ' + cell.data_type)
			else:
				detail.append("")
		res = [x for n, x in enumerate(detail) if any(y != "" for y in detail[n:])]
		res[0] = res[2]
		res[1] = "1"
		res[2] = "Description"
		course[-1]["lessons"][-1]["rows"].append(res)
# print(json.dumps(course, sort_keys=True, indent=2))
# pathlib.Path(args.dir + "/output/" + args.course_id + "/res/icons/").mkdir(parents=True, exist_ok=True)
for chapter in course:
	# shutil.copyfile(args.dir + "/common/res/icons/icon.png", args.dir + "/output/" + args.course_id + "/res/icons/" + chapter["id"] + ".png") 
	for lesson in chapter["lessons"]:
		# shutil.copyfile(args.dir + "/common/res/icons/icon.png", args.dir + "/output/" + args.course_id + "/res/icons/" + lesson["id"] + ".png") 
		for row in lesson["rows"]:
			game_name = row[0]
			if(game_name == 'quizliteracy'):
				game_name = 'eggquizliteracy'
			for index, item in enumerate(row):
				try:
					basename = os.path.basename(item)
					# if item.endswith(".png") or item.endswith(".jpg"):
					# 	to_file = args.dir + "/course-" + args.course_id + "/" + lesson["id"] + "/res/" + basename
					# 	to_dir = os.path.dirname(to_file)
					# 	pathlib.Path(to_dir).mkdir(parents=True, exist_ok=True)
					# 	shutil.copyfile(args.old_dir + "/" + game_name + "/res/image/" + item, to_file)
					# 	row[index]=basename 
					# if (args.course_id != 'maths') and (item.endswith(".mp3") or item.endswith(".m4a")):
					# 	to_file = args.dir + "/output/" + lesson["id"] + "/res/" + item
					# 	to_dir = os.path.dirname(to_file)
					# 	pathlib.Path(to_dir).mkdir(parents=True, exist_ok=True)
					# 	shutil.copyfile(args.old_dir + "/" + game_name + "/res/sound/" + item, to_file) 
					# 	row[index]=basename 
				except Exception as inst:
					print(inst)
		write_json(args.dir +"/course-" + args.course_id + "/" + lesson["id"] + "/res/" + lesson["id"] + ".json", {"rows" : lesson["rows"]}, False)
		del lesson["rows"]
write_json(args.dir + "/" + args.course_id+"/res/course.json", {
	"id": args.course_id,
	"name": args.course_name,
	"lang": args.course_lang,
	"type": args.course_type,
	"chapters":  course } , False)
