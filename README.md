# Пример реферальной системы

* авторизация по номеру телефона c sms подтверждением (реализована псевдо-отправка sms)
* просмотр и редактирование профиля пользователя (ФИО, email)
* при создании пользователю присваивается его персональный инвайт-код
* можно однократно активировать инвайт-код другого пользователя
* просмотр списка пользователей активировавших ваш инвайт-код

Авторизация через сессии в куки (sessionid + CSRF token)


## Django backend

**/referals_back**

python.exe -m venv venv

\venv\Scripts\activate.bat

pip install -r requirements.txt

python.exe manage.py migrate


## React frontend

**/referals_front**

npm install

npm start
