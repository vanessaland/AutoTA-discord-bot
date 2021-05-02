# Script to Convert JSON files to Excel files
import numpy as np
import pandas as pd

def convert():
  df = pd.read_json('attendance.json')
  print(df.to_string()) 
  df.to_excel('data.xlsx')
