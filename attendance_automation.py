# -*- coding: utf-8 -*-
"""Attendance_Automation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wQlwEuOU-zHwC9ZIxGRy2df8sXU5dj7Z
"""

import os
import csv
import shutil
import zipfile
import pandas as pd
from datetime import datetime, timedelta
import os
import zipfile

zip_file_path = r'/content/ClassAttendance.zip'  # Diubah jadi path file zipnya // Change to the zip file path

temp_directory = r'/content/June2024'  # Bikin folder baru dulu buat simpan output, trs pathnya copy disini // Create a new folder to save the output, then copy the path here
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(temp_directory)

print('Extraction Process Succeed!')

csv_files = [file for file in os.listdir(temp_directory) if file.endswith('.csv')]

output_directory = os.path.join(temp_directory, 'csv_utf8')
os.makedirs(output_directory, exist_ok=True)

for file in csv_files:
    file_path = os.path.join(temp_directory, file)
    new_file_path = os.path.join(output_directory, 'utf8_' + file)

    with open(file_path, 'r', encoding='utf-16') as input_file:
        with open(new_file_path, 'w', encoding='utf-8', newline='') as output_file:
            reader = csv.reader(input_file, delimiter='\t')
            writer = csv.writer(output_file, delimiter=',')
            writer.writerows(reader)

print('Conversion Process Succeed!')

output_zip_file_path = r'/content/June2024.zip'  # Copy aja path folder output di atas tp blkgnya tambahin .zip // Copy the output folder path above but add .zip to it
with zipfile.ZipFile(output_zip_file_path, 'w') as zip_file:
    for file in os.listdir(output_directory):
        file_path = os.path.join(output_directory, file)
        zip_file.write(file_path, file)

print('Compression Process Succeed!')

shutil.rmtree(temp_directory)
os.remove(zip_file_path)

print('Succeed!')


import pandas as pd
from datetime import datetime, timedelta
import os
import zipfile

directory = '/content/'

attendance_data = {}

for filename in os.listdir(directory):
    if filename.endswith(".zip"):
        zip_file_path = os.path.join(directory, filename)

        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(directory)

        for extracted_file in os.listdir(directory):
            if extracted_file.endswith(".csv"):
                file_path = os.path.join(directory, extracted_file)

                try:
                    df = pd.read_csv(file_path, usecols=[0, 1], names=['Name', 'Date'])
                except UnicodeDecodeError:
                    df = pd.read_csv(file_path, usecols=[0, 1], names=['Name', 'Date'], encoding='latin-1')

                df.drop_duplicates(subset='Name', keep='first', inplace=True)

                def parse_datetime(x):
                    try:
                        return datetime.strptime(x, "%m/%d/%y, %I:%M:%S %p")
                    except (ValueError, TypeError):
                        return pd.NaT

                df['Date'] = df['Date'].apply(parse_datetime)

                df = df.dropna(subset=['Date'])

                if not df.empty:
                    meeting_start_time = df['Date'].iloc[0].replace(hour=8, minute=30, second=0)
                    late_threshold = timedelta(minutes=15)
                    date = meeting_start_time.strftime('%d/%m')

                    attendance = df.apply(
                        lambda row: 'Late' if row['Date'] > meeting_start_time + late_threshold else 'Attend',
                        axis=1)

                    for i, row in df.iterrows():
                        attendance_data.setdefault(row['Name'], {})[date] = 'Late' if row['Date'] > meeting_start_time + late_threshold else 'Attend'

attendance_df = pd.DataFrame.from_dict(attendance_data)
attendance_df = attendance_df.drop(['Start time', 'End time'], axis=1)

ordered_names = ['James Smith', 'Emily Johnson', 'Michael Williams', 'Emma Brown', 'William Jones', 'Olivia Garcia', 'Benjamin Martinez', 'Ava Rodriguez', 'Lucas Davis', 'Sophia Hernandez',
                 'Henry Miller', 'Mia Martinez', 'Alexander Gonzalez', 'Charlotte Lopez', 'Daniel Wilson', 'Isabella Moore', 'Matthew Taylor', 'Amelia Anderson', 'Joseph Thomas', 'Abigail Jackson',
                 'David White', 'Grace Harris', 'Samuel Carter', 'Natalie Clark', 'Ethan Wright', 'Lily Martinez', 'Jack Walker', 'Chloe Hall']


output_file = 'AttendanceJune2024.xlsx' # Ubah bulan dan tahunnya // Change the month and year
attendance_df = attendance_df.T
attendance_df = attendance_df.reindex(sorted(attendance_df.columns, key=lambda x: datetime.strptime(x, '%d/%m')), axis=1)
attendance_df = attendance_df.reindex(index=ordered_names)
attendance_df.to_excel(output_file)

print("Attendance Data Has Been Saved in an Excel File!")
