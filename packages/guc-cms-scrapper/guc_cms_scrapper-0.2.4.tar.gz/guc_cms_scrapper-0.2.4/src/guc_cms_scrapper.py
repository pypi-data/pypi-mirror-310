from dataclasses import dataclass
import datetime
from enum import Enum
import re
from bs4 import BeautifulSoup
import requests
import requests_ntlm

GUC_CMS_BASE_URL = "https://cms.guc.edu.eg"

@dataclass
class CourseMetadata:
    id: str
    code: str
    name: str

    semester: str
    """
    Current semester of the course. For example: 52.
    Used in the URL (`sid` query parameter) to get the course page.
    """


class InvalidCredentialsError(Exception):
    pass


class CourseItemType(str, Enum):
    LECTURE_SLIDES = "Lecture Slides"
    ASSIGNMENT = "Assignment"
    SOLUTION = "Solution"
    OTHER = "Other"


@dataclass
class CourseItem:
    title: str
    type: CourseItemType
    description: str
    url: str
    number: int
    clean_title: str


@dataclass
class CourseWeek:
    start_date: datetime.datetime
    description: str
    items: list[CourseItem]


@dataclass
class CourseData:
    announcements: str
    weeks: list[CourseWeek]


def infer_course_item_type(raw_type: str) -> CourseItemType:
    lower_raw_type = raw_type.lower()
    
    if "lecture" in lower_raw_type:
        return CourseItemType.LECTURE_SLIDES
    elif "solution" in lower_raw_type:
        return CourseItemType.SOLUTION
    elif "assignment" in lower_raw_type:
        return CourseItemType.ASSIGNMENT
    else:
        return CourseItemType.OTHER

def clean_title(title: str) -> str:
    # 1 - Lecture 5 => Lecture 5
    # 2 - Practice Assignment 5 => Practice Assignment 5
    # 4 - Practice Assignment 5 Solution => Practice Assignment 5 Solution
    
    regex = r'^\d+ - (.*)$'
    match = re.match(regex, title)
    
    return match.group(1) if match else title


def extract_item_number(title: str) -> int:
    # 1 - Lecture 5 => 5
    # 2 - Practice Assignment 5 => 5
    # 4 - Practice Assignment 5 Solution => 5
    
    regex = r'^\d+ -.*(\d+).*$'
    match = re.match(regex, title)
    
    return int(match.group(1)) if match else -1


class GucCmsScrapper:
    def __init__(self, username: str, password: str):
        self.authenticated_session = GucCmsScrapper.get_authenticated_session(username, password, base_url)

    def get_authenticated_session(username: str, password: str) -> requests.Session:
        """
        Authenticates a user with the provided username and password and returns an authenticated session.
        This method logs in to the GUC CMS and returns a session object that can be used to make further
        requests as the authenticated user.
        Args:
            username (str): The GUC username
            password (str): The GUC password
        Returns:
            requests.Session: An authenticated session object.
        Raises:
            InvalidCredentialsError: If the authentication fails (e.g., due to incorrect username or password).
        Example:
            session = GucCmsScrapper.get_authenticated_session("username", "password")
            response = session.get("https://cms.guc.edu.eg")
            print(response.text)
        """

        session = requests.Session()
        session.auth = requests_ntlm.HttpNtlmAuth(username, password)

        response = session.get(GUC_CMS_BASE_URL)

        if response.status_code == 401:
            raise InvalidCredentialsError()

        return session

    def get_courses(self) -> list[CourseMetadata]:
        """
        Fetches the list of courses from the GUC CMS.
        This method sends a GET request to the GUC CMS student homepage, parses the HTML content,
        and extracts course metadata including course ID, code, name, and semester.
        Returns:
            list[CourseMetadata]: A list of CourseMetadata objects containing course details.
        Example:
            scrapper = GucCmsScrapper("username", "password")
            courses = scrapper.get_courses()
            for course in courses:
                print(course.id, course.code, course.name, course.semester)
        """

        url = GUC_CMS_BASE_URL + "/apps/student/HomePageStn.aspx"

        response = self.authenticated_session.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        courses = []

        for row in soup.select(
            "#ContentPlaceHolderright_ContentPlaceHoldercontent_GridViewcourses > tr:not(:first-child)"
        ):
            cells = row.select("td")
            name_full = cells[1].text.strip()  # (|DMET901|) Computer Vision (571) => (|{CODE}|) {NAME} ({ID})
            code, name, id = re.match(r"\(\|(.*)\|\) (.*) \((.*)\)", name_full).groups()
            semester = cells[5].text.strip()

            courses.append(CourseMetadata(id=id, code=code, name=name, semester=semester))

        return courses

    def get_course_data(self, course_id: str, semester: str) -> CourseData:
        """
        Fetches and parses course data from the GUC CMS for a given course and semester.
        Args:
            course_id (str): The ID of the course to fetch data for.
            semester (str): The semester ID to fetch data for.
        Returns:
            CourseData: An object containing the course announcements and weekly data.
        Example:
            scrapper = GucCmsScrapper("username", "password")
            course_data = scrapper.get_course_data(course_id="12345", semester="52")
            print(course_data.announcements)
            for week in course_data.weeks:
                print(week.start_date, week.description)
                for item in week.items:
                    print(item.title, item.type, item.description, item.url)
        """

        url = f"{GUC_CMS_BASE_URL}/apps/student/CourseViewStn.aspx?id={course_id}&sid={semester}"
        response = self.authenticated_session.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        announcements = soup.select_one("#ContentPlaceHolderright_ContentPlaceHoldercontent_desc").decode_contents()

        weeks = []
        for weekSoup in soup.select(".weeksdata"):
            start_date_str = weekSoup.select_one("h2").text.strip()  # Week: 2024-9-14 => Week: {DATE}
            start_date = datetime.datetime.strptime(start_date_str, "Week: %Y-%m-%d")

            description = weekSoup.find("strong", text="Description").parent.find_next_sibling("p").text.strip()
            week_items = []

            for itemSoup in weekSoup.select(".card-body"):
                titleSoup = itemSoup.select_one("[id^=content] :first-child")
                title = titleSoup.text.strip()
                
                type_raw = titleSoup.next_sibling.strip()                
                description = itemSoup.select_one("div:nth-child(2)").text.strip()
                
                url = GUC_CMS_BASE_URL + "/" + itemSoup.select_one("a")["href"]
                
                course_item = CourseItem(
                    title=title, 
                    type=infer_course_item_type(type_raw), 
                    description=description, 
                    url=url,
                    number=extract_item_number(title),
                    clean_title=clean_title(title)
                )
                
                week_items.append(course_item)

            weeks.append(CourseWeek(start_date=start_date, description=description, items=week_items))

        return CourseData(announcements=announcements, weeks=weeks)
