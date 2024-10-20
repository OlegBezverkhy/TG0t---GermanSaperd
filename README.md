# TG0t - GermanSaperd
 Решение урока TG05
Телеграмм бот, который используя API получает информацию с сайта http://numbersapi.com/.  
Реализована проверка, если пользователь выбирает дату или год, на корректность: может ли быть введенное число быть датой или годом.  
Вот примет использования указанного API с сайта http://numbersapi.com/:Использование API: 
http://numbersapi.com/<number>/<type>, где number — число, а type — тип факта (trivia — факт из жизни,math — математический факт, date и year — вопрос про дату (в формате MM/DD) и год).   

Например, получить факт о 25 октября можно по запросу http://numbersapi.com/10/25/date:  
#### October 25th is the day in 1760 that George III becomes King of Great Britain.  
Все ключи и токены хранятся в отдельном файле config.py
