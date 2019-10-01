'''
    File name: parse_medical.py
    Author: Darren Chang
    Date created: 7/10/2019
    Date last modified: 7/17/2019
    Python Version: 3.6.8
'''
import csv 
import requests 
import xml.etree.ElementTree as ET 
import os
import ntpath
import glob
import pandas as pd

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

	items['barcode'] = root.find('barcode').text

	items['sampleId'] = root.find('sampleId').text

	for alteration in root.iter('alterations'):
		for alt_element in alteration:
			items['type'] = alt_element.find('type').text
			items['gene'] = alt_element.find('gene').text
			items['name'] = alt_element.find('name').text
			items['method'] = alt_element.find('method').text
			items['detected'] = alt_element.find('detected').text
			items['value'] = alt_element.find('value').text
			for type_element in alteration.iter(alt_element.find('type').text):
				items['cfdnaPercentage'] = type_element.find('cfdnaPercentage').text
				items['exon'] = type_element.find('exon').text
				items['chromosome'] = type_element.find('chromosome').text
				items['nucleotideMutation'] = type_element.find('nucleotideMutation').text
				items['position'] = type_element.find('position').text
				items['transcriptId'] = type_element.find('transcriptId').text
				items['reportingCategory'] = type_element.find('reportingCategory').text
				break
			break

	return items 

def savetoCSV(items, filename): 
  
	# specifying the fields for csv file 
	fields = ['accessionId', 'barcode', 'sampleId', 'type', 'gene', 'name',\
			  'method', 'detected', 'value', 'cfdnaPercentage', 'exon', 'chromosome',\
			  'nucleotideMutation', 'position', 'transcriptId', 'reportingCategory']
  
	# writing to csv file 
	with open(filename + '_mutation_data.csv', 'w') as csvfile: 
  
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
	
	extension = 'csv'
	all_filenames = [i for i in glob.glob('*_mutation_data.{}'.format(extension))]
	#combine all files in the list
	combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
	#export to csv
	combined_csv.to_csv( "mutation_csv.csv", index=False, encoding='utf-8-sig')

	  
if __name__ == "__main__": 
  
	# calling main function 
	main() 