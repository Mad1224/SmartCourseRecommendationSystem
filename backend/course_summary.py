"""
Show course distribution by Kulliyyah
"""
from pymongo import MongoClient
from collections import Counter

client = MongoClient('mongodb://localhost:27017/')
db = client['fyp2']

courses = list(db.courses.find({}))
print(f'📊 Total Courses in Database: {len(courses)}\n')
print('='*60)

# Count by Kulliyyah
kulliyyah_counts = Counter([c.get('kulliyyah', 'Unknown') for c in courses])

print('\n🏛️  Courses by Kulliyyah:\n')
for kulliyyah, count in sorted(kulliyyah_counts.items(), key=lambda x: x[1], reverse=True):
    percentage = (count / len(courses)) * 100
    print(f'  {kulliyyah:15s}: {count:3d} courses ({percentage:5.1f}%)')

print('\n' + '='*60)

# Show sample courses from each kulliyyah
print('\n📚 Sample Courses by Kulliyyah:\n')

kulliyyah_info = {
    'KOE': 'Kulliyyah of Engineering',
    'KICT': 'Kulliyyah of Information & Communication Technology',
    'KENMS': 'Kulliyyah of Economics & Management Sciences',
    'KAHS': 'Kulliyyah of Allied Health Sciences',
    'KOP': 'Kulliyyah of Pharmacy',
    'KIRKHS': 'Kulliyyah of Islamic Revealed Knowledge & Human Sciences'
}

for kulliyyah, full_name in kulliyyah_info.items():
    print(f'\n{kulliyyah} - {full_name}:')
    kulliyyah_courses = [c for c in courses if c.get('kulliyyah') == kulliyyah]
    for course in kulliyyah_courses[:5]:  # Show first 5 courses
        print(f"  • {course['course_code']}: {course['course_name']}")
    if len(kulliyyah_courses) > 5:
        print(f"  ... and {len(kulliyyah_courses) - 5} more courses")

print('\n' + '='*60)

# Show programs
print('\n🎓 Available Programs:\n')
programs = set([c.get('program') for c in courses if c.get('program')])
for program in sorted(programs):
    program_courses = [c for c in courses if c.get('program') == program]
    print(f'  • {program}: {len(program_courses)} courses')
