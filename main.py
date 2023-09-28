import logging
# My option lists for
from menu_definitions import menu_main, debug_select
from IntrospectionFactory import IntrospectionFactory
from db_connection import engine, Session
from orm_base import metadata
# Note that until you import your SQLAlchemy declarative classes, such as Student, Python
# will not execute that code, and SQLAlchemy will be unaware of the mapped table.
from Department import Department
from Course import Course
from Option import Option
from Menu import Menu
# Poor man's enumeration of the two available modes for creating the tables
from constants import START_OVER, INTROSPECT_TABLES, REUSE_NO_INTROSPECTION
#import IPython  # So that I can exit out to the console without leaving the application.
from sqlalchemy import inspect  # map from column name to attribute name
from pprint import pprint
from datetime import time
from Section import Section


def add_department(session):
    """
    Prompt the user for the information for a new department and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    '''
    unique_name: bool = False
    unique_abbreviation: bool = False
    name: str = ''
    abbreviation: str = ''
    while not unique_abbreviation or not unique_name:
        name = input("Department full name--> ")
        abbreviation = input("Department abbreviation--> ")
        name_count: int = session.query(Department).filter(Department.name == name).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a department by that name.  Try again.")
        if unique_name:
            abbreviation_count = session.query(Department). \
                filter(Department.abbreviation == abbreviation).count()
            unique_abbreviation = abbreviation_count == 0
            if not unique_abbreviation:
                print("We already have a department with that abbreviation.  Try again.")
    new_department = Department(abbreviation, name)
    session.add(new_department)
    '''

    unique_abbr = False
    unique_chair = False
    unique_office = False
    unique_desc = False
    departmentName: str = ''
    abbreviation: str = ''
    chairName: str = ''
    building: str = ''
    officeNum: int = 0
    description: str = ''

    while not unique_abbr or not unique_chair or not unique_office or not unique_desc:
        departmentName = input("Department name --> ")
        abbreviation = input("Department's abbreviation --> ")
        chairName = input("Department Chair name --> ")
        building = input("Building name --> ")
        officeNum = int(input("Office number --> "))
        description = input("Description of department --> ")

        abbr_count = session.query(Department).filter(Department.abbreviation == abbreviation).count()
        chair_count = session.query(Department).filter(Department.chairName == chairName).count()
        office_count = session.query(Department).filter(Department.building == building,
                                                        Department.officeNum == officeNum).count()
        desc_count = session.query(Department).filter(Department.description == description).count()

        unique_abbr = abbr_count == 0
        unique_chair = chair_count == 0
        unique_office = office_count == 0
        unique_desc = desc_count == 0

        if not unique_abbr:
            print("We already have a department by that abbreviation. Try again.")
        elif not unique_chair:
            print("The named individual is already a chair of a different department. Try again.")
        elif not unique_office:
            print("That office room is already occupied by another department. Try again.")
        elif not unique_desc:
            print("That description matches the description of another department. Try again.")
    newDepartment = Department(abbreviation, departmentName, chairName, building, officeNum, description)
    session.add(newDepartment)

def add_course(session):
    """
    Prompt the user for the information for a new course and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    print("Which department offers this course?")
    department: Department = select_department(sess)
    unique_number: bool = False
    unique_name: bool = False
    number: int = -1
    name: str = ''
    while not unique_number or not unique_name:
        name = input("Course full name--> ")
        number = int(input("Course number--> "))
        name_count: int = session.query(Course).filter(Course.departmentAbbreviation == department.abbreviation,
                                                       Course.name == name).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a course by that name in that department.  Try again.")
        if unique_name:
            number_count = session.query(Course). \
                filter(Course.departmentAbbreviation == department.abbreviation,
                       Course.courseNumber == number).count()
            unique_number = number_count == 0
            if not unique_number:
                print("We already have a course in this department with that number.  Try again.")
    description: str = input('Please enter the course description-->')
    units: int = int(input('How many units for this course-->'))
    course = Course(department, number, name, description, units)
    session.add(course)


def validating_time() -> time:
    valid_time = False
    while not valid_time:
        time_input = input("Start time--> ")
        if len(time_input) != 7 or time_input[1] != ":":
            print("Invalid input. Structure input like this -> '8:32 PM'.")
        else:
            valid_time = True
            if time_input[5:] == "PM":
                hours = int(time_input[0]) + 12
            else:
                hours = int(time_input[0])
            minutes = int(time_input[2:4])
    return time(hours, minutes, 0)


def add_section(sess : Session):
    print("Which course do you want to add a section to?")
    course: Course = select_course(sess)
    semester_list = ["fall", "winter", "spring", "summer i", "summer ii"]
    building_list = ["VEC", "ECS", "EN2", "EN3", "EN4", "ET", "SSPA"]
    schedule_list = ["MW", "TuTh", "MWF", "F", "S"]
    unique_reservation = False

    while not unique_reservation:
        correct_semester = False
        correct_building = False
        correct_schedule = False
        while not correct_semester:
            semester = input("Semester offered--> ")
            if semester.lower() not in semester_list:
                print(f"Invalid input. Make sure you are selecting a valid semester.\nSelect one-> {semester_list}")
            else:
                correct_semester = True
        sectionYear = int(input("Year offered--> "))
        while not correct_schedule:
            schedule = input("Days Scheduled--> ")
            if schedule not in schedule_list:
                print(f"Invalid input. Make sure you are selecting a valid schedule.\nSelect one-> {schedule_list}")
            else:
                correct_schedule = True
        startTime: time = validating_time()
        instructor = input("Instructor name--> ")
        instructor_count: int = sess.query(Section).filter(Section.sectionYear == sectionYear, Section.semester == semester,
                                                            Section.schedule == schedule, Section.startTime == startTime,
                                                            Section.instructor == instructor).count()

        unique_instructor_slot = instructor_count == 0
        if not unique_instructor_slot:
            print("That instructor is already booked for that time, please re-enter inputs.")
        else:
            while not correct_building:
                building = input("Building name--> ")
                if building not in building_list:
                    print(f"Invalid input. Make sure you are choosing a valid building.\nSelect one-> {building_list}")
                else:
                    correct_building = True
            room = int(input("Enter Room Number--> "))
            reservation_count: int = sess.query(Section).filter(Section.sectionYear == sectionYear, Section.semester == semester,
                                                            Section.schedule == schedule, Section.startTime == startTime,
                                                            Section.building == building, Section.room == room).count()

            unique_reservation = reservation_count == 0
            if not unique_reservation:
                print("The room selected is already booked, please re-enter inputs.")
    section = Section(course, semester, sectionYear, building, room, schedule, startTime, instructor)
    sess.add(section)

def select_section(sess: Session) -> Section:
    found = False
    abbreviation: str = ''
    course_number: int = -1
    section_number: int = -1
    section_year: int = -1
    semester: str = ''
    while not found:
        abbreviation = input("Department Abbreviation--> ")
        course_number = int(input("Course Number--> "))
        section_number = int(input("Section Number--> "))
        section_year = int(input("Section Year--> "))
        semester = input("Semester--> ")
        unique_count = sess.query(Section).filter(Section.departmentAbbreviation == abbreviation,
                                                  Section.courseNumber == course_number, Section.sectionNumber == section_number,
                                                  Section.sectionYear == section_year, Section.semester == semester).count()

        found = unique_count == 1
        if not found:
            print("No Sections with the given inputs. Try again.")
    section = sess.query(Section).filter(Section.departmentAbbreviation == abbreviation,
                                         Section.courseNumber == course_number, Section.sectionNumber == section_number,
                                         Section.sectionYear == section_year, Section.semester == semester).first()
    return section

def list_sections(sess: Session):
    found = False
    abbreviation: str = ''
    course_number: int = -1
    while not found:
        abbreviation = input("Department Abbreviation--> ")
        course_number = int(input("Course Number--> "))
        unique_count = sess.query(Section).filter(Section.departmentAbbreviation == abbreviation,
                                                  Section.courseNumber == course_number).count()
        found = unique_count >= 1
        if not found:
            print("No sections for that course. Try again")
    sections: [Section] = list(sess.query(Section).filter(Section.departmentAbbreviation == abbreviation,
                                                          Section.courseNumber == course_number))
    print(f"Sections in {abbreviation} {course_number}:")
    for section in sections:
        print(section)

def delete_section(sess):

    section = select_section(sess)
    sess.delete(section)

def select_department(sess) -> Department:
    """
    Prompt the user for a specific department by the department abbreviation.
    :param sess:    The connection to the database.
    :return:        The selected department.
    """
    found: bool = False
    abbreviation: str = ''
    while not found:
        abbreviation = input("Enter the department abbreviation--> ")
        abbreviation_count: int = sess.query(Department). \
            filter(Department.abbreviation == abbreviation).count()
        found = abbreviation_count == 1
        if not found:
            print("No department with that abbreviation.  Try again.")
    return_student: Department = sess.query(Department). \
        filter(Department.abbreviation == abbreviation).first()
    return return_student


def select_course(sess) -> Course:
    """
    Select a course by the combination of the department abbreviation and course number.
    Note, a similar query would be to select the course on the basis of the department
    abbreviation and the course name.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    department_abbreviation: str = ''
    course_number: int = -1
    while not found:
        department_abbreviation = input("Department abbreviation--> ")
        course_number = int(input("Course Number--> "))
        name_count: int = sess.query(Course).filter(Course.departmentAbbreviation == department_abbreviation,
                                                    Course.courseNumber == course_number).count()
        found = name_count == 1
        if not found:
            print("No course by that number in that department.  Try again.")
    course = sess.query(Course).filter(Course.departmentAbbreviation == department_abbreviation,
                                       Course.courseNumber == course_number).first()
    return course

def delete_course(sess):
    """
    asks the user for the course to delete by course abbreviation and deletes it
    :param sess: connection to database
    :return: None
    """

    print('Deleting Course')

    course = select_course(sess)
    n_sections = sess.query(Section).filter(Section.departmentAbbreviation == course.departmentAbbreviation,
                                            Section.courseNumber == course.courseNumber).count()
    if n_sections > 0:
        print(f"Sorry, there are {n_sections} sections in that course. Delete them first,"
              f" then come back here to delete the course")
    else:
        sess.delete(course)

    sess.delete(course)

def delete_department(session):
    """
    Prompt the user for a department by the abbreviation and delete it.
    :param session: The connection to the database.
    :return:        None
    """
    print("deleting a department")
    department = select_department(session)
    n_courses = session.query(Course).filter(Course.departmentAbbreviation == department.abbreviation).count()
    if n_courses > 0:
        print(f"Sorry, there are {n_courses} courses in that department.  Delete them first, "
              "then come back here to delete the department.")
    else:
        session.delete(department)


def list_departments(session):
    """
    List all departments, sorted by the abbreviation.
    :param session:     The connection to the database.
    :return:            None
    """
    # session.query returns an iterator.  The list function converts that iterator
    # into a list of elements.  In this case, they are instances of the Student class.
    departments: [Department] = list(session.query(Department).order_by(Department.abbreviation))
    for department in departments:
        print(department)


def list_courses(sess):
    """
    List all courses currently in the database.
    :param sess:    The connection to the database.
    :return:        None
    """
    # session.query returns an iterator.  The list function converts that iterator
    # into a list of elements.  In this case, they are instances of the Student class.
    courses: [Course] = sess.query(Course).order_by(Course.courseNumber)
    for course in courses:
        print(course)


def move_course_to_new_department(sess):
    """
    Take an existing course and move it to an existing department.  The course has to
    have a department when the course is created, so this routine just moves it from
    one department to another.

    The change in department has to occur from the Course end of the association because
    the association is mandatory.  We cannot have the course not have any department for
    any time the way that we would if we moved it to a new department from the department
    end.

    Also, the change in department requires that we make sure that the course will not
    conflict with any existing courses in the new department by name or number.
    :param sess:    The connection to the database.
    :return:        None
    """
    print("Input the course to move to a new department.")
    course = select_course(sess)
    old_department = course.department
    print("Input the department to move that course to.")
    new_department = select_department(sess)
    if new_department == old_department:
        print("Error, you're not moving to a different department.")
    else:
        # check to be sure that we are not violating the {departmentAbbreviation, name} UK.
        name_count: int = sess.query(Course).filter(Course.departmentAbbreviation == new_department.abbreviation,
                                                    Course.name == course.name).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a course by that name in that department.  Try again.")
        if unique_name:
            # Make sure that moving the course will not violate the {departmentAbbreviation,
            # course number} uniqueness constraint.
            number_count = sess.query(Course). \
                filter(Course.departmentAbbreviation == new_department.abbreviation,
                       Course.courseNumber == course.courseNumber).count()
            if number_count != 0:
                print("We already have a course by that number in that department.  Try again.")
            else:
                course.set_department(new_department)


def select_student_from_list(session):
    """
    This is just a cute little use of the Menu object.  Basically, I create a
    menu on the fly from data selected from the database, and then use the
    menu_prompt method on Menu to display characteristic descriptive data, with
    an index printed out with each entry, and prompt the user until they select
    one of the Students.
    :param session:     The connection to the database.
    :return:            None
    """
    # query returns an iterator of Student objects, I want to put those into a list.  Technically,
    # that was not necessary, I could have just iterated through the query output directly.
    students: [Department] = list(sess.query(Department).order_by(Department.lastName, Department.firstName))
    options: [Option] = []  # The list of menu options that we're constructing.
    for student in students:
        # Each time we construct an Option instance, we put the full name of the student into
        # the "prompt" and then the student ID (albeit as a string) in as the "action".
        options.append(Option(student.lastName + ', ' + student.firstName, student.studentId))
    temp_menu = Menu('Student list', 'Select a student from this list', options)
    # text_studentId is the "action" corresponding to the student that the user selected.
    text_studentId: str = temp_menu.menu_prompt()
    # get that student by selecting based on the int version of the student id corresponding
    # to the student that the user selected.
    returned_student = sess.query(Department).filter(Department.studentId == int(text_studentId)).first()
    # this is really just to prove the point.  Ideally, we would return the student, but that
    # will present challenges in the exec call, so I didn't bother.
    print("Selected student: ", returned_student)


def list_department_courses(sess):
    department = select_department(sess)
    dept_courses: [Course] = department.get_courses()
    print("Course for department: " + str(department))
    for dept_course in dept_courses:
        print(dept_course)


if __name__ == '__main__':
    print('Starting off')
    #logging.basicConfig()
    # use the logging factory to create our first logger.
    # for more logging messages, set the level to logging.DEBUG.
    # logging_action will be the text string name of the logging level, for instance 'logging.INFO'
    #logging_action = debug_select.menu_prompt()
    # eval will return the integer value of whichever logging level variable name the user selected.
    #logging.getLogger("sqlalchemy.engine").setLevel(eval(logging_action))
    # use the logging factory to create our second logger.
    # for more logging messages, set the level to logging.DEBUG.
    #logging.getLogger("sqlalchemy.pool").setLevel(eval(logging_action))

    # Prompt the user for whether they want to introspect the tables or create all over again.
    introspection_mode: int = IntrospectionFactory().introspection_type
    if introspection_mode == START_OVER:
        print("starting over")
        # create the SQLAlchemy structure that contains all the metadata, regardless of the introspection choice.
        metadata.drop_all(bind=engine)  # start with a clean slate while in development

        # Create whatever tables are called for by our "Entity" classes that we have imported.
        metadata.create_all(bind=engine)
    elif introspection_mode == INTROSPECT_TABLES:
        print("reusing tables")
        # The reflection is done in the imported files that declare the entity classes, so there is no
        # reflection needed at this point, those classes are loaded and ready to go.
    elif introspection_mode == REUSE_NO_INTROSPECTION:
        print("Assuming tables match class definitions")

    with Session() as sess:
        main_action: str = ''
        while main_action != menu_main.last_action():
            main_action = menu_main.menu_prompt()
            print('next action: ', main_action)
            exec(main_action)
        sess.commit()
    print('Ending normally')

#5gAg$v$H