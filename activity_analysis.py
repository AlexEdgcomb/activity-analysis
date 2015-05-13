import sys
import csv
import activity_statistics
import activity_order

def get_activity_statistic_by_student(activity_statistics_by_zybook_by_student_by_activity, zybook_code, start_chapter, end_chapter, statistic_to_use):
    activity_order_for_zybook = activity_order.getActivityOrderForChapterRange(zybook_code, start_chapter, end_chapter)
    
    activity_statistic_by_student = {}
    
    activity_statistics_by_student_by_activity = activity_statistics_by_zybook_by_student_by_activity[zybook_code]
    for user_id in activity_statistics_by_student_by_activity:
        activity_statistic_by_student[user_id] = []
        activity_statistics_by_activity = activity_statistics_by_student_by_activity[user_id]
        
        for activity in activity_order_for_zybook:
            statistic_to_record = None
            if statistic_to_use == 'obvious_cheat':
                obvious_cheat = ''
                if activity in activity_statistics_by_activity:
                    if activity_statistics_by_activity[activity]['obvious_cheat']:
                        obvious_cheat = '1'
                    else:
                        obvious_cheat = '0'
                statistic_to_record = obvious_cheat
            elif statistic_to_use == 'completed':
                statistic_to_record = '0'
                if activity in activity_statistics_by_activity:
                    if activity_statistics_by_activity[activity]['completed']:
                        statistic_to_record = '1'
            
            activity_statistic_by_student[user_id].append(statistic_to_record)
    return activity_statistic_by_student

def get_activity_earnestness_by_zybook_by_activity(zybook_codes, activity_order, activity_statistics_by_zybook_by_student_by_activity):
    earnestness_by_activity = []
    for activity in activity_order:
        sum_of_attempts = 0
        sum_of_cheats   = 0
        for zybook_code in zybook_codes:
            activity_statistics_by_student_by_activity = activity_statistics_by_zybook_by_student_by_activity[zybook_code]
            for user_id in activity_statistics_by_student_by_activity:
                activity_statistics_by_activity = activity_statistics_by_student_by_activity[user_id]
        
                obvious_cheat = ''
                if activity in activity_statistics_by_activity:
                    sum_of_attempts += 1
                    if activity_statistics_by_activity[activity]['obvious_cheat']:
                        sum_of_cheats += 1
        earnestness_by_activity.append(1.0 - (float(sum_of_cheats) / float(sum_of_attempts)))
    return earnestness_by_activity

def print_class_earnestness(class_type, class_earnestness):
    to_print = class_type + ','
    for stats in class_earnestness:
        to_print += str(stats) + ','
    print to_print

def print_activity_earnestness_by_student_by_activity(zybook_codes, activity_order, activity_statistics_by_zybook_by_student_by_activity):
    for zybook_code in zybook_codes:
        activity_statistics_by_student_by_activity = activity_statistics_by_zybook_by_student_by_activity[zybook_code]
        for user_id in activity_statistics_by_student_by_activity:
            activity_statistics_by_activity = activity_statistics_by_student_by_activity[user_id]
            
            to_print = str(user_id)
            
            for activity in activity_order:
                obvious_cheat = ''
                if activity in activity_statistics_by_activity:
                    if activity_statistics_by_activity[activity]['obvious_cheat']:
                        obvious_cheat = '1'
                    else:
                        obvious_cheat = '0'
                to_print += ',' + obvious_cheat
            
            print to_print

def earnestness_analysis():
    activity_statistics_by_zybook_by_student_by_activity = activity_statistics.getActivityStatistics('formatted_activity_data_earnestness.csv')
    
    # These crid-part are the same for each zybook from chp 1 - 6
    activity_order = ['631707-0','631707-1','631713-0','631717-0','631717-1','631743-0','631845-0','631845-1','631991-0','631991-1','631991-2','631991-3','632011-0','632011-1','632011-2','632011-3','632011-4','632011-5','632011-6','632011-7','632015-0','632015-1','632015-2','632017-0','632017-1','632017-2','632017-3','632043-0','632043-1','632043-2','632043-3','632043-4','632051-0','632051-1','632051-2','632051-3','632055-0','632055-1','632055-2','632055-3','632055-4','632055-5','632055-6','632055-7','632063-0','632063-1','632063-2','632063-3','632082-0','632082-1','632082-2','632086-0','632086-1','632086-2','632086-3','632086-4','632118-0','632118-1','632118-2','632118-3','632118-4','632129-0','632129-1','632129-2','632129-3','632131-0','632131-1','632144-0','632144-1','632144-2','632144-3','632149-0','632160-0','632174-0','632174-1','632174-2','632176-0','632180-0','632180-1','632180-2','632187-0','632187-1','632187-2','632225-0','632225-1','632405-0','632405-1','632405-2','632405-3','632405-4','632407-0','632407-1','632407-2','632411-0','632411-1','632415-0','632415-1','632415-2','632424-0','632424-1','632424-2','632424-3','632424-4','632424-5','632424-6','632424-7','632424-8','632429-0','632429-1','632450-0','632450-1','632450-2','632452-0','632456-0','632456-1','632456-2','632456-3','632458-0','632458-1','632458-2','632458-3','632458-4','632466-0','632466-1','632481-0','632481-1','632481-2','632481-3','632481-4','632481-5','632502-0','632502-1','632502-2','632511-0','632511-1','632511-2','632511-3','632511-4','632522-0','632522-1','632535-0','632548-0','632548-1','632548-2','632548-3','632548-4','632552-0','632552-1','632552-2','632552-3','632552-4','632552-5','632552-6','632610-0','632610-1','632610-2','632614-0','632614-1','632614-2','632614-3','632614-4','632620-0','632620-1','632620-2','632620-3','632620-4','632632-0','632632-1','632632-2','632632-3','632636-0','632636-1','632636-2','632636-3','632647-0','632647-1','632647-2','632656-0','632656-1','632656-2','632656-3','632665-0','632665-1','632676-0','632676-1','632676-2','632676-3','632676-4','632702-0','632702-1','632704-0','632704-1','632778-0','632778-1','632778-2','632778-3','632778-4','632778-5','632818-0','632818-1','632818-2','632818-3','632834-0','632834-1','632840-0','632840-1','632840-2','632929-0','632929-1','632929-2','632929-3','632929-4','632929-5','632947-0','632947-1','632947-2','633076-0','633076-1','633076-2','633076-3','633076-4','633088-0','633088-1','633088-2','633088-3','633095-0','633095-1','633138-0','633138-1','633138-2','633142-0','633142-1','633142-2','633189-0','633189-1','633207-0','633207-1','633207-2']
    
    #university = get_activity_earnestness_by_zybook_by_activity(['UCRCS10Fall2014'], activity_order, activity_statistics_by_zybook_by_student_by_activity)
    #state      = get_activity_earnestness_by_zybook_by_activity(['FresnoStateCSCI40CppFall2014', 'CSUFresnoCSCI40Fall2014'], activity_order, activity_statistics_by_zybook_by_student_by_activity)
    #community  = get_activity_earnestness_by_zybook_by_activity(['CHCSCSCI110CppFall14', 'MiamiDadeCOP1334Fall2014'], activity_order, activity_statistics_by_zybook_by_student_by_activity)
    
    #print_class_earnestness('university', university)
    #print_class_earnestness('state', state)
    #print_class_earnestness('community', community)
    
    #university = print_activity_earnestness_by_student_by_activity(['UCRCS10Fall2014'], activity_order, activity_statistics_by_zybook_by_student_by_activity)
    #state      = print_activity_earnestness_by_student_by_activity(['FresnoStateCSCI40CppFall2014', 'CSUFresnoCSCI40Fall2014'], activity_order, activity_statistics_by_zybook_by_student_by_activity)
    community  = print_activity_earnestness_by_student_by_activity(['CHCSCSCI110CppFall14', 'MiamiDadeCOP1334Fall2014'], activity_order, activity_statistics_by_zybook_by_student_by_activity)

def get_number_of_completions_and_activities_for_student(statistics_per_activity):
    sum_of_completions   = 0
    number_of_activities = len(statistics_per_activity)
    for activity_statistic in statistics_per_activity:
        if activity_statistic == '1':
            sum_of_completions += 1
    
    return sum_of_completions, number_of_activities

def print_completion_and_points_awarded(activity_statistic_by_student, points_awarded):
    for user_id in activity_statistic_by_student:
        statistics_per_activity                  = activity_statistic_by_student[user_id]
        sum_of_completions, number_of_activities = get_number_of_completions_and_activities_for_student(statistics_per_activity)
        print user_id + ',' + str(float(sum_of_completions) / float(number_of_activities)) + ',' + points_awarded

def get_number_of_completions_and_activities_for_students(activity_statistic_by_student):
    total_completions = 0
    total_activities  = 0
    for user_id in activity_statistic_by_student:
        statistics_per_activity                  = activity_statistic_by_student[user_id]
        sum_of_completions, number_of_activities = get_number_of_completions_and_activities_for_student(statistics_per_activity)
        
        total_completions += sum_of_completions
        total_activities  += number_of_activities
    
    return total_completions, total_activities

def get_number_of_cheats_and_attempts_for_student(statistics_per_activity):
    sum_of_cheats      = 0
    number_of_attempts = 0
    for activity_statistic in statistics_per_activity:
        if activity_statistic != '':
            number_of_attempts += 1
            
            if activity_statistic == '1':
                sum_of_cheats += 1
    
    return sum_of_cheats, number_of_attempts

def print_earnestness_and_points_awarded(activity_statistic_by_student, points_awarded):
    for user_id in activity_statistic_by_student:
        statistics_per_activity = activity_statistic_by_student[user_id]
        
        sum_of_cheats, sum_of_attempts = get_number_of_cheats_and_attempts_for_student(statistics_per_activity)
        
        if sum_of_attempts != 0:
            cheat_score = float(sum_of_cheats) / float(sum_of_attempts)
            earnestness = 1.0 - cheat_score
            print user_id + ',' + str(earnestness) + ',' + points_awarded

def get_number_of_cheats_and_attempts_for_students(activity_statistic_by_student):
    total_cheats               = 0
    total_activities_attempted = 0
    
    for user_id in activity_statistic_by_student:
        statistics_per_activity           = activity_statistic_by_student[user_id]
        sum_of_cheats, number_of_attempts = get_number_of_cheats_and_attempts_for_student(statistics_per_activity)
        
        total_cheats               += sum_of_cheats
        total_activities_attempted += number_of_attempts
    
    return total_cheats, total_activities_attempted

def points_awarded_analysis():
    activity_statistics_by_zybook_by_student_by_activity = activity_statistics.getActivityStatistics('formatted_activity_data_points_awarded.csv')
    
    points_awarded_by_zybook_code = {
        'OUAME2402Fall2014C':            '20',  # ch 1 - 9 was clearly assigned to students
        'MacombITCS1140Python3Fall2014': '17',  # ch 1 - 4 was clearly assigned to students
        'UCICS151Fall2014':              '10',  # ch 1 - 4 was clearly assigned to students
        'UCRCS10Fall2014':               '5',   # ch 1 - 6 was clearly assigned to students
        'GMUCS112Python3Fall2014':       '2.3', # ch 1 - 7 was clearly assigned to students
        'MSStateECE3724Fall2014':        '2',   # ch 1 - 6 was clearly assigned to students
        'UCIICS31Fall2014':              '0',   # ch 1 - 6 was likely assigned to students
        'SJSUCS49CHowellFall2014':       '0'    # ch 1 - 9 was likely assigned to students
    }
    statistics_per_points_awarded = {}
    for zybook_code, points_awarded in points_awarded_by_zybook_code.iteritems():
        if not(points_awarded in statistics_per_points_awarded):
            statistics_per_points_awarded[points_awarded] = {
                # Completion rate
                'total_completed':  0,
                'total_activities': 0,
                
                # Earnestness rate
                'total_cheats':               0,
                'total_activities_attempted': 0
            }
        
        # Completion rate
        activity_statistic_by_student     = get_activity_statistic_by_student(activity_statistics_by_zybook_by_student_by_activity, zybook_code, 1, 4, 'completed')
        print_completion_and_points_awarded(activity_statistic_by_student, points_awarded)
        #total_completed, total_activities = get_number_of_completions_and_activities_for_students(activity_statistic_by_student)
        #statistics_per_points_awarded[points_awarded]['total_completed'] +=  total_completed
        #statistics_per_points_awarded[points_awarded]['total_activities'] += total_activities
        
        # Earnestness rate
        #activity_statistic_by_student            = get_activity_statistic_by_student(activity_statistics_by_zybook_by_student_by_activity, zybook_code, 1, 4, 'obvious_cheat')
        #print_earnestness_and_points_awarded(activity_statistic_by_student, points_awarded)
        #total_cheats, total_activities_attempted = get_number_of_cheats_and_attempts_for_students(activity_statistic_by_student)
        #statistics_per_points_awarded[points_awarded]['total_cheats']               += total_cheats
        #statistics_per_points_awarded[points_awarded]['total_activities_attempted'] += total_activities_attempted
    
    '''
    for points_awarded in statistics_per_points_awarded:
        total_completed  = statistics_per_points_awarded[points_awarded]['total_completed']
        total_activities = statistics_per_points_awarded[points_awarded]['total_activities']
        completion_rate  = float(total_completed) / float(total_activities)
        
        total_cheats               = statistics_per_points_awarded[points_awarded]['total_cheats']
        total_activities_attempted = statistics_per_points_awarded[points_awarded]['total_activities_attempted']
        earnestness_rate           = 1.0 - (float(total_cheats) / float(total_activities_attempted))
        
        print points_awarded + ',' + str(completion_rate) + ',' + str(earnestness_rate)
    '''
    
def main():
    #earnestness_analysis()
    points_awarded_analysis()
    
if __name__ == '__main__':
    main()