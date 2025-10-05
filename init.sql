USE study;

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    course_number INT NOT NULL CHECK (course_number BETWEEN 1 AND 6)
);

CREATE TABLE IF NOT EXISTS disciplines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    discipline_name VARCHAR(100) NOT NULL,
    day_of_week ENUM('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота') NOT NULL,
    lesson_number INT NOT NULL CHECK (lesson_number BETWEEN 1 AND 8),
    course_number INT NOT NULL CHECK (course_number BETWEEN 1 AND 6)
);

INSERT IGNORE INTO disciplines (discipline_name, day_of_week, lesson_number, course_number) VALUES
('Математика', 'Понедельник', 1, 1),
('Физика', 'Понедельник', 2, 1),
('Программирование', 'Вторник', 1, 2),
('Базы данных', 'Среда', 1, 2),
('Алгоритмы', 'Четверг', 3, 3),
('Веб-разработка', 'Пятница', 2, 3);
