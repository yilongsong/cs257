'''
convert.py
Yilong Song
Oct 19, 2021

Creates four csv files:
athletes.csv using athlete_events.csv and noc_regions.csv
events.csv using athlete_events.csv
raw.csv (helper csv file) using athlete_events.csv
athlete_event.csv (table relating athletes and events) using raw.csv and events.csv
noc_regions.csv using noc_regions_original.csv (renamed from noc_regions.csv)

Order of use:
Write noc_regions.csv before athletes.csv
Write raw.csv before athlete_event.csv

athlete_event.csv and events.csv may take a while to run
'''


import csv

def main():
    read_file_name = input("file to read: ")
    write_file_name = input("filename to write to: ")


    with open(read_file_name, newline='') as read_file:
        collection = {}
        list_collection = []
        if read_file_name=='athlete_events.csv':
            reader = csv.reader(read_file, delimiter=',', quotechar='"') # Handles quotes.
        else:
            reader = csv.reader(read_file, delimiter=',', quotechar=',') # Does not need to handle quotes in this case
        with open(write_file_name, 'w', newline='') as write_file:
            writer = csv.writer(write_file, delimiter=',')
            n=1
            if write_file_name == 'athletes.csv':
                n=0
                with open('noc_regions.csv', newline='') as noc:
                    reader_noc = csv.reader(noc, delimiter=',')
                    list_noc = list(reader_noc)
                    for row in reader:
                        if row[0] == "ID":
                            pass
                        else:
                            print(row)
                            row_to_write = row
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
                            if row_to_write[7] == "SGP":
                                row_to_write[7] = "SIN"
                            for noc in list_noc:
                                if noc[1] == row_to_write[7]:
                                    row_to_write[6] = noc[0]
                            if row_to_write[0] > n:
                                writer.writerow(row_to_write[0:7])
                                n+=1
                            
            for row in reader:
                '''if write_file_name == 'athletes.csv':
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
                            n+=1'''

                if write_file_name == 'noc_regions.csv':
                    if row[0]=='NOC':
                        pass
                    else:
                        writer.writerow([n] + row[0:2])
                        n+=1

                elif write_file_name == 'events.csv':
                    if row[0]=="ID":
                        pass
                    else:
                        row_to_write=row
                        row_to_write[9] = int(row_to_write[9])
                        row_to_write = row_to_write[8:-1]
                        if str(row_to_write) not in collection:
                            collection[str(row_to_write)]=0
                            list_collection.append(row_to_write)


                elif write_file_name == 'raw.csv': # for construction of athlete_event table
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

            if write_file_name == 'athlete_event.csv': # Uses raw.csv and events.csv
                dict_existence = {}
                with open('events.csv', newline='') as events:
                    reader_events = csv.reader(events, delimiter=',')
                    list_events = list(reader_events)
                    with open('raw.csv', newline='') as raw:
                        n=1
                        reader_raw = csv.reader(raw, delimiter=',')
                        for event in list_events:
                            collection[str(event[1:])] = event[0]
                        for line_raw in reader_raw:
                            print(str(n)+'/271116')
                            n+=1
                            row_to_write=[]
                            row_to_write.append(line_raw[1])
                            print(str(line_raw[9:-1]))
                            if str(line_raw[9:-1]) in collection and str(line_raw[1])+str(collection[str(line_raw[9:-1])]) not in dict_existence:
                                row_to_write.append(collection[str(line_raw[9:-1])])
                                dict_existence[str(line_raw[1])+str(collection[str(line_raw[9:-1])])] = 0
                                row_to_write.append(line_raw[-1])
                                writer.writerow(row_to_write)
                            else:
                                print("error")
                            
                            '''for line_events in list_events:
                                if line_events[1:] == line_raw[9:-1]:
                                    print(line_raw)
                                    print(line_events)
                                    row_to_write.append(line_raw[1])
                                    row_to_write.append(line_events[0])
                                    row_to_write.append(line_raw[-1])
                                    writer.writerow(row_to_write)
                                    break'''


                        
            m = 1
            if write_file_name=='events.csv':
                list_collection.sort(key=lambda x : (x[1], x[2], x[4], x[5]))
                for event in list_collection:
                    writer.writerow([m]+event)
                    m+=1


if __name__=='__main__':
    main()