import csv

csv_file_path = 'MSH_USER.csv' #change
destination_file_path = 'MSH_USER_SO_FIXED.csv'
counter = 0
with open(csv_file_path, 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)
    with open(destination_file_path, 'w',encoding='utf-8', newline='') as dest_csv:
            # Create a CSV writer object
            writer = csv.writer(dest_csv)
            
            # Write the header to the destination file
            writer.writerow(header)
            
            # Iterate over rows in the source file and write them to the destination file
            for row in csv_reader:
                if 'С.О' in row[5] and 'РАЙОН' in row[3]:
                    counter += 1
                    writer.writerow(row)
                    print(row[5], counter)

