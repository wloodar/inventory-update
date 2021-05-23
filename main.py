from datetime import datetime
from pathlib import Path
import csv
import os

DIR_LOCATION = "C:\\Users\\user\\Desktop\\inventory"
OLD_DIR = './old/'

final_file_name = ""
txt_files = []
quantiy_rows = []

def convert_others(file):
    for line in file:
        if not "szt." in line:
            continue

        quantity = line.split("szt.")[1].split()[0]
        productCode = line.split()[0]

        if int(quantity) > 1:
            quantiy_rows.append([productCode, quantity, 0, 1, "24 godziny"])

def convert_rabalux(file):
    for line in file:
        if not "szt." in line:
            continue

        quantity = line.split("szt.")[1].split()[0]
        productCode = line.split()[0]
        newProductCode = ""

        if "RA" in productCode:
            newProductCode = "RA" + productCode.split("RA")[0]
        else:
            newProductCode = "RA" + productCode

        if int(quantity) > 1:
            quantiy_rows.append([newProductCode, quantity, 0, 1, "24 godziny"])


# Move old csv file to old directory

for file in os.listdir(DIR_LOCATION):
    if file.endswith(".csv"):
        old_csv_file = os.path.join(DIR_LOCATION, file)

        old_dir_name = old_csv_file[old_csv_file.rindex('+')+1:].split(".", 1)[0]

        last_dir_num = -1

        for old_dirs_list in os.listdir(OLD_DIR):
            if old_dir_name in old_dirs_list:
                last_dir_num += 1

        old_dir_name = old_dir_name + '+' + str(last_dir_num)

        Path(old_csv_file).rename(DIR_LOCATION + "\\old\\" + old_dir_name + "\\" + os.path.basename(old_csv_file))


# List all txt files and convert them to rows for csv file

for file in os.listdir(DIR_LOCATION):
    if file.endswith(".txt") or file.endswith(".TXT"):
        txt_files.append(os.path.join(DIR_LOCATION, file))

for file_name in txt_files:
    final_file_name += Path(file_name).stem + "+"

    file = open(file_name, "r")

    if 'rabalux' in file_name.lower():
        convert_rabalux(file)
    else:
        convert_others(file)



# Save quantity rows as csv

if len(txt_files) > 0:
    final_file_name += datetime.today().strftime('%d-%m-%Y') + ".csv"

    with open(final_file_name, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(["product_code", "stock", "stock_warnlevel", "active", "delivery"])
        writer.writerows(quantiy_rows)

    # Move txt files to old directory

    for file in os.listdir(DIR_LOCATION):
        if file.endswith(".csv"):
            old_csv_file = os.path.join(DIR_LOCATION, file)

            old_dir_name = old_csv_file[old_csv_file.rindex('+') + 1:].split(".", 1)[0]

            next_same_date_dir_num = 0

            if os.path.isdir('./old/' + old_dir_name):
                for OLD_DIR in os.listdir('./old/'):
                    if old_dir_name in OLD_DIR:
                        next_same_date_dir_num += 1

            if next_same_date_dir_num > 0:
                old_dir_name += '+' + str(next_same_date_dir_num)

            os.makedirs('./old/' + old_dir_name)

            for txt_file in os.listdir(DIR_LOCATION):
                if file.endswith(".txt") or txt_file.endswith(".TXT"):
                    Path(os.path.join(DIR_LOCATION, txt_file)).rename(
                        "./old/" + old_dir_name + "/" + os.path.basename(txt_file))


print("Files converted :)")