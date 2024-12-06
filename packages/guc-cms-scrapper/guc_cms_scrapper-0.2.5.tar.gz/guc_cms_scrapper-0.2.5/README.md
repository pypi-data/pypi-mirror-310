# GUC CMS Scrapper

A Python package to scrape the German University in Cairo (GUC) Course Management System (CMS) to retrieve courses and their details.

## Installation


### Pip
```bash
pip install guc-cms-scrapper
```

### Poetry
```bash
poetry add guc-cms-scrapper
```

## Usage

### Authentication

```python
from guc_cms_scrapper import GucCmsScrapper

# Initialize the scrapper with your GUC credentials
scrapper = GucCmsScrapper(username='<your guc username>', password='<your guc password>')
```

### Getting Course List

```python
# Fetch all available courses
courses = scrapper.get_courses()

for course in courses:
  print(f"Course: {course.name}")
  print(f"Code: {course.code}")
  print(f"ID: {course.id}")
  print(f"Semester: {course.semester}")
  print("---")
```

### Getting Course Data

```python
# Fetch detailed data for a specific course
course_data = scrapper.get_course_data(course_id="12345", semester="52")

# Access course announcements
print(course_data.announcements)

# Access weekly content
for week in course_data.weeks:
  print(f"\nWeek starting {week.start_date}")
  print(f"Description: {week.description}")
  
  for item in week.items:
    print(f"Title: {item.title}") # 1 - Practice Assignment 3
    print(f"Clean Title: {item.clean_title}") # Practice Assignment 3 (without the leading number)
    print(f"Type: {item.type}") # Lecture, Assignment, Solution, Other
    print(f"Description: {item.description}")
    print(f"URL: {item.url}")
```

## Development

### Pre-requisites
- Python
- Poetry

### Useful Commands
- Build and Publish to PyPi (You need to be logged in to PyPi, see [here](https://python-poetry.org/docs/repositories/#configuring-credentials))
```bash
poetry publish --build
```
