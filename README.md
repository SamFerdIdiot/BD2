# BD2

# 1. Запуск системы
docker-compose up -d

# 2. Загрузка данных
docker-compose exec app python study_api.py LOAD_CSV students.csv

# 3. Проверка данных
docker-compose exec app python study_api.py GET_students 1
docker-compose exec app python study_api.py GET_disciplines

# 4. Добавление новых данных
docker-compose exec app python study_api.py PUT_student "наталья орлова" 2
docker-compose exec app python study_api.py PUT_discipline "философия" "Пятница" 1 2

# 5. Проверка добавленных данных
docker-compose exec app python study_api.py GET_students 2
docker-compose exec app python study_api.py GET_discipline 2
