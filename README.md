### Тестовое задание для https://github.com/avito-tech/antibot-developer-trainee
---
#### Как запустить
1) Установить docker, docker-compose
2) Установить git
3) git clone https://github.com/Bor-is-luv/test_task.git
4) (sudo) docker-compose up
---
#### Настройки
Чтобы задать настройки, откройте docker-compose.yml и измените значение переменных окружения flask на собственные
1) LIMIT - количество разрешённых запросов. Целое, больше нуля. 
2) WAITING_TIME - время ожидания в секундах пользователя после превышения лимита.Целое, больше нуля.
3) PERIOD - период времени в секундах, за который отведено LIMIT запросов. Целое, > 0.
4) MASK_VALUE - маска подсети. Целое, от 0 включительно до 32 включительно.
---
При вводе значений типа не int всё сломается. При вводе целого числа < 0 (а в последнем случае и больше 32), будут выставлены дефолтные значения, как в исходном docker-compose.yml.
---
#### Возможные трудности
В ходе развёртывания приложения flask, из интернета устанавливаются зависимости и pip не всегда может их найти. Мне помогло [осбуждение этой проблемы] (https://stackoverflow.com/questions/44761246/temporary-failure-in-name-resolution-errno-3-with-docker) 
Особенно, ответ Jack Fan