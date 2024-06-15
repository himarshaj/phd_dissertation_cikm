import requests
import csv
import sys
import re
from datetime import datetime
from datetime import timedelta
import os

def extract_captions(url):
	response = requests.get(url)
	if response.status_code == 200:
		# print(type(response.text))
		return response.text
	else:
		print(f"Failed to fetch captions from {url}")
		return None

def format_time(time_str):
	hours, minutes, seconds, milliseconds = time_str.split(':')
	formatted_time = datetime.strptime(f"{hours}:{minutes}:{seconds}:{milliseconds}", "%H:%M:%S:%f").time()

	# formatted_time = "{:02d}:{:02d}:{:02d}.{}".format(int(hours), int(minutes), int(seconds), milliseconds)
	return formatted_time

def add_times(time1, time2):
	# print("time1.microsecond: ",time1.microsecond)
	# print("time2.microsecond: ",time2.microsecond)

	# print("time1.millisecond : ",time1.microsecond/1000)
	# print("time2.millisecond : ",time2.microsecond/1000)
	# Convert time objects to timedelta objects
	timedelta1 = timedelta(hours=time1.hour, minutes=time1.minute, seconds=time1.second, milliseconds=time1.microsecond/1000)
	timedelta2 = timedelta(hours=time2.hour, minutes=time2.minute, seconds=time2.second, milliseconds=time2.microsecond/1000)

	# print(timedelta1 , timedelta2)
	# Add the timedelta objects
	total_timedelta = timedelta1 + timedelta2

	# Convert the total timedelta back to a time object
	total_time = (datetime.min + total_timedelta).time()
	total_time_with_ms = total_time.strftime('%H:%M:%S.%f')[:-3]

	# print("total_time : ",total_time_with_ms)
	return total_time_with_ms

def parse_captions(captions, csv_writer, clip_start_time):
	format_str = "%H:%M:%S,%f"
	# sss_min = str(start_min)
	# print(type(sss_min))
	# ssss_min = datetime.strptime(sss_min,format_str).time()
	# print(ssss_time)
	if captions:

		blocks = re.split(r'\n\s*\n', captions.strip())
		# print(blocks)

		# with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
			# csv_writer = csv.writer(csvfile)

			# Write header to the CSV file
			# csv_writer.writerow(['start_time', 'end_time', 'captions'])

		for block in blocks:
			# print(block)
			lines = block.strip().split('\n')
			time_match = re.match(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})', lines[1])
			start_time, end_time = time_match.groups() if time_match else ('', '')
			s_time = start_time.replace(',',':')
			e_time = end_time.replace(',',':')
			s_time = format_time(s_time)
			e_time = format_time(e_time)
			
			# print(s_time)
			# print(e_time)

			caption = ' '.join(line.strip() for line in lines[2:])

			adjusted_start_time = add_times(clip_start_time, s_time) 

			adjusted_end_time = add_times(clip_start_time, e_time) 
			
			# print(adjusted_start_time)
			# print(adjusted_end_time)
			
			# s_time = datetime.strptime(start_time,format_str).time()
			# e_time = datetime.strptime(end_time,format_str).time()


			# Write the row with custom formatting for quotes
			csv_writer.writerow([adjusted_start_time, adjusted_end_time, f"'{caption}'"])

			# Flush the buffer to ensure immediate writing
			csvfile.flush()
			# break
	else:
		print("no captions")

def main(csvfile,base_url):
	# if len(sys.argv) != 2:
	# 	print("Usage: python3 extract_captions.py <url>")
	# 	sys.exit(1)

	# base_url = sys.argv[1]

	for start_time in range(0, 3601, 60):
		url = f"{base_url}{start_time}/{start_time+60}"
		print(url)
		captions = extract_captions(url)

		# formatted_time1 = "{:02d}:{:02d}:{:02d}:{:03d}".format(int(00), int(00), int(start_time), int(000))
		# print(formatted_time1)
		duration = timedelta(seconds=start_time)
		base_time = datetime.strptime('00:00:00', '%H:%M:%S')
		clip_start_time = base_time + duration


		parse_captions(captions, csv_writer, clip_start_time.time())
		# break

if __name__ == "__main__":
	##Hannity
	# base_url = "https://archive.org/download/FOXNEWSW_20230919_010000_Hannity/FOXNEWSW_20230919_010000_Hannity.align.srt?t="
	
	##Gutfeld  
	# base_url = "https://archive.org/download/FOXNEWSW_20230919_020000_Gutfeld/FOXNEWSW_20230919_020000_Gutfeld.align.srt?t="
	base_url = "https://archive.org/download/MSNBCW_20230808_010000_The_Rachel_Maddow_Show/MSNBCW_20230808_010000_The_Rachel_Maddow_Show.align.srt?t="


	##Jesse_Watters_Primetime  
	# base_url = "https://archive.org/download/FOXNEWSW_20230919_000000_Jesse_Watters_Primetime/FOXNEWSW_20230919_000000_Jesse_Watters_Primetime.align.srt?t="
	episode = base_url.split("/")[4]
	# print(episode)

	output_file = f"{episode}_captions.csv"

	if os.path.exists(output_file):
		if os.path.getsize(output_file) == 0:
			pass
		else:
			print(f"Output file '{output_file}' already exists. Exiting.")
			exit()

	with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
		csv_writer = csv.writer(csvfile)

		# Write header to the CSV file
		csv_writer.writerow(['start_time', 'end_time', 'captions'])


		main(csv_writer,base_url)
