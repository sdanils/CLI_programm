# Клиент для взаимодействия с сервером в виде CLI программы. 
Проект содержит CLI программу для взаимедействи с сервером, так же включает в себя логирование некоторых событий и тесты. Спецификация API сервера описана в sms-platform.yaml. 

Описание:
При запуске программы, вызывается функция login_verification() для проверки пользователя. Проверка осуществляется с помощью ввода пороля, который хранится файле параметров программы config.toml. Для хранения пароля используется хэш md5. Для примера в программе используется "12345". 
Если хэш пароля совпадает с сохранённым, меню продлогает создать рассылку. В этом случае происходит чтение данных рассылки и проверка на корректность данных. Номер телефона проверяется с помощью регулярного выражения, которое достается из файла конфигурации. Это должно упростить изменение маски ввода.
После проверки данных создается экземпляр http запроса Mailing_request. В нём хранится вся необходимая информация о запросе и функции, нужные для отправки.
Метод Mailing_request.to_bytes конвертирует поля класса в строку http запроса. Которая передаётся по сокету, соеденённому с адресом из конфигурации программы. Тоесть общение с сервером реализовано через модуль socket.
Для хранения ответа сервера реализован класс Mailing_response, содержащий статический метод from_bytes. from_bytes преобразует строку байт в обьект http ответа. 
Эта реализация позволяет просто представить работу сокета и запросов. Для отправки сообщения создается класс запроса, принимающий словарь данных и вызвается Mailing_request.make_request. Он совершает отправку и в себе вызывает метод создания ответа, возвращаю обект Mailing_response с информацией об ответе.
В программе предусмотрено логирование важных событий. В логфаил записывается информация о входе в программу, действия отправки данных, результаты отправки данных и результаты чтения ответа от сервера.
Проект также сожержит несколько тестов на pytest. Тесты покрывают функции чтения номера телефона и работы масок ввода. Для этого используются фикстуры и параметры pytest. Есть тесты проверяющие методы создания запроса/ответа по строки байт и обратные им (to_bytes() и from_bytes()). Так же включены тесты для проверки работы программы с сервером. 
Важно что тесты не содержаться в проекте. Для обхода проблемы с импортом проверяемых модулей используется подход временного добавления каталога приложения в sys.path.

Структура проекта:
Файлом конфигурации программы является config.toml. В нём хранятся маршруты сервера [path], пользователи [user], адрес сервера [server] и маска ввода номера телефона в формате строки, она нужна для формирования регулярного выражения.
Основной проект содержится в папке app. cli_app.py главный фаил, в нём запускается CLI интерфейс. Фаил verification_function.py содержит функции проверки введёного пароля и сравнение его с хранящимся хэшем md5. number_functions.py содержит функции для чтения и проверки телефона. 
Конфигурация программы читается из config.toml, реализация содержится в get_config.py. 
Creating_mailing.py содержит функцию, создающую рассылку. Это чтение данных и создание обьекта запроса.

Инструкция по запуску:
Пароль "12345". Хранится в md5
Запуск тестов через python. Без использования конфигураций. Команда из дериктории проекта: py -m pytest test/tests_.py. реализовано через добавлением дериктории приложения в sys.path. Запуск тестов с включенным сервером и виртуальной средой. pytest test/mockON_tests.py из mockOn    
