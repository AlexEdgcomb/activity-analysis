import sys
import split_and_sort
import format_activity_data

'''
    Return a dictionary of zybook codes.
    Each zybook code contains a list of chapters indexed from 0 .. (n-1), where n is the number of chapters.
    Each chapter contains a list of sections indexed from 0 .. (m-1), where m is the number of sections.
    Each section contains a list of activity codes comprised of: crid + '-' + part
    Ex:
    {
        'zybook_code_1':
            [ # chapter 1
                [ # section 1
                    '12345-1', '12345-2', '12346-1', ...
                ],
                [ # section 2
                    '12350-1', '12351-1', '12351-2', ...
                ]
            ],
            [ # chapter 2
                ...
            ],
            ...
        'zybook_code_2':
            ...
    }
'''
def getActivityBySectionByChapterByZyBookCode():
    zybook_code_by_id = format_activity_data.getZyBookCodeByID('tables/zyBookCode_to_zyBookID_mapping.csv')
    
    activity_by_section_by_chapter_by_zybook = {}
    
    content_resources = split_and_sort.load_file_as_list('tables/CRID_to_chapter_section.csv')
    for content_resource in content_resources:
        crid = content_resource[0]
        
        if not(crid == 'content_resource_id'):
            chapter   = int(content_resource[1]) - 1
            section   = int(content_resource[2]) - 1
            zybook_id = content_resource[3]
            parts     = int(content_resource[4])
        
            zybook_code   = zybook_code_by_id[zybook_id]
        
            if not(zybook_code in activity_by_section_by_chapter_by_zybook):
                activity_by_section_by_chapter_by_zybook[zybook_code] = []
        
            while len(activity_by_section_by_chapter_by_zybook[zybook_code]) <= chapter:
                activity_by_section_by_chapter_by_zybook[zybook_code].append([])
            
            while len(activity_by_section_by_chapter_by_zybook[zybook_code][chapter]) <= section:
                activity_by_section_by_chapter_by_zybook[zybook_code][chapter].append([])
        
            for part in range(parts):
                activity_code = split_and_sort.get_activity_code(crid, str(part))
                activity_by_section_by_chapter_by_zybook[zybook_code][chapter][section].append(activity_code)
    
    return activity_by_section_by_chapter_by_zybook

def getActivityOrderPerZyBookCode():
    activity_by_section_by_chapter_by_zybook = getActivityBySectionByChapterByZyBookCode()
    activity_order_by_zybook_code = {}
    
    for zybook_code in activity_by_section_by_chapter_by_zybook:
        activity_order_by_zybook_code[zybook_code] = []
        
        zybook_code_chapter_section_activity = activity_by_section_by_chapter_by_zybook[zybook_code]
        for chapter_section_activity in zybook_code_chapter_section_activity:
            for section_activity in chapter_section_activity:
                for activity in section_activity:
                    activity_order_by_zybook_code[zybook_code].append(activity)
    
    return activity_order_by_zybook_code

def getActivityOrderForChapterRange(zybook_code, start_chapter, end_chapter):
    activity_by_section_by_chapter_by_zybook = getActivityBySectionByChapterByZyBookCode()
    
    activity_order = []
    for chapter_index, chapter_section_activity in enumerate(activity_by_section_by_chapter_by_zybook[zybook_code]):
        if start_chapter <= (chapter_index + 1) <= end_chapter:
            for section_activity in chapter_section_activity:
                for activity in section_activity:
                    activity_order.append(activity)
    
    return activity_order