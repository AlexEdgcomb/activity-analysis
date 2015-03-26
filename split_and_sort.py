import csv
import sys
import operator
from datetime import datetime

timestamp_column_index   = 0
student_column_index     = 1
resource_id_column_index = 2
part_column_index        = 3
zybook_code_column_index = 9

def read_activity_data_as_list(filename):
    with open(filename, 'rbU') as csv_con:
        reader = csv.reader(csv_con, delimiter=',')
        return list(reader)

def separate_by_zybooks(activity_data):
    global zybook_code_column_index
    
    activity_data_header = activity_data[0]
    activity_data_body   = activity_data[1:]
    
    zybooks = {}
    for activity in activity_data_body:
        zybook_code = activity[zybook_code_column_index]
        if not(zybook_code in zybooks):
            zybooks[zybook_code] = [activity_data_header]
        zybooks[zybook_code].append(activity)
    
    return zybooks

def convert_to_epoch(timestamp_string):
    # Example time format: 2014-08-28 15:12:47
    timestamp_in_datetime = datetime.strptime(timestamp_string, '%Y-%m-%d %H:%M:%S')
    return (timestamp_in_datetime - datetime(1970, 1, 1)).total_seconds()

def convert_epoch_to_timestamp(epoch_time):
    seven_hours_in_seconds = 7 * 60 * 60
    return datetime.fromtimestamp(epoch_time + seven_hours_in_seconds).strftime('%Y-%m-%d %H:%M:%S')

def sort_activity_data(activity_data_by_zybook):
    global timestamp_column_index
    global student_column_index
    global resource_id_column_index
    global part_column_index
    
    for zybook_code in activity_data_by_zybook.keys():
        activity_data = activity_data_by_zybook[zybook_code]
        
        header = activity_data[0]
        body   = activity_data[1:]
        
        # Convert timestamps to epoch
        for activity in body:
            activity[timestamp_column_index] = convert_to_epoch(activity[timestamp_column_index])
        
        body = sorted(body, key=operator.itemgetter(student_column_index, resource_id_column_index, part_column_index, timestamp_column_index))
        activity_data_by_zybook[zybook_code] = [header] + body
        
        # Convert timestamps back to string. Ex: 2014-08-28 15:12:47
        for activity in body:
            activity[timestamp_column_index] = convert_epoch_to_timestamp(activity[timestamp_column_index])
    
    return activity_data_by_zybook

def write_to_csv(activity_data_by_zybook):
    for zybook_code in activity_data_by_zybook.keys():
        activity_data = activity_data_by_zybook[zybook_code]
        
        with open(zybook_code + '.csv', 'wb') as out_file:
            writer = csv.writer(out_file, delimiter=',')
            for activity in activity_data:
                writer.writerow(activity)

def main(filename):
    activity_data = read_activity_data_as_list(filename)
    activity_data_by_zybook = separate_by_zybooks(activity_data)
    sorted_activity_data_by_zybook = sort_activity_data(activity_data_by_zybook)
    write_to_csv(sorted_activity_data_by_zybook)
    
if __name__ == '__main__':
    main(sys.argv[1])