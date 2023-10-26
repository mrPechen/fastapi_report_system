Fastapi report system

Проект: https://github.com/mrPechen/report_system , но переписанный на FastAPI с использованием Keycloak.

Порядок запуска:

1) В файле .env.txt, убрать расширение "txt" и указать данные для postgres и keycloak. Поля CLIENT_ID, CLIENT_SECRET_KEY, ADMIN_SECRET_KEY, REALM указать после настройки Keycloak.
2) Из корня проекта запустить команду "docker compose -f keycloak.yaml up --build".
   - Keycloak будет доступен по адресу http://localhost:8282/ . Там перейти в "Administration Console" и ввести данные которые вы указали в .env в полях KEYCLOAK_ADMIN и KEYCLOAK_ADMIN_PASSWORD.
   - В левом верхнем углу нажать на "master" -> "create realm". В поле "Realm name" указать желаемое имя, остальное оставить без изменений. Добавить ваш Realm name в поле REALM в env. Убедиться, что вынаходитесь в своем реалме.
   - В меню слева нажать "Clients" -> "Create client". Указать "Client ID" в виде имени и "Name" и нажать "Next". В следующем меню включить "Client authentication" и "Authorization" и сохранить. Добавить ваш Client ID в поле CLIENT_ID в env файле.
   - В появившемся меню в разделе "Access settings" указать следующее: Root URL = http://0.0.0.0:8000/api/v1/login, Valid redirect URIs = http://0.0.0.0:8000/api/v1/callback, Admin URL = http://0.0.0.0:8000/api/v1/login . Сохранить.
   - Сверху во вкладках прейти в Credentials и скопировать Client secret в поле CLIENT_SECRET_KEY в env файл.
   - Перейти в Clients -> admin-cli, пролистать вниз до пункта "Capability config" и включить "Client authentication", "Authorization" и "Standard flow" и сохранить. Далее в этом же меню перейти во вкладку Credentials скопировать Client secret в поле ADMIN_SECRET_KEY в env файл. Далее перейти во вкладку "Service accounts roles" и нажать "Assign role", там отметить все и нажать Assign. Далее нажать еще раз "Assign role" -> "Filter by clients", отметить все и нажать Assign.
   - Далее слева в меню перейти в Realm Settings -> Login и включить User registration, Email as username, Login with email.
   - Тепрь слева в меню в Users можно зараннее создать пользователя. Если пользователь не создан, то он сможет зарегистрироваться сам при попытке аутентификации.

3) В новой вкладке терминала из корня проекта запустить команду "docker compose -f docker-compose.yaml up --build".
4) Эндпоинты:
   - http://0.0.0.0:8000/api/v1/login - Перенаправляет в Keycloak для аутентификации. При успешной аутентификации возвращает access token и refresh token.
   - http://0.0.0.0:8000/api/v1/logout - Логаут.
   - http://0.0.0.0:8000/api/v1/refresh - POST Эндпоинт для рефреша токена. Требует body с json который содержит {"refresh_token": "your refresh token"}.
   - http://0.0.0.0:8000/api/v1/upload - POST Эндпоинт, который принимает в запросе параметры Autherization с протоколом Bearer + access token и body form-data, где key = "file" и value = ваш xlsx файл (пример таблицы в корне проекта в файле "file.xlsx"). Данные из файла добавляются в базу данных.
   - http://0.0.0.0:8000/api/v1//report/{filter_date} - где filter_date = дата формата месяц-год(09-2023). Эндпоинт возвращает xlsx файл в котором записаны минимальные, максимальные и средние значения всех примесей для всех материалов из базы данных за указанный период.



