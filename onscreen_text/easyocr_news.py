#!/usr/bin/env python3

import easyocr
import time
import csv
import os

if __name__ == "__main__":
	# Simple image to string
	start_time = time.time()
	reader = easyocr.Reader(['en'], gpu=False) # this needs to run only once to load the model into memory
	folder_path = 'MSNBCW_20230808_010000_The_Rachel_Maddow_Show' #'test' #'FOXNEWSW_20230919_000000_Jesse_Watters_Primetime'
	# folder_path = 'ErrorImages'
	# output_file= 'ErrorImages.tsv'
	output_file = 'MSNBCW_20230808_010000_The_Rachel_Maddow_Show.tsv' #'test.tsv'#'FOXNEWSW_20230919_000000_Jesse_Watters_Primetime_OCR.tsv'
	with open(output_file, 'w', newline='', encoding='utf-8') as tsvfile:
		writer = csv.writer(tsvfile, delimiter='\t')
		writer.writerow(['Image', 'OCR'])

		for filename in os.listdir(folder_path):
			if filename.endswith(('.jpg', '.jpeg', '.png')):
				image_path = os.path.join(folder_path, filename)

				# Perform OCR on each image
				ocr_text = reader.readtext(image_path, detail = 0)

				# Write the results to the TSV file
				print(filename)
				writer.writerow([filename, ocr_text])
			#break

	end_time = time.time()
	duration = end_time - start_time

	print(f"OCR completed for images in '{folder_path}'. Results saved in '{output_file}'")

	print(f"Total time taken: {duration:.2f} seconds")

	# print(pytesseract.image_to_string(Image.open('test3.jpg')))