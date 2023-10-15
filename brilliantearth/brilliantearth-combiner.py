import os
import csv

folder_names = ["asscher", "cushion", "emerald", "heart", "marquise", "oval", "pear", "princess", "radiant"]

lab_output_file = "all_lab.csv"
natural_output_file = "all_natural.csv"

with open(lab_output_file, mode='w', newline='') as lab_file, open(natural_output_file, mode='w', newline='') as natural_file:
    lab_writer = csv.writer(lab_file)
    natural_writer = csv.writer(natural_file)

    header = ["Price ($)", "Carat", "Cut", "Color", "Clarity", "Price/Ct"]
    lab_writer.writerow(header)
    natural_writer.writerow(header)

    for folder_name in folder_names:
        lab_csv_path = os.path.join(folder_name, "lab_data.csv")
        natural_csv_path = os.path.join(folder_name, "natural_data.csv")

        if os.path.exists(lab_csv_path):
            with open(lab_csv_path, mode='r', newline='') as lab_input_file:
                lab_reader = csv.reader(lab_input_file)
                next(lab_reader)
                for row in lab_reader:
                    lab_writer.writerow(row)

        if os.path.exists(natural_csv_path):
            with open(natural_csv_path, mode='r', newline='') as natural_input_file:
                natural_reader = csv.reader(natural_input_file)
                next(natural_reader)
                for row in natural_reader:
                    natural_writer.writerow(row)

print(f"Combined lab data saved to {lab_output_file}")
print(f"Combined natural data saved to {natural_output_file}")