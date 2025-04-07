# Данный python-скрипт имитирует запрос к БД
# Напишите ваш SQL-запрос в query и запустите данный python-скрипт для получения результата
# Перед запуском скрипта установите библиотеку duckdb

# Установка библиотеки duckdb
# pip install duckdb duckdb-engine

# Импорт библиотек
import pandas as pd
import duckdb
from IPython.display import display

pd.set_option('display.max_columns', None)


# Задание таблиц БД
users = pd.read_csv('CSV/users.csv')
course_users = pd.read_csv('CSV/course_users.csv')
courses = pd.read_csv('CSV/courses.csv')
course_types = pd.read_csv('CSV/course_types.csv')
lessons = pd.read_csv('CSV/lessons.csv')
subjects = pd.read_csv('CSV/subjects.csv')
cities = pd.read_csv('CSV/cities.csv')
homework_done = pd.read_csv('CSV/homework_done.csv')
homework = pd.read_csv('CSV/homework.csv')
homework_lessons = pd.read_csv('CSV/homework_lessons.csv')
user_roles = pd.read_csv('CSV/user_roles.csv')

# Задание SQL-запроса
query = """
SELECT 
    -- Информация о курсе
    c.id AS course_id,                           -- ID курса
    c.name AS course_name,                       -- Название курса
    s.name AS subject_name,                      -- Предмет
    s.project AS subject_type,                   -- Тип предмета (ЕГЭ/ОГЭ)
    ct.name AS course_type,                      -- Тип курса
    c.starts_at AS course_start_date,            -- Дата старта курса
    
    -- Информация о студенте
    u.id AS student_id,                          -- ID ученика
    u.last_name AS student_last_name,            -- Фамилия ученика
    ci.name AS student_city,                     -- Город ученика
    
    -- Информация о статусе студента на курсе
    cu.active AS is_active,                      -- Ученик не отчислен с курса (1 = активен, 0 = отчислен)
    cu.created_at AS course_opened_date,         -- Дата открытия курса ученику
    
    -- Расчет количества полных месяцев с момента открытия курса
    (
        EXTRACT(YEAR FROM age(CURRENT_DATE, cu.created_at::DATE)) * 12 + 
        EXTRACT(MONTH FROM age(CURRENT_DATE, cu.created_at::DATE))
    )::INTEGER AS full_months_since_opening,
    
    -- Расчет количества выполненных домашних заданий
    (
        SELECT COUNT(DISTINCT hd.id)
        FROM homework_done hd
        JOIN homework h ON hd.homework_id = h.id
        JOIN homework_lessons hl ON h.id = hl.homework_id
        JOIN lessons l ON hl.lesson_id = l.id
        WHERE hd.user_id = u.id
        AND l.course_id = c.id
        AND hd.mark IS NOT NULL  -- Только завершенные домашние задания
    ) AS homework_done_count
    
FROM courses c
JOIN subjects s ON c.subject_id = s.id
JOIN course_types ct ON c.course_type_id = ct.id
JOIN course_users cu ON c.id = cu.course_id
JOIN users u ON cu.user_id = u.id
LEFT JOIN cities ci ON u.city_id = ci.id

WHERE 
    -- Только годовые курсы
    ct.id = 1  -- 1 = 'Годовой'
    
    -- Только курсы ЕГЭ и ОГЭ
    AND s.project IN ('ЕГЭ', 'ОГЭ')
    
    -- Только пользователи с ролью student
    AND u.user_role_id = 5
    
ORDER BY 
    c.id, 
    u.last_name;
"""

# Выполнение SQL-запроса
df_result = duckdb.query(query).to_df()

# Вывод результата
display(df_result)