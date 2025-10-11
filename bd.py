import psycopg2
import sys

connect = psycopg2.connect(
    host="localhost",
    database="study", 
    user="postgres",
    password="denisov1212"
)

def get_student(student_id):
    cursor = connect.cursor()
    cursor.execute("SELECT student_id, student_name, course FROM students WHERE student_id = %s", (student_id,))
    student = cursor.fetchone()
    if student:
        print(f"ID: {student[0]}, Имя: {student[1]}, Курс: {student[2]}")
    else:
        print("Ошибка")

def get_discipline(course_number):
    cursor = connect.cursor()
    cursor.execute("""
        SELECT discipline_name, day_of_week, lesson_number 
        FROM disciplines 
        WHERE course_number = %s 
        ORDER BY 
            CASE day_of_week
                WHEN 'Понедельник' THEN 1
                WHEN 'Вторник' THEN 2
                WHEN 'Среда' THEN 3
                WHEN 'Четверг' THEN 4
                WHEN 'Пятница' THEN 5
                WHEN 'Суббота' THEN 6
            END,
            lesson_number
    """, (course_number,))
    
    for disc in cursor.fetchall():
        print(f"{disc[1]}, пара {disc[2]}: {disc[0]}")

def get_students(course_number):
    cursor = connect.cursor()
    cursor.execute("SELECT student_name FROM students WHERE course = %s ORDER BY student_name", (course_number,))
    for student in cursor.fetchall():
        print(student[0])

def get_disciplines():
    cursor = connect.cursor()
    cursor.execute("SELECT course_number, day_of_week, lesson_number, discipline_name FROM disciplines ORDER BY course_number, day_of_week, lesson_number")
    for disc in cursor.fetchall():
        print(f"Курс {disc[0]}, {disc[1]}, пара {disc[2]}: {disc[3]}")

def put_student(student_name, course):
    cursor = connect.cursor()
    cursor.execute("SELECT MAX(student_id) FROM students")
    new_id = cursor.fetchone()[0] + 1
    cursor.execute("INSERT INTO students (student_id, student_name, course) VALUES (%s, %s, %s)", (new_id, student_name, course))
    connect.commit()
    print(f"Добавлен студент: ID {new_id}, {student_name}, курс {course}")
def put_discipline(discipline_name, day_of_week, lesson_number, course_number):
    cursor = connect.cursor()
    cursor.execute("INSERT INTO disciplines (discipline_name, day_of_week, lesson_number, course_number) VALUES (%s, %s, %s, %s)",
                   (discipline_name, day_of_week, lesson_number, course_number))
    connect.commit()
    print(f"Добавлено занятие: {discipline_name}, {day_of_week}, пара {lesson_number}, курс {course_number}")

def delete_student(student_id):
    cursor = connect.cursor()
    cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
    connect.commit()
    print(f"Студент с ID {student_id} удален")

def delete_discipline(discipline_id):
    cursor = connect.cursor()
    cursor.execute("DELETE FROM disciplines WHERE id = %s", (discipline_id,))
    connect.commit()
    print(f"Занятие с ID {discipline_id} удалено")

if len(sys.argv) < 2:
    print("Команды:")
    print("GET student id")
    print("GET discipline курс")
    print("GET students курс")
    print("GET disciplines")
    print("PUT student 'имя' курс")
    print("PUT discipline 'название' 'день' пара курс")
    print("DELETE student id")
    print("DELETE discipline id")
elif sys.argv[1] == "GET":
    if sys.argv[2] == "student":
        get_student(int(sys.argv[3]))
    elif sys.argv[2] == "discipline":
        get_discipline(int(sys.argv[3]))
    elif sys.argv[2] == "students":
        get_students(int(sys.argv[3]))
    elif sys.argv[2] == "disciplines":
        get_disciplines()
elif sys.argv[1] == "PUT":
    if sys.argv[2] == "student":
        put_student(sys.argv[3], int(sys.argv[4]))
    elif sys.argv[2] == "discipline":
        put_discipline(sys.argv[3], sys.argv[4], int(sys.argv[5]), int(sys.argv[6]))
elif sys.argv[1] == "DELETE":
    if sys.argv[2] == "student":
        delete_student(int(sys.argv[3]))
    elif sys.argv[2] == "discipline":
        delete_discipline(int(sys.argv[3]))

connect.close()
