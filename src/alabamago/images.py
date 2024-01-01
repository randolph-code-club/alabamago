import toga
import os
import csv

dir_path = os.path.dirname(os.path.realpath(__file__))

monument_file = os.path.join(dir_path, "monuments.csv")
with open(monument_file, 'r') as csvfile:
	csvreader = csv.reader(csvfile)
	next(csvreader)
	for row in csvreader:
		monument_coord = (float(row[7]), float(row[8]))
		f = open(os.path.join(dir_path, ".env"), "r")
		google_key = f.read().strip()
		image = f"https://maps.googleapis.com/maps/api/staticmap?center={row[7]},{row[8]}&markers={row[7]},{row[8]}&zoom=14&size=100x100&key={google_key}"
		print(image)