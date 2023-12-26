"""
Alabama GO
"""
import toga
import urllib.request
import json
import math
import csv
import os
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class AlabamaGO(toga.App):

	def startup(self):
		main_box = toga.Box(style=Pack(direction=COLUMN))

		name_label = toga.Label(
			"Your name: ",
			style=Pack(padding=(0, 5))
		)
		self.name_input = toga.TextInput(style=Pack(flex=1))

		name_box = toga.Box(style=Pack(direction=ROW, padding=5))
		name_box.add(name_label)
		name_box.add(self.name_input)

		button = toga.Button(
			"Say Hello!",
			on_press=self.say_hello,
			style=Pack(padding=5)
		)

		main_box.add(name_box)
		main_box.add(button)

		self.main_window = toga.MainWindow(title=self.formal_name)
		self.main_window.content = main_box
		self.main_window.show()

	def get_location(self):
		url = 'https://ipinfo.io/json'
		request = urllib.request.Request(url)
		response = urllib.request.urlopen(request)
		data = json.load(response)
		parts = data["loc"].split(",")
		return (float(parts[0]), float(parts[1]))
	
	def say_hello(self, widget):
		lat, long = self.get_location()
		self.get_nearby_monuments((lat, long))
		self.main_window.info_dialog(
			"Location",
			f"{lat}, {long}"
		)

	def get_nearby_monuments(self, my_coord, limit=10):
		dist_list = []
		monument_file = os.path.join(toga.App.app.paths.app, "monuments.csv")
		with open(monument_file, 'r') as csvfile:
			csvreader = csv.reader(csvfile)
			next(csvreader)
			for row in csvreader:
				monument_coord = (float(row[7]), float(row[8]))
				dist = haversine_distance(my_coord, monument_coord)
				dist_list.append({dist: row})
			dist_list = sorted(dist_list, key=lambda x: list(x.keys())[0])
			smallest_numbers = dist_list[:limit]
			print(smallest_numbers)
			return smallest_numbers
		
def haversine_distance(coord1, coord2):
	"""
	Calculate the Haversine distance between two GPS coordinates.

	Parameters:
	- coord1: Tuple of (latitude, longitude) for the first coordinate.
	- coord2: Tuple of (latitude, longitude) for the second coordinate.

	Returns:
	- Distance in kilometers.
	"""
	# Radius of the Earth in kilometers
	R = 6371.0

	# Convert latitude and longitude from degrees to radians
	lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
	lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])

	# Differences in coordinates
	dlat = lat2 - lat1
	dlon = lon2 - lon1

	# Haversine formula
	a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

	# Distance in kilometers
	distance = R * c

	return distance


def main():
	return AlabamaGO()
