import csv 
import requests 
import xml.etree.ElementTree as ET 
import os
import ntpath

def get_xml_files(path):
	xml_list = []
	for filename in os.listdir(path):
		if filename.endswith(".xml"):
			xml_list.append(os.path.join(path, filename))
	return xml_list

def parseXML(xmlfile): 
  
	# create element tree object 
	tree = ET.parse(xmlfile) 
  
	# get root element 
	root = tree.getroot() 
  
	# create empty list for news items 
	items = {}

	# Patient Data 
	items['accessionId'] = root.find('accessionId').text

	items['specimen'] = root.find('specimen').text

	for patient in root.iter('patient'):
		gender = patient.find('gender').text
		dob = patient.find('dob').text
	items['gender'] = gender
	items['dob'] = dob

	for physician in root.iter('physician'):
		physician_last = physician.find('lastName').text
		physician_first = physician.find('firstName').text
	items['physician'] = physician_first + " " + physician_last
	
	items['specimen'] = root.find('specimen').text

	items['barcode'] = root.find('barcode').text
	
	items['sampleId'] = root.find('sampleId').text

	print(root.find('accessionId').text)

	for disease in root.find('disease'):
		#print("1: " + disease.text)
		#print("2: " + disease.text.split('\n')[0])
		items['disease_name'] = disease.text.split('\n')[0]
		break

	for classification in root.iter('classification'):
		items['disease_classification_name'] = classification.find('name').text

	codes = []
	lst = []
	for code in root.iter('icdCodes'):
		codes = code.findall('icdCode')

	for element in codes:
		lst.append(element.text)
	items['icdCodes'] = lst

	# return news items list 
	return items 

def savetoCSV(items, filename): 
  
	# specifying the fields for csv file 
	fields = ['accessionId', 'specimen', 'gender', 'dob', 'physician',\
			  'specimen', 'barcode', 'sampleId', 'disease_name',\
			  'disease_classification_name', 'icdCodes']
  
	# writing to csv file 
	with open(filename + '_patient_data.csv', 'w') as csvfile: 
  
		# creating a csv dict writer object 
		writer = csv.DictWriter(csvfile, fieldnames = fields) 
  
		# writing headers (field names) 
		writer.writeheader() 
  
		# writing data rows 
		writer.writerow(items) 
  
	  
def main(): 

	dir_path = os.getcwd() + "/XML-Files"
	xml_files = get_xml_files(dir_path)
	#print(xml_files)

	# parse xml file 
	print("-----------------------------------------------------")
	for file in xml_files:
		items = parseXML(file)
		name = os.path.splitext(ntpath.basename(file))[0]
		print(items)
		#print(name) #print case that prints the name of XML file
		# store news items in a csv file 
		savetoCSV(items, name) 
		print("-----------------------------------------------------")
	  
	  
if __name__ == "__main__": 
  
	# calling main function 
	main() 