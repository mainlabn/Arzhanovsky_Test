# Ссылка на выполненный Дашборд
[Перейти на сайт](https://datalens.yandex/bisz5xxfn8nix)

# Код расчетных показателей дашборда

## Основные переменные

### `full_months_available`
```sql
CASE 
   WHEN c.lessons_in_month > 0 THEN (cu.available_lessons / c.lessons_in_month)::INTEGER
   ELSE 0
END AS full_months_available
```
**Комментарий:** количество полных месяцев курса, доступных ученику. Вычисляется на основе количества доступных уроков и среднего числа уроков в месяц.

### `course_opened_date`
**Комментарий:** дата, когда курс был открыт ученику.

### `course_end_date`
```sql
DATEADD('month', [full_months_available], [course_opened_date])
```
**Комментарий:** последняя дата, до которой курс доступен ученику на основе количества оплаченных месяцев.

### `month_number`
**Комментарий:** номер проверяемого месяца курса. Параметр, создан внутри DataLens.

---

### `extensions_count`
```sql
COUNTD(
  IF(
    [full_months_available] >= [selected_month_number] AND 
    DATEADD('month', [selected_month_number] - 1, [course_opened_date]) < 
    DATEADD('month', [full_months_available], [course_opened_date]),
    [student_id],
    NULL
  )
)
```
**Комментарий:** количество студентов, которые продлили указанный месяц курса. Проверяется, что:
- студент достиг этого месяца по времени,
- у него есть доступ к этому месяцу.

### `extensions_percentage`
```sql
IF([total_students] > 0, 
   ROUND(([extensions_count] * 100.0 / [total_students]), 2), 
   0)
```
**Комментарий:** процент продления месяца от общего числа студентов.

---

### `non_extensions_count`
```sql
COUNTD(
  IF(
    DATEADD('month', [selected_month_number] - 1, [course_opened_date]) >= 
    DATEADD('month', [full_months_available], [course_opened_date]),
    [student_id],
    NULL
  )
)
```
**Комментарий:** количество студентов, у которых нет доступа к выбранному месяцу курса (не продлили). Необходим в фильтрации.

---

### `total_students`
```sql
COUNTD([student_id])
```
**Комментарий:** общее число студентов на выбранных курсах в выборке.

---

Если нужно, можно добавить блоки по группам, предметам, динамике продлений или сегментации по городам/типам курсов.

