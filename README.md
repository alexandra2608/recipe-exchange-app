# Recipe Exchange App

Веб-приложение для публикации и обмена рецептами.
Пользователи могут создавать, редактировать и просматривать рецепты через современный SPA-интерфейс.

Проект разработан в рамках учебной проектной деятельности и демонстрирует работу fullstack-приложения с разделением на frontend и backend.

## Технологический стек

Frontend

* Vue.js
* JavaScript
* HTML5
* CSS3

Backend

* Django
* Django REST Framework

База данных

* SQLite

## Основные возможности

* авторизация и регистрация
* просмотр списка рецептов
* создание новых рецептов
* редактирование рецептов
* удаление рецептов
* подписки на кулинаров
* лайки и комментарии
* сохранение рецептов в профиль
* оценивание рецептов

## Структура проекта

recipe-exchange-app/backend — серверная часть на Django
recipe-exchange-app/frontend — клиентское SPA-приложение на Vue.js
recipe-exchange-app/screenshots — скриншоты интерфейса

## Установка и запуск

### Backend

1. Перейти в папку backend

`cd backend`

2. Создать виртуальное окружение

`python -m venv venv`

3. Активировать окружение

Windows
`venv\Scripts\activate`

Mac / Linux
`source venv/bin/activate`

4. Установить зависимости

`pip install -r requirements.txt`

5. Применить миграции

`python manage.py migrate`

6. Запустить сервер

`python manage.py runserver`

Backend будет доступен по адресу
http://127.0.0.1:8000/recipes

### Frontend

1. Перейти в папку frontend

`cd frontend`

2. Установить зависимости

`npm install`

3. Запустить приложение

`npm run dev`

Frontend будет доступен по адресу
http://localhost:5173

## Скриншоты

Здесь будут размещены скриншоты интерфейса приложения.

## Подробная документация 

Документация доступна по [ссылке](https://alexandra2608.github.io/ITMO_ICT_WebDevelopment_2024-2025/).

