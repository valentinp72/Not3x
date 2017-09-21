# coding: utf-8

import xml.etree.ElementTree as ET
import os

tree = ET.parse('data.xml')
root = tree.getroot()


# Default location where projects and files will be located:
globalPath = "output/"

maximum = len(root)
#maximum = 20

class Files():

	# List of all files alreayd opened and its contents
	def __init__(self):
		self.files = []

	# Insert text after position in project/name
	def insert(self, project, name, text, position):
		for f in self.files:
			if f['project'] == project and f['name'] == name:

				f['content'] = f['content'][:position] + text + f['content'][position:]

				return True

		return False

	# Remove all characters between start and end
	def remove(self, project, name, start, end):
		for f in self.files:
			if f['project'] == project and f['name'] == name:

				#print "Avant : " + f['content'][:start]
				#print "Apres : " + f['content'][end:]

				f['content'] = f['content'][:start] + f['content'][end:]
				#s = s[:pos] + s[(pos+1):]

				return True

		return False

	# Returns True if the file is already opened
	def isOpened(self, project, name):
		for f in self.files:
			if f['project'] == project and f['name'] == name:
				return True
		return False

	# Opens the file (Warning: only saved when the file is closed)
	def open(self, project, name):
		if not self.isOpened(project, name):
			self.files.append({'project': project, 'name': name, 'content': ""})

	# Close all files (Warning: this opens the file, write all contents on it, and close it)
	def closeAll(self):
		global globalPath

		while len(self.files) > 0:
			f = self.files.pop(0)

			fileName = globalPath + f['project'] + "/" + f['name']

			# Check if folder exists, and create it if necessary
			if not os.path.exists(os.path.dirname(fileName)):
				os.makedirs(os.path.dirname(fileName))

			fd = open(fileName, "w+");
			fd.write(f['content'].encode('utf-8','ignore'))
			fd.close()


	# Print all datas of all files
	def printAll(self):
		print self.files



def correctSpecialCharacters(content):
	return content.replace('\\n', '\n').replace('\\t', '	')

files = Files()

for i in range(0, maximum):
	if root[i].attrib.get('K') == "IT":

		currentProject  = root[i][0].text
		currentFile     = root[i][2].text
		currentPosition = int(root[i][3].text)

		content = correctSpecialCharacters(root[i][1].text)


		if not files.isOpened(currentProject, currentFile):
			files.open(currentProject, currentFile)

		files.insert(currentProject, currentFile, content, currentPosition)

	elif root[i].attrib.get('K') == "ST":
		currentProject  = root[i][0].text
		currentFile     = root[i][3].text

		cursorStart     = int(root[i][1].text)
		cursorEnd       = int(root[i][4].text)

		if not files.isOpened(currentProject, currentFile):
			files.open(currentProject, currentFile)

		files.remove(currentProject, currentFile, cursorStart, cursorEnd)


files.printAll()
files.closeAll()
