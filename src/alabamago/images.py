import toga
import os
import csv
import requests

dir_path = os.path.dirname(os.path.realpath(__file__))

monument_file = os.path.join(dir_path, "monuments.csv")
with open(monument_file, 'r') as csvfile:
	csvreader = csv.reader(csvfile)
	next(csvreader)
	for row in csvreader:
		monument_coord = (float(row[7]), float(row[8]))
		f = open(os.path.join(dir_path, ".env"), "r")
		google_key = f.read().strip()
		image_url = f"https://maps.googleapis.com/maps/api/staticmap?center={row[7]},{row[8]}&markers={row[7]},{row[8]}&zoom=14&size=100x100&key={google_key}"
		response = requests.get(image_url, stream=True)
		file_path = os.path.join(dir_path, "resources", "icons", f"map_icon_{row[0]}.png")
		if response.status_code == 200:
			# Open a file in binary write mode and write the content of the response
			with open(file_path, 'wb') as file:
				for chunk in response.iter_content(chunk_size=128):
					file.write(chunk)
			print(f"Image downloaded successfully and saved to: {file_path}")
		else:
			print(f"Failed to download image. Status code: {response.status_code}")