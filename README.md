# Activity analysis

Usage:
1) Add 4 CSV files the to tables folder:
    * `activity_data.csv`
    * `CRID_to_chapter_section.csv`
    * `student_user_ids.csv`
    * `zyBookCode_to_zyBookID_mapping.csv`
    
`activity_data_queries.txt` has example queries to produce the above listed 4 CSV files.

2) Run `format_activity_data.py` to produce `formatted_activity_data.csv`.

`format_activity_data.py` merges the above listed 4 CSV files.

3) Run `activity_analysis.py` to produce reports.

4) Customize `activity_analysis.py` and repeat step 3.