import os 
import sys
import camelot 
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import resolve1

def count_pages():
	file = open(sys.argv[1], 'rb')
	parser = PDFParser(file)
	document = PDFDocument(parser)

	# This will give you the count of pages
	return (resolve1(document.catalog['Pages'])['Count'])

def struct_Add_order(df_0):
	add_str = ""
	len_add = len(df_0)
	for i in range(0, len_add):
		df_0.iloc[i][0] = str(df_0.iloc[i][0]).replace("\n","")
		df_0.iloc[i][0] = str(df_0.iloc[i][0]).replace(" ","")
		df_0.iloc[i][3] = str(df_0.iloc[i][3]).replace("\n","")
	
	for i in range(1, len_add):
		add_str = add_str + "\t" + str(df_0.iloc[i][3]) + " " + str(df_0.iloc[i][0]) + "[" + str(df_0.iloc[i][2]) + "];" + "\n"
	return ("struct add_order {\n" + add_str + "}\n\n")		

def struct_Execute_order(df_1):
	exec_str = ""
	len_add = len(df_1)
	for i in range(0, len_add):
		df_1.iloc[i][0] = str(df_1.iloc[i][0]).replace("\n","")
		df_1.iloc[i][0] = str(df_1.iloc[i][0]).replace(" ","")
		df_1.iloc[i][3] = str(df_1.iloc[i][3]).replace("\n","")
	
	for i in range(1, len_add):
		exec_str = exec_str + "\t" + str(df_1.iloc[i][3]) + " " + str(df_1.iloc[i][0]) + "[" + str(df_1.iloc[i][2]) + "];" + "\n"
	return ("struct execute_order {\n" + exec_str + "}\n\n")

def struct_Cancel_order(df_2):
	can_str = ""
	len_add = len(df_2)
	for i in range(0, len_add):
		df_2.iloc[i][0] = str(df_2.iloc[i][0]).replace("\n","")
		df_2.iloc[i][0] = str(df_2.iloc[i][0]).replace(" ","")
		df_2.iloc[i][3] = str(df_2.iloc[i][3]).replace("\n","")
	
	for i in range(1, len_add):
		can_str = can_str + "\t" + str(df_2.iloc[i][3]) + " " + str(df_2.iloc[i][0]) + "[" + str(df_2.iloc[i][2]) + "];" + "\n"
	return ("struct cancel_order {\n" + can_str + "}\n\n")	

def struct_Replace_order(df_3):
	rep_str = ""
	len_add = len(df_3)
	for i in range(0, len_add):
		df_3.iloc[i][0] = str(df_3.iloc[i][0]).replace("\n","")
		df_3.iloc[i][0] = str(df_3.iloc[i][0]).replace(" ","")
		df_3.iloc[i][3] = str(df_3.iloc[i][3]).replace("\n","")
	
	for i in range(1, len_add):
		rep_str = rep_str + "\t" + str(df_3.iloc[i][3]) + " " + str(df_3.iloc[i][0]) + "[" + str(df_3.iloc[i][2]) + "];" + "\n"
	return ("struct replace_order {\n" + rep_str + "}\n\n")	
	 	
def write_to_file(str):
	file = open("header.h", "a")
	file.write(str)
	file.close()

def process_pdf_doc():	
	tables = camelot.read_pdf('Sample_Structures1.pdf', pages = '1,2')
	df_0 = tables[0].df
	df_1 = tables[1].df
	df_2 = tables[2].df
	df_3 = tables[3].df

	add_str = struct_Add_order(df_0)
	write_to_file(add_str)
	# print(add_str)
	exec_str = struct_Execute_order(df_1)
	write_to_file(exec_str)
	can_str = struct_Cancel_order(df_2)
	write_to_file(can_str)
	rep_str = struct_Replace_order(df_3)
	write_to_file(rep_str)


if __name__ == "__main__":
	process_pdf_doc()
