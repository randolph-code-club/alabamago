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
from toga.style.pack import COLUMN, ROW, CENTER


class AlabamaGO(toga.App):

	def create_logo_box(self):
		box = toga.Box(
			style=Pack(
				padding=10,
				alignment=CENTER,
				direction=COLUMN,
			)
		)
		image_from_path = toga.Image("resources/bama.png")
		box.add(
			toga.ImageView(
				image_from_path,
				style=Pack(
					width=50,
					height=50
				)
			)
		)
		return box
	
	def create_search_button(self):
		button1 = toga.Button(
			"Search Nearby",
			on_press=self.search_nearby,
			style=Pack(flex=1,font_size=30),
		)
		return toga.Box(
			style=Pack(direction=ROW),
			children=[button1],
		)

	def search_nearby(self, widget):
		self.list_box.parent.remove(self.list_box)
		lat, long = self.get_location()
		nearby = self.get_nearby_monuments((lat, long))
		self.list_box = self.create_list_box(nearby)
		self.main_box.add(self.list_box)

	def create_list_box(self, monuments):
		list_box = toga.DetailedList(
			data = [
				{
					"icon": toga.Icon("resources/bama.png"),
					"title": monument["dist"],
					"subtitle": monument["dist"]
				}
				for monument in monuments
			],
			on_select=self.on_select_handler,
			style=Pack(flex=1)
		)
		return list_box
	
	def on_select_handler(self, widget):
		pass

	def startup(self):
		self.logo_box = self.create_logo_box()
		self.search_box = self.create_search_button()
		self.list_box = toga.Box()
		self.main_box = toga.Box(
			style=Pack(direction=COLUMN),
			children=[self.logo_box, self.search_box, self.list_box]
		)

		self.main_window = toga.MainWindow(title=self.formal_name)
		self.main_window.content = self.main_box
		self.main_window.show()

	def get_location(self):
		url = 'https://ipinfo.io/json'
		request = urllib.request.Request(url)
		response = urllib.request.urlopen(request)
		data = json.load(response)
		parts = data["loc"].split(",")
		return (float(parts[0]), float(parts[1]))
	
	# def say_hello(self, widget):
	# 	lat, long = self.get_location()
	# 	self.get_nearby_monuments((lat, long))
	# 	self.main_window.info_dialog(
	# 		"Location",
	# 		f"{lat}, {long}"
	# 	)

	def get_nearby_monuments(self, my_coord, limit=10):
		dist_list = []
		monument_file = os.path.join(toga.App.app.paths.app, "monuments.csv")
		with open(monument_file, 'r') as csvfile:
			csvreader = csv.reader(csvfile)
			next(csvreader)
			for row in csvreader:
				monument_coord = (float(row[7]), float(row[8]))
				dist = haversine_distance(my_coord, monument_coord)
				dist_list.append({
					"dist": dist,
					"data": row
					}
				)
			dist_list = sorted(dist_list, key=lambda x: x["dist"])
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
