# earnestness-analysis

split_and_sort.py expect a CSV file generated from the following query from zyBook's database:
'''
SELECT ContentResourceActivities.timestamp, UserZyBookPermissions.user_id, ContentResources.content_resource_id, ContentResourceActivities.part, ContentResourceActivities.metadata, ContentResourceActivities.complete, ContentResourceActivities.answer, zyBookContentSections.chapter_number, zyBookContentSections.section_number, zyBooks.zybook_code
FROM ContentResourceActivities, zyBookContentSections, zyBooks, ContentResourceCanonicalSections, ContentResources, UserZyBookPermissions
WHERE ContentResourceActivities.content_resource_id = ContentResources.content_resource_id
  AND ContentResources.content_resource_id = ContentResourceCanonicalSections.content_resource_id
  AND ContentResourceCanonicalSections.canonical_section_id = zyBookContentSections.canonical_section_id
  AND zyBookContentSections.zybook_id = zyBooks.zybook_id
  AND ContentResources.resource_type_id = 6
  AND UserZyBookPermissions.zybook_id = zyBooks.zybook_id
  AND UserZyBookPermissions.subscribed = 1
  AND ContentResourceActivities.zybook_id = zyBooks.zybook_id
  AND zyBooks.zybook_code IN ('UMichENGR151Fall2014', 'UNCPCSC2150DiscMathFall14')
'''