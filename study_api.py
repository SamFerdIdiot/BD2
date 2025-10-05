import mysql.connector
import sys
import csv
import argparse
import os
from typing import List, Optional

class StudyDatabase:
    def __init__(self):
        self.connection = None
        self.connect()
        
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', 'rootpassword'),
                database=os.getenv('DB_NAME', 'study'),
                port=3306
            )
        except mysql.connector.Error as err:
            print(f"ошибка подключения к базе данных: {err}")
            sys.exit(1)
    
    def load_students_from_csv(self, filename: str):
        try:
            cursor = self.connection.cursor()
            with open(filename, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    sql = "INSERT INTO students (name, course_number) VALUES (%s, %s)"
                    cursor.execute(sql, (row['name'], int(row['course_number'])))
            self.connection.commit()
            cursor.close()
            print(f"данные успешно загружены из {filename}")
        except Exception as e:
            print(f"ошибка при загрузке csv: {e}")
    
    def get_student(self, student_id: int) -> Optional[dict]:
        try:
            cursor = self.connection.cursor(dictionary=True)
            sql = "SELECT * FROM students WHERE id = %s"
            cursor.execute(sql, (student_id,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except mysql.connector.Error as err:
            print(f"ошибка: {err}")
            return None
    
    def get_discipline_by_course(self, course_number: int) -> List[dict]:
        try:
            cursor = self.connection.cursor(dictionary=True)
            sql = """
            SELECT * FROM disciplines 
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
            """
            cursor.execute(sql, (course_number,))
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as err:
            print(f"ошибка: {err}")
            return []
    
    def get_students_by_course(self, course_number: int) -> List[dict]:
        try:
            cursor = self.connection.cursor(dictionary=True)
            sql = "SELECT * FROM students WHERE course_number = %s ORDER BY name"
            cursor.execute(sql, (course_number,))
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as err:
            print(f"ошибка: {err}")
            return []
    
    def get_all_disciplines(self) -> List[dict]:
        try:
            cursor = self.connection.cursor(dictionary=True)
            sql = "SELECT * FROM disciplines ORDER BY course_number, day_of_week, lesson_number"
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as err:
            print(f"ошибка: {err}")
            return []
    
    def put_student(self, name: str, course_number: int) -> bool:
        try:
            cursor = self.connection.cursor()
            sql = "INSERT INTO students (name, course_number) VALUES (%s, %s)"
            cursor.execute(sql, (name, course_number))
            self.connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as err:
            print(f"ошибка: {err}")
            return False
    
    def put_discipline(self, discipline_name: str, day_of_week: str, lesson_number: int, course_number: int) -> bool:
        try:
            cursor = self.connection.cursor()
            sql = """
            INSERT INTO disciplines (discipline_name, day_of_week, lesson_number, course_number) 
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (discipline_name, day_of_week, lesson_number, course_number))
            self.connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as err:
            print(f"ошибка: {err}")
            return False
    
    def delete_student(self, student_id: int) -> bool:
        try:
            cursor = self.connection.cursor()
            sql = "DELETE FROM students WHERE id = %s"
            cursor.execute(sql, (student_id,))
            self.connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as err:
            print(f"ошибка: {err}")
            return False
    
    def delete_discipline(self, discipline_id: int) -> bool:
        try:
            cursor = self.connection.cursor()
            sql = "DELETE FROM disciplines WHERE id = %s"
            cursor.execute(sql, (discipline_id,))
            self.connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as err:
            print(f"ошибка: {err}")
            return False
    
    def close(self):
        if self.connection:
            self.connection.close()

def main():
    parser = argparse.ArgumentParser(description='система управления базой данных учебного заведения')
    subparsers = parser.add_subparsers(dest='command', help='доступные команды')
    
    parser_get_student = subparsers.add_parser('GET_student', help='получить студента по id')
    parser_get_student.add_argument('student_id', type=int, help='id студента')
    
    parser_get_discipline = subparsers.add_parser('GET_discipline', help='получить занятия по номеру курса')
    parser_get_discipline.add_argument('course_number', type=int, help='номер курса')
    
    parser_get_students = subparsers.add_parser('GET_students', help='получить студентов по номеру курса')
    parser_get_students.add_argument('course_number', type=int, help='номер курса')
    
    parser_get_disciplines = subparsers.add_parser('GET_disciplines', help='получить все занятия')
    
    parser_put_student = subparsers.add_parser('PUT_student', help='добавить нового студента')
    parser_put_student.add_argument('name', type=str, help='имя студента')
    parser_put_student.add_argument('course_number', type=int, help='номер курса')
    
    parser_put_discipline = subparsers.add_parser('PUT_discipline', help='добавить новое занятие')
    parser_put_discipline.add_argument('discipline_name', type=str, help='название дисциплины')
    parser_put_discipline.add_argument('day_of_week', type=str, 
                                     choices=['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'],
                                     help='день недели')
    parser_put_discipline.add_argument('lesson_number', type=int, help='номер пары (1-8)')
    parser_put_discipline.add_argument('course_number', type=int, help='номер курса')
    
    parser_delete_student = subparsers.add_parser('DELETE_student', help='удалить студента по id')
    parser_delete_student.add_argument('student_id', type=int, help='id студента')
    
    parser_delete_discipline = subparsers.add_parser('DELETE_discipline', help='удалить занятие по id')
    parser_delete_discipline.add_argument('discipline_id', type=int, help='id занятия')
    
    parser_load_csv = subparsers.add_parser('LOAD_CSV', help='загрузить студентов из csv файла')
    parser_load_csv.add_argument('filename', type=str, help='имя csv файла')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    db = StudyDatabase()
    
    try:
        if args.command == 'GET_student':
            student = db.get_student(args.student_id)
            if student:
                print(f"id: {student['id']}, имя: {student['name']}, курс: {student['course_number']}")
            else:
                print("студент не найден")
                
        elif args.command == 'GET_discipline':
            disciplines = db.get_discipline_by_course(args.course_number)
            if disciplines:
                for disc in disciplines:
                    print(f"id: {disc['id']}, дисциплина: {disc['discipline_name']}, день: {disc['day_of_week']}, пара: {disc['lesson_number']}, курс: {disc['course_number']}")
            else:
                print("занятия не найдены")
                
        elif args.command == 'GET_students':
            students = db.get_students_by_course(args.course_number)
            if students:
                for student in students:
                    print(f"id: {student['id']}, имя: {student['name']}, курс: {student['course_number']}")
            else:
                print("студенты не найдены")
                
        elif args.command == 'GET_disciplines':
            disciplines = db.get_all_disciplines()
            if disciplines:
                for disc in disciplines:
                    print(f"id: {disc['id']}, дисциплина: {disc['discipline_name']}, день: {disc['day_of_week']}, пара: {disc['lesson_number']}, курс: {disc['course_number']}")
            else:
                print("занятия не найдены")
                
        elif args.command == 'PUT_student':
            if db.put_student(args.name, args.course_number):
                print("студент успешно добавлен")
            else:
                print("ошибка при добавлении студента")
                
        elif args.command == 'PUT_discipline':
            if db.put_discipline(args.discipline_name, args.day_of_week, args.lesson_number, args.course_number):
                print("занятие успешно добавлено")
            else:
                print("ошибка при добавлении занятия")
                
        elif args.command == 'DELETE_student':
            if db.delete_student(args.student_id):
                print("студент успешно удален")
            else:
                print("ошибка при удалении студента")
                
        elif args.command == 'DELETE_discipline':
            if db.delete_discipline(args.discipline_id):
                print("занятие успешно удалено")
            else:
                print("ошибка при удалении занятия")
                
        elif args.command == 'LOAD_CSV':
            db.load_students_from_csv(args.filename)
            
    finally:
        db.close()

if __name__ == "__main__":
    main()
