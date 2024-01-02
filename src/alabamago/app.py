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
from datetime import datetime

scans = []

class AlabamaGO(toga.App):

	def create_logo_box(self):
		box = toga.Box(
			style=Pack(
				padding=10,
				alignment=CENTER,
				direction=COLUMN,
			)
		)
		image_from_path = toga.Image("resources/alabama_go_logo.png")
		box.add(
			toga.ImageView(
				image_from_path,
				style=Pack(
					width=187.5,
					height=105.46875
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
		self.main_box.remove(self.list_box)
		lat, long = self.get_location()
		nearby = self.get_nearby_monuments((lat, long))
		self.list_box = self.create_list_box(nearby)
		self.main_box.add(self.list_box)

	def create_list_box(self, monuments):
		for monument in monuments:
			monument["dist"] = round(monument["dist"], 2)
		list_box = toga.DetailedList(
			data = [
				{
					"icon": toga.Icon(f"resources/icons/map_icon_{monument['data'][0]}.png"),
					"title": monument["data"][2],
					"subtitle": str(monument["dist"]) + " km",
					"id": monument["data"][0]
				}
				for monument in monuments
			],
			on_select=self.on_select_handler,
			style=Pack(flex=1)
		)
		return list_box
	
	def on_select_handler(self, widget):
		row = widget.selection
		print(getattr(row, "title", ""))
		details = self.get_monument_id(getattr(row, "id"))
		self.create_detail_page(details)
        # self.label.text = (
        #     f"Bee is {getattr(row, 'title', '')} in {getattr(row, 'subtitle', '')}"
        #     if row is not None
        #     else "No row selected"
        # )

	def save_scan(self, row):
		scans.append({
			"id": row[0],
			"datetime": datetime.utcnow()
		})

	def create_detail_page(self, row):
		self.save_scan(row)
		back_button = toga.Button("< Back", on_press=self.main_page, style=Pack(flex=1, padding_right=500, padding_left=10))
		f = open(os.path.join(toga.App.app.paths.app, ".env"), "r")
		google_key = f.read().strip()
		geoview = toga.WebView(
			url=f"https://maps.googleapis.com/maps/api/staticmap?center={row[7]},{row[8]}&markers={row[7]},{row[8]}&zoom=19&size=380x315&key={google_key}",
			style=Pack(flex=1),
		)
		image_view = toga.WebView(
			url=row[16],
			style=Pack(flex=1),
		)
		scan_view = toga.WebView(
			url=f"https://shielded-harbor-81806-544e6cbb1d40.herokuapp.com/scan/{row[0]}",
			style=Pack(height=70),
		)
		border = toga.Box(
			style=Pack(height=20, background_color="gray")
		)
		self.main_box = toga.Box(
			style=Pack(direction=COLUMN),
			children=[back_button, image_view, border, geoview, scan_view]
		)
		self.main_window = toga.MainWindow(title=self.formal_name)
		self.main_window.content = self.main_box
		self.main_window.show()

	def startup(self):
		self.main_page(None)

	def main_page(self, _):
		history_button = toga.Button("📖", on_press=self.history_page, style=Pack(flex=1, padding_right=500, padding_left=30, font_size=20))
		self.logo_box = self.create_logo_box()
		self.search_box = self.create_search_button()
		self.list_box = toga.Box()
		self.main_box = toga.Box(
			style=Pack(direction=COLUMN),
			children=[history_button, self.logo_box, self.search_box, self.list_box]
		)

		self.main_window = toga.MainWindow(title=self.formal_name)
		self.main_window.content = self.main_box
		self.main_window.show()

	def back_to_main_page(self, _):
		self.main_page(None)
		self.search_nearby(None)

	def history_page(self, _):
		back_button = toga.Button("< Back", on_press=self.main_page, style=Pack(flex=1, padding_right=500, padding_left=10))
		title = toga.Label("Your History", style=Pack(flex=1, padding=10, font_size=30, text_align=CENTER))
		if len(scans) == 0:
			detail_list = toga.Label("You have no scans. Go search and scan stuff!", style=Pack(flex=1, padding=10, text_align=CENTER))
		else:
			detail_list = toga.DetailedList(
			data = [
				{
					"icon": toga.Icon(f"resources/icons/map_icon_{scan['id']}.png"),
					"title": self.get_monument_id(scan["id"])[2],
					"subtitle": scan["datetime"],
					"id": scan["id"]
				}
				for scan in scans
			],
			on_select=self.on_select_handler,
			style=Pack(flex=1)
		)
		self.main_box = toga.Box(
			style=Pack(direction=COLUMN),
			children=[back_button, title, detail_list]
		)

		self.main_window = toga.MainWindow(title=self.formal_name)
		self.main_window.content = self.main_box
		self.main_window.show()	

	def get_location(self):
		url = 'http://ipinfo.io/json'
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
		
	def get_monument_id(self, id):
		monument_file = os.path.join(toga.App.app.paths.app, "monuments.csv")
		with open(monument_file, 'r') as csvfile:
			csvreader = csv.reader(csvfile)
			next(csvreader)
			for row in csvreader:
				if row[0] == id:
					return row
		
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
