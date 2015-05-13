import sys
import split_and_sort
import format_activity_data

'''
    Convert from activity recordings to activity statistics.
    
    Activity recordings: |activity_data_by_zybook_by_student_by_activity| is a dictionary of zybook codes.
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
    
    Activity statistics: |activity_statistics_by_zybook_by_student_by_activity| is a dictionary of zybook codes.
    Each zybook code contains a dictionary of user ids.
    Each user id contains a dictionary of unique activity.
    Each unique activity contains a dictionary of activity statistics, such as |obvious_cheat|.
    Ex:
    {
        'zybook_code_1': {
            'user_id_1': {
                'crid_1-part_1': {
                    'obvious_cheat': Boolean, # if showed_before_correct and (attempts_before_show == blank_attempts_before_show)
                    'completed':     Boolean
                }
            }
        }
    }
    
    Other potential statistics not yet recorded:
    'total_attempts':             Integer, # Number of activities
    'attempts_before_show':       Integer, # Count number of attempts before first show; use null if never showed
    'attempts_before_correct':    Integer, # Count number of attempts (including shows) before first correct; use null if never correct
    'showed_before_correct':      Boolean, # True if show (or only blanks) encountered before correct
    'blank_attempts_before_show': Integer, # Count number of blank attempts before first show; use null if never showed
'''
def convert_to_activity_statistics_by_zybook_by_student_by_activity(activity_data_by_zybook_by_student_by_activity):
    activity_statistics_by_zybook_by_student_by_activity = activity_data_by_zybook_by_student_by_activity
    
    for zybook_code in activity_statistics_by_zybook_by_student_by_activity:
        activity_data_by_student_by_activity = activity_statistics_by_zybook_by_student_by_activity[zybook_code]
        for user_id in activity_data_by_student_by_activity:
            activity_data_by_activity = activity_statistics_by_zybook_by_student_by_activity[zybook_code][user_id]
            
            for activity in activity_data_by_activity:
                activity_data = activity_statistics_by_zybook_by_student_by_activity[zybook_code][user_id][activity]
                
                showed_before_correct      = False
                attempts_before_show       = None
                blank_attempts_before_show = None
                
                has_shown_been_encountered = False
                has_correct_been_countered = False
                for datum in activity_data:
                    answer_shown       = datum[split_and_sort.showed_column_index]   == '1'
                    correctly_answered = datum[split_and_sort.complete_column_index] == '1'
                    answer_given       = datum[split_and_sort.answered_column_index] == '1'
                    
                    if answer_shown:
                        has_shown_been_encountered = True
                    
                    if correctly_answered:
                        has_correct_been_countered = True
                
                    if has_shown_been_encountered:
                        # Student showed answer before getting the correct answer.
                        if not has_correct_been_countered:
                            showed_before_correct = True
                    else:
                        if attempts_before_show == None:
                            attempts_before_show = 0
                        attempts_before_show += 1
                    
                        # The student neither showed nor entered an answer.
                        if not answer_given:
                            if blank_attempts_before_show == None:
                                blank_attempts_before_show = 0
                            blank_attempts_before_show += 1
                
                obvious_cheat = showed_before_correct and (attempts_before_show == blank_attempts_before_show)
                
                activity_statistics_by_zybook_by_student_by_activity[zybook_code][user_id][activity] = {
                    'obvious_cheat': obvious_cheat,
                    'completed':     has_correct_been_countered
                }
    
    return activity_statistics_by_zybook_by_student_by_activity

def getActivityStatistics(filename):
    activity_data_by_zybook_by_student_by_activity       = split_and_sort.load_split_and_sort_activity_data(filename)
    activity_statistics_by_zybook_by_student_by_activity = convert_to_activity_statistics_by_zybook_by_student_by_activity(activity_data_by_zybook_by_student_by_activity)
    
    return activity_statistics_by_zybook_by_student_by_activity

def main(filename):
    activity_statistics_by_zybook_by_student_by_activity = getActivityStatistics(filename)
    
if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main('formatted_activity_data.csv')