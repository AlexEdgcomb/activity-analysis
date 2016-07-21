import csv
import sys
from sets import Set

def getStudentUserIDsAsSet(filename):
    student_user_ids = Set()
    with open(filename, 'rbU') as csv_con:
        reader = csv.reader(csv_con, delimiter=',')
        for line in reader:
            student_user_ids.add(line[0])

    return student_user_ids

def getSectionChapterByCRID(filename):
    section_chapter_by_crid = {}
    with open(filename, 'rbU') as csv_con:
        reader = csv.reader(csv_con, delimiter=',')
        for line in reader:
            crid    = line[0]
            chapter = line[1]
            section = line[2]
            section_chapter_by_crid[crid] = {
                'section': section,
                'chapter': chapter
            }

    return section_chapter_by_crid

def getZyBookCodeByID(filename):
    zybook_code_by_id = {}
    with open(filename, 'rbU') as csv_con:
        reader = csv.reader(csv_con, delimiter=',')
        for line in reader:
            zybook_id   = line[0]
            zybook_code = line[1]
            zybook_code_by_id[zybook_id] = zybook_code

    return zybook_code_by_id

def format_activity_data(activity_data_filename, crid_to_section_chapter_filename, student_user_ids_filename, zybook_id_to_code_filename):
    student_user_ids        = getStudentUserIDsAsSet(student_user_ids_filename)
    section_chapter_by_crid = getSectionChapterByCRID(crid_to_section_chapter_filename)
    zybook_code_by_id       = getZyBookCodeByID(zybook_id_to_code_filename)

    with open(activity_data_filename, 'rbU') as csv_con:
        reader = csv.reader(csv_con, delimiter=',')
        with open('formatted_activity_data.csv', 'wb') as out_file:
            writer = csv.writer(out_file, delimiter=',')

            header_row = ['timestamp', 'user_id', 'content_resource_id', 'part', 'showed', 'complete', 'answered', 'chapter_number', 'section_number', 'zybook_code']
            writer.writerow(header_row)

            for line in reader:
                timestamp = line[0]
                part      = line[1]
                showed    = line[2]
                complete  = line[3]
                answered  = line[4]
                user_id   = line[5]
                zybook_id = line[6]
                crid      = line[7]

                if user_id in student_user_ids:
                    '''
                        Exclude crids that were removed from the zybooks.
                        Ex: UMichFall2014 had an early release that was later updated with new content.
                    '''
                    if crid in section_chapter_by_crid:
                        chapter     = section_chapter_by_crid[crid]['chapter']
                        section     = section_chapter_by_crid[crid]['section']
                        zybook_code = zybook_code_by_id[zybook_id]

                        activity = [timestamp, user_id, crid, part, showed, complete, answered, chapter, section, zybook_code]
                        writer.writerow(activity)

def main(activity_data_filename, crid_to_section_chapter_filename, instructor_ids_filename, zybook_id_to_code_filename):
    format_activity_data(activity_data_filename, crid_to_section_chapter_filename, instructor_ids_filename, zybook_id_to_code_filename)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        main('tables/activity_data.csv', 'tables/CRID_to_chapter_section.csv', 'tables/student_user_ids.csv', 'tables/zyBookCode_to_zyBookID_mapping.csv')