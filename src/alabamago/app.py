"""
Alabama GO
"""
import toga
import urllib.request
import json
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
		return [float(parts[0]), float(parts[1])]
	
	def say_hello(self, widget):
		# with httpx.Client() as client:
		# 	response = client.get("https://jsonplaceholder.typicode.com/posts/42")

		# payload = response.json()

		lat, long = self.get_location()

		self.main_window.info_dialog(
			"Location",
			f"{lat}, {long}"
		)


def main():
    return AlabamaGO()
