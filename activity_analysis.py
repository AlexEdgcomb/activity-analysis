import sys
import csv
import activity_statistics
import activity_order
import date_range

def get_activity_statistic_by_student_by_activity_order(activity_order, zybook_code, activity_statistics_by_zybook_by_student_by_activity, statistic_to_use):
    activity_statistic_by_student = {}

    if zybook_code in activity_statistics_by_zybook_by_student_by_activity:
        activity_statistics_by_student_by_activity = activity_statistics_by_zybook_by_student_by_activity[zybook_code]
        for user_id in activity_statistics_by_student_by_activity:
            activity_statistic_by_student[user_id] = []
            activity_statistics_by_activity = activity_statistics_by_student_by_activity[user_id]

            for activity in activity_order:
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

def get_activity_statistic_by_student_by_chapter_range(activity_statistics_by_zybook_by_student_by_activity, zybook_code, start_chapter, end_chapter, statistic_to_use):
    activity_order_for_zybook = activity_order.getActivityOrderForChapterRange(zybook_code, start_chapter, end_chapter)
    return get_activity_statistic_by_student_by_activity_order(activity_order_for_zybook, zybook_code, activity_statistics_by_zybook_by_student_by_activity, statistic_to_use)

def get_activity_statistic_by_student_given_sections(activity_statistics_by_zybook_by_student_by_activity, zybook_code, sections_by_chapter, statistic_to_use):
    activity_order_for_zybook = activity_order.getActivityOrderForSections(zybook_code, sections_by_chapter)
    return get_activity_statistic_by_student_by_activity_order(activity_order_for_zybook, zybook_code, activity_statistics_by_zybook_by_student_by_activity, statistic_to_use)

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
        activity_statistic_by_student     = get_activity_statistic_by_student_by_chapter_range(activity_statistics_by_zybook_by_student_by_activity, zybook_code, 1, 4, 'completed')
        print_completion_and_points_awarded(activity_statistic_by_student, points_awarded)
        #total_completed, total_activities = get_number_of_completions_and_activities_for_students(activity_statistic_by_student)
        #statistics_per_points_awarded[points_awarded]['total_completed'] +=  total_completed
        #statistics_per_points_awarded[points_awarded]['total_activities'] += total_activities

        # Earnestness rate
        #activity_statistic_by_student            = get_activity_statistic_by_student_by_chapter_range(activity_statistics_by_zybook_by_student_by_activity, zybook_code, 1, 4, 'obvious_cheat')
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

def print_student_completion_and_earnestness(zybook_codes, sections_by_chapter, format_activity_filename, date_range=None):
    for zybook_code in zybook_codes:
        activity_statistics_by_zybook_by_student_by_activity = activity_statistics.getActivityStatistics(format_activity_filename, date_range)

        completion_by_student    = get_activity_statistic_by_student_given_sections(activity_statistics_by_zybook_by_student_by_activity, zybook_code, sections_by_chapter, 'completed')
        obvious_cheat_by_student = get_activity_statistic_by_student_given_sections(activity_statistics_by_zybook_by_student_by_activity, zybook_code, sections_by_chapter, 'obvious_cheat')

        sum_of_completion     = 0.0
        sum_of_earnestness    = 0.0
        number_of_earnestness = 0
        for user_id in completion_by_student:
            completion_per_activity                  = completion_by_student[user_id]
            sum_of_completions, number_of_activities = get_number_of_completions_and_activities_for_student(completion_per_activity)
            student_completion                       = float(sum_of_completions) / float(number_of_activities)
            sum_of_completion                        = sum_of_completion + student_completion

            obvious_cheat_per_activity     = obvious_cheat_by_student[user_id]
            sum_of_cheats, sum_of_attempts = get_number_of_cheats_and_attempts_for_student(obvious_cheat_per_activity)
            student_earnestness            = 'n/a'
            if sum_of_attempts != 0:
                cheat_score           = float(sum_of_cheats) / float(sum_of_attempts)
                student_earnestness   = 1.0 - cheat_score
                sum_of_earnestness    = sum_of_earnestness + student_earnestness
                number_of_earnestness = number_of_earnestness + 1

            if date_range == None:
                print user_id + ',' + zybook_code + ',' + str(student_completion) + ',' + str(student_earnestness)

        if not(date_range == None):
            average_completion  = 0.0
            average_earnestness = 'na'
            if not(len(completion_by_student) == 0):
                average_completion  = sum_of_completion / float(len(completion_by_student))
            if not(number_of_earnestness == 0):
                average_earnestness = sum_of_earnestness / float(number_of_earnestness)
            print zybook_code + ',' + str(average_completion) + ',' + str(average_earnestness)

def brano_spring2015():
    zybook_codes = ['PDXECE102Spring2015']

    # Dictionary of chapter numbers storing an array of section numbers
    sections_by_chapter = {
        1:  [4, 5],
        2:  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        3:  [1, 2, 4, 5, 6, 7, 8],
        4:  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        5:  [1, 2, 3, 4, 5, 6, 7],
        11: [1, 2, 3, 4, 5],
        12: [1, 2, 3, 4, 5, 6],
        3:  [3],
        13: [1, 2],
        8:  [1, 2, 3, 4, 5, 6, 7, 8, 9],
        9:  [1, 2, 9],
        13: [3, 4, 5, 6, 7],
        7:  [1, 2, 3, 4, 5, 6, 7]
    }

    print_student_completion_and_earnestness(zybook_codes, sections_by_chapter, 'formatted_activity_data_brano.csv')

def brano_winter2015():
    zybook_codes = ['PortlandStateECE102Winter2015', 'PortlandStateECE102WongWinter2015']

    # Dictionary of chapter numbers storing an array of section numbers
    sections_by_chapter = {
        1:  [4, 5],
        2:  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        3:  [1, 2, 4, 5, 6, 7, 8],
        4:  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        5:  [1, 2, 3, 4, 7],
        10: [1, 2, 3, 4, 5, 6, 7, 8, 9],
        5:  [5, 6],
        11: [1, 2, 3, 4, 6, 8, 9, 10],
        13: [6, 7, 10],
        3:  [3],
        12: [1, 2, 3, 4, 5, 6, 7],
        7:  [1, 2, 3, 4, 5],
        8:  [1, 2, 3, 4, 5, 6],
        9:  [1, 2, 3, 4, 5, 6, 7],
        14: [1, 2, 3, 4, 5, 6, 7]
    }

    print_student_completion_and_earnestness(zybook_codes, sections_by_chapter, 'formatted_activity_data_brano.csv')

def UCRCS30Spring2015():
    zybook_codes = ['UCRCS30Spring2015']

    # All of ch 1 - 13
    sections_by_chapter = {
        1:  [1, 2, 3, 4, 5, 6],
        2:  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        3:  [1, 2, 3, 4, 5, 6, 7, 8, 9],
        4:  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        5:  [1, 2, 3, 4, 5, 6, 7],
        6:  [1, 2, 3, 4, 5, 6, 7, 8],
        7:  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        8:  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        9:  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        10: [1, 2, 3, 4, 5],
        11: [1, 2, 3, 4, 5, 6],
        12: [1, 2, 3, 4, 5, 6, 7, 8, 9],
        13: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    }

    print_student_completion_and_earnestness(zybook_codes, sections_by_chapter, 'formatted_activity_data_like_brano.csv')

def IAStateME160Spring2015():
    zybook_codes = ['IAStateME160Spring2015']

    # All of ch 1 - 15
    sections_by_chapter = {
        1:  [1, 2, 3, 4, 5, 6],
        2:  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        3:  [1, 2, 3, 4, 5, 6, 7, 8, 9],
        4:  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        5:  [1, 2, 3, 4, 5, 6, 7],
        6:  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        7:  [1, 2, 3, 4, 5, 6, 7, 8],
        8:  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        9:  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        10: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        11: [1, 2, 3, 4, 5],
        12: [1, 2, 3, 4, 5, 6],
        13: [1, 2, 3, 4, 5, 6, 7, 8, 9],
        14: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        15: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    }

    print_student_completion_and_earnestness(zybook_codes, sections_by_chapter, 'formatted_activity_data_like_brano.csv')

def UCDavisENG0062015():
    zybook_codes = ['UCDavisENG006Spring2015', 'UCDavisENG006Winter2015']

    # All of ch 1 - 15
    sections_by_chapter = {
        1:  [1, 2, 3, 4, 5, 6],
        2:  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        3:  [1, 2, 3, 4, 5, 6, 7, 8, 9],
        4:  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        5:  [1, 2, 3, 4, 5, 6, 7],
        6:  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        7:  [1, 2, 3, 4, 5, 6, 7, 8],
        8:  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        9:  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        10: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        11: [1, 2, 3, 4, 5],
        12: [1, 2, 3, 4, 5, 6],
        13: [1, 2, 3, 4, 5, 6, 7, 8, 9],
        14: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        15: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    }

    print_student_completion_and_earnestness(zybook_codes, sections_by_chapter, 'formatted_activity_data_like_brano.csv')

def UCIICS6BSpring2015(weekly=False):
    zybook_codes = ['UCIICS6BSpring2015']

    # Assigned sections
    sections_by_chapter = {
        1: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        2: [1, 2, 3, 4],
        3: [1, 2, 3],
        4: [1, 2, 3, 4, 5],
        5: [1, 2, 3, 4, 5, 6, 7],
        6: [4, 5]
    }

    if weekly:
        weeks = [
            date_range.DateRange('3-22-2015', '3-28-2015'),
            date_range.DateRange('3-29-2015', '4-4-2015'),
            date_range.DateRange('4-5-2015', '4-11-2015'),
            date_range.DateRange('4-12-2015', '4-18-2015'),
            date_range.DateRange('4-19-2015', '4-25-2015'),
            date_range.DateRange('4-26-2015', '5-2-2015'),
            date_range.DateRange('5-3-2015', '5-9-2015'),
            date_range.DateRange('5-10-2015', '5-16-2015'),
            date_range.DateRange('5-17-2015', '5-23-2015'),
            date_range.DateRange('5-24-2015', '5-30-2015'),
            date_range.DateRange('5-31-2015', '6-6-2015'),
            date_range.DateRange('6-7-2015', '6-13-2015'),
            date_range.DateRange('6-14-2015', '6-20-2015'),
            date_range.DateRange('6-21-2015', '6-27-2015'),
            date_range.DateRange('6-28-2015', '7-4-2015')
        ]
        for week in weeks:
            print_student_completion_and_earnestness(zybook_codes, sections_by_chapter, 'formatted_activity_data_UCR_UCI_Spring15.csv', week)
    else:
        print_student_completion_and_earnestness(zybook_codes, sections_by_chapter, 'formatted_activity_data_UCR_UCI_Spring15.csv')

def UCRCS10Spring2015(weekly=False):
    zybook_codes = ['UCRCS10Spring2015']

    # Assigned sections
    sections_by_chapter = {
        1: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        2: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
        3: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        4: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        5: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        6: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    }

    if weekly:
        weeks = [
            date_range.DateRange('3-22-2015', '3-28-2015'),
            date_range.DateRange('3-29-2015', '4-4-2015'),
            date_range.DateRange('4-5-2015', '4-11-2015'),
            date_range.DateRange('4-12-2015', '4-18-2015'),
            date_range.DateRange('4-19-2015', '4-25-2015'),
            date_range.DateRange('4-26-2015', '5-2-2015'),
            date_range.DateRange('5-3-2015', '5-9-2015'),
            date_range.DateRange('5-10-2015', '5-16-2015'),
            date_range.DateRange('5-17-2015', '5-23-2015'),
            date_range.DateRange('5-24-2015', '5-30-2015'),
            date_range.DateRange('5-31-2015', '6-6-2015'),
            date_range.DateRange('6-7-2015', '6-13-2015'),
            date_range.DateRange('6-14-2015', '6-20-2015'),
            date_range.DateRange('6-21-2015', '6-27-2015'),
            date_range.DateRange('6-28-2015', '7-4-2015')
        ]
        for week in weeks:
            print_student_completion_and_earnestness(zybook_codes, sections_by_chapter, 'formatted_activity_data_UCR_UCI_Spring15.csv', week)
    else:
        print_student_completion_and_earnestness(zybook_codes, sections_by_chapter, 'formatted_activity_data_UCR_UCI_Spring15.csv')

def UCRCS10Spring2015_and_2016():
    zybooks = [
        {
            'zybook_code': 'UCRCS10Spring2015',
            'sections_by_chapter': {
                1: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                2: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
                3: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                4: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                5: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                6: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            },
        },
        {
            'zybook_code': 'UCRCS10Spring2016',
            'sections_by_chapter': {
                1: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
                2: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                3: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
                4: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                5: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
                6: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
                7: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            }
        }
    ]

    for zybook in zybooks:
        zybook_code = zybook['zybook_code']
        sections_by_chapter = zybook['sections_by_chapter']

        print_student_completion_and_earnestness([ zybook_code ], sections_by_chapter, 'formatted_activity_data_UCR_Spring15_Spring16.csv')


def UCRCS10Winter2015_and_2016():
    zybooks_all_assigned_sections = [
        {
            'zybook_code': 'UCRCS10Winter2015',
            'sections_by_chapter': {
                1: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                2: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                3: [1, 2, 3, 4, 5, 6, 7, 8],
                4: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                5: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
                6: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            },
        },
        {
            'zybook_code': 'UCRCS10Winter2016',
            'sections_by_chapter': {
                1: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
                2: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                3: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
                4: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                5: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
                6: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
                7: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            }
        }
    ]

    zybooks_same_assigned_sections = [
        {
            'zybook_code': 'UCRCS10Winter2015',
            'sections_by_chapter': {
                #1: [1, 2, 3, 4, 5, 6, 7, 8],
                #2: [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14],
                #3: [1, 2, 3, 4, 5, 6, 7],
                #4: [1, 2, 3, 4, 5, 6, 7, 8, 9],
                #5: [1, 2, 3, 4, 5, 6, 8, 9, 10],
                6: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            },
        },
        {
            'zybook_code': 'UCRCS10Winter2016',
            'sections_by_chapter': {
                #1: [7, 8, 9, 2, 3, 4, 5, 6],
                #2: [1, 2, 3, 4, 14, 6, 5, 8, 17, 10, 9, 15, 18],
                #3: [1, 2, 3, 4, 5, 8, 9],
                #4: [1, 2, 3, 4, 5, 11, 12, 13, 10],
                #5: [1, 2, 3, 4, 5, 8, 13, 12, 6],
                6: [1, 2, 3, 4, 6, 8, 7, 11, 5, 12],
            }
        }
    ]

    for zybook in zybooks_same_assigned_sections:
        zybook_code = zybook['zybook_code']
        sections_by_chapter = zybook['sections_by_chapter']
        print_student_completion_and_earnestness([ zybook_code ], sections_by_chapter, 'formatted_activity_data_UCR_Winter15_Winter16.csv')

def main():
    #earnestness_analysis()
    #points_awarded_analysis()

    #brano_spring2015()
    #brano_winter2015()
    #UCRCS30Spring2015()
    #IAStateME160Spring2015()
    #UCDavisENG0062015()

    #UCIICS6BSpring2015()
    #UCRCS10Spring2015()

    #UCIICS6BSpring2015(weekly=True)
    #UCRCS10Spring2015(weekly=True)

    #UCRCS10Spring2015_and_2016()
    UCRCS10Winter2015_and_2016()

if __name__ == '__main__':
    main()