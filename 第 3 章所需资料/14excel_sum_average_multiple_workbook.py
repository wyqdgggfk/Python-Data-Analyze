import glob
import os
import sys
from datetime import date 
from xlrd import open_workbook,xldate_as_tuple	
from xlwt import Workbook
input_folder = sys.argv[1]
output_file = sys.argv[2]
