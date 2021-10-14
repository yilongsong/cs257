import csv

def main():
    read_file_name = input("file to read: ")
    write_file_name = input("filename to write to: ")


    with open(read_file_name, newline='') as read_file:
        collection = []
        if read_file_name=='athlete_events.csv':
            reader = csv.reader(read_file, delimiter=',', quotechar='"')
        else:
            reader = csv.reader(read_file, delimiter=',', quotechar=',')
        with open(write_file_name, 'w', newline='') as write_file:
            writer = csv.writer(write_file, delimiter=',')
            n=0
            if write_file_name=='raw.csv':
                n=1
            for row in reader:
                if write_file_name == 'athletes.csv':
                    if row[0]=="ID":
                        pass
                    else:
                        print(row)
                        row_to_write=row
                        if row_to_write[1][0]=='"':
                            row_to_write[1]=row_to_write[1][1:-1]
                        row_to_write[0] = int(row_to_write[0])
                        if row_to_write[3]!='NA':
                            row_to_write[3] = int(row_to_write[3])
                        else:
                            row_to_write[3] = 'NULL'
                        if row_to_write[4]!='NA':
                            row_to_write[4] = int(row_to_write[4])
                        else:
                            row_to_write[4] = 'NULL'
                        if row_to_write[5]!='NA':
                            row_to_write[5] = float(row_to_write[5])
                        else:
                            row_to_write[5] = 'NULL'
                        if row_to_write[0] > n:
                            writer.writerow(row_to_write[0:8])
                            n+=1
                elif write_file_name == 'noc_regions1.csv':
                    if row[0]=='NOC':
                        pass
                    else:
                        writer.writerow(row[0:2])
                elif write_file_name == 'events.csv':
                    if row[0]=="ID":
                        pass
                    else:
                        row_to_write=row
                        row_to_write[9] = int(row_to_write[9])
                        if row_to_write not in collection:
                            collection.append(row_to_write)
                elif write_file_name == 'raw.csv':
                    if row[0] == "ID":
                        pass
                    else:
                        row_to_write=row
                        row
                        if row_to_write[1][0]=='"':
                            row_to_write[1]=row_to_write[1][1:-1]
                        row_to_write[0] = int(row_to_write[0])
                        if row_to_write[3]!='NA':
                            row_to_write[3] = int(row_to_write[3])
                        else:
                            row_to_write[3] = 'NULL'
                        if row_to_write[4]!='NA':
                            row_to_write[4] = int(row_to_write[4])
                        else:
                            row_to_write[4] = 'NULL'
                        if row_to_write[5]!='NA':
                            row_to_write[5] = float(row_to_write[5])
                        else:
                            row_to_write[5] = 'NULL'
                        
                        row_to_write[9] = int(row_to_write[9])
                        writer.writerow([n] + row_to_write)
                        n+=1
                        
            m = 1
            if write_file_name=='events.csv':
                collection.sort(key=lambda x : (x[9], x[10], x[11], x[12]))
                for event in collection:
                    writer.writerow([m]+event[8:-1])
                    m+=1


if __name__=='__main__':
    main()