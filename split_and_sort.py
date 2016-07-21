import csv
import sys
import operator
from datetime import datetime
import date_range

timestamp_column_index      = 0
student_column_index        = 1
resource_id_column_index    = 2
part_column_index           = 3
showed_column_index         = 4
complete_column_index       = 5
answered_column_index       = 6
chapter_number_column_index = 7
section_number_column_index = 8
zybook_code_column_index    = 9

def get_activity_code(crid, part):
    return crid + '-' + part

'''
    |activity_data| is an array of activity data.
    
    |activity_data_by_zybook_by_student_by_activity| is a dictionary of zybook codes.
    Each zybook code contains a dictionary of user ids.
    Each user id contains a dictionary of unique activity.
    Each unique activity contains a list of activity data for that activity, for that student, for that zybook code.
    
    Ex:
    {
        'zybook_code_1': {
            'user_id_1': {
                'crid_1-part_1': [activity_data_1, activity_data_2]
            }
        }
    }
'''
def split_by_zybooks_by_student_by_activity(activity_data, date_range=None):
    global timestamp_column_index
    global student_column_index
    global resource_id_column_index
    global part_column_index
    global zybook_code_column_index
    
    activity_data_by_zybook_by_student_by_activity = {}
    for datum in activity_data:
        timestamp   = datum[timestamp_column_index]
        user_id     = datum[student_column_index]
        crid        = datum[resource_id_column_index]
        part        = datum[part_column_index]
        zybook_code = datum[zybook_code_column_index]
        
        # If a date range is specified, then only use datum in that date range
        if not(date_range == None):
            activity_timestamp  = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            timestamp_too_early = activity_timestamp < date_range.start_date
            timestamp_too_late  = activity_timestamp > date_range.end_date
            if timestamp_too_early or timestamp_too_late:
                continue
        
        activity_code = get_activity_code(crid, part)
        
        if not(zybook_code in activity_data_by_zybook_by_student_by_activity):
            activity_data_by_zybook_by_student_by_activity[zybook_code] = {}
        
        if not(user_id in activity_data_by_zybook_by_student_by_activity[zybook_code]):
            activity_data_by_zybook_by_student_by_activity[zybook_code][user_id] = {}
        
        if not(activity_code in activity_data_by_zybook_by_student_by_activity[zybook_code][user_id]):
            activity_data_by_zybook_by_student_by_activity[zybook_code][user_id][activity_code] = []
        
        activity_data_by_zybook_by_student_by_activity[zybook_code][user_id][activity_code].append(datum)
    
    return activity_data_by_zybook_by_student_by_activity

def sort_activity_data_by_zybook_by_student_by_activity(activity_data_by_zybook_by_student_by_activity):
    global timestamp_column_index
    
    for zybook_code in activity_data_by_zybook_by_student_by_activity:
        activity_data_by_student_by_activity = activity_data_by_zybook_by_student_by_activity[zybook_code]
        for user_id in activity_data_by_student_by_activity:
            activity_data_by_activity = activity_data_by_zybook_by_student_by_activity[zybook_code][user_id]
            for activity in activity_data_by_activity:
                activity_data = activity_data_by_zybook_by_student_by_activity[zybook_code][user_id][activity]
                activity_data = sorted(activity_data, key=operator.itemgetter(timestamp_column_index))
    
    return activity_data_by_zybook_by_student_by_activity

def load_file_as_list(filename):
    with open(filename, 'rbU') as csv_con:
        reader = csv.reader(csv_con, delimiter=',')
        # Return all but the first row, which is just header data.
        return list(reader)[1:]

def load_split_and_sort_activity_data(filename, date_range=None):
    activity_data                                         = load_file_as_list(filename)
    activity_data_by_zybook_by_student_by_activity        = split_by_zybooks_by_student_by_activity(activity_data, date_range)
    sorted_activity_data_by_zybook_by_student_by_activity = sort_activity_data_by_zybook_by_student_by_activity(activity_data_by_zybook_by_student_by_activity)
    
    return sorted_activity_data_by_zybook_by_student_by_activity

def main(filename):
    load_split_and_sort_activity_data(filename)
    
if __name__ == '__main__':
    main(sys.argv[1])