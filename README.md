# 🚗 Car Parts SPA

Single Page Application для управления иерархией деталей автомобиля с расчетом стоимости и экспортом в Excel/PDF.

---

## 📌 Функционал

* 📊 Древовидная структура деталей (без ограничений вложенности)
* ➕ Добавление / ✏️ редактирование / 🗑 удаление
* 🧮 Автоматический расчет стоимости:

  * Лист: `price * quantity`
  * Родитель: сумма дочерних элементов
* 📤 Экспорт:

  * Excel (.xlsx)
  * PDF (.pdf)
* ⚡ SPA (без перезагрузки страницы)

---

## 🏗 Архитектура

Проект разделен на:

* **Frontend**: Vue 3 + Pinia + Vite
* **Backend**: FastAPI + SQLAlchemy
* **DB**: PostgreSQL
* **Infrastructure**: Docker + Nginx

---

## 🔗 Взаимодействие

```text
Frontend (Vue) → /api → Nginx → Backend (FastAPI) → PostgreSQL
```

* Frontend не знает реальный адрес backend
* Все запросы идут через `/api` (nginx proxy)

---

## 📂 Структура проекта

```text
spa-test/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   ├── repositories/
│   │   └── core/
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── store/
│   │   └── router/
│   ├── nginx.conf
│   └── Dockerfile
│
├── docker-compose.yml
└── README.md
```

---

## 🚀 Запуск проекта

### 🔧 Требования

* Docker
* Docker Compose

---

### ▶️ Запуск

```bash
docker compose up -d --build
```

---

### 🌐 Доступ

* Frontend: http://localhost
* Backend API: http://localhost/api
* Swagger: http://localhost:8000/docs

---

## ⚙️ Основные API

| Метод  | Endpoint      | Описание        |
| ------ | ------------- | --------------- |
| GET    | /parts        | Получить дерево |
| POST   | /parts        | Создать деталь  |
| PATCH  | /parts/{id}   | Обновить        |
| DELETE | /parts/{id}   | Удалить         |
| GET    | /export/excel | Скачать Excel   |
| GET    | /export/pdf   | Скачать PDF     |

---

## 🧠 Бизнес-логика

Расчет стоимости выполняется на backend:

```python
if part.children:
    total = sum(child.total for child in children)
else:
    total = price * quantity
```

Frontend только отображает готовые данные.

---

## 📄 Экспорт

### Excel

* Табличный формат
* Индексация (1, 1.1, 1.1.1)
* Границы и стили

### PDF

* Таблица
* Unicode-шрифт (DejaVuSans)
* Поддержка кириллицы

---

## 🐳 Docker

### Сервисы

* `db` — PostgreSQL
* `backend` — FastAPI
* `frontend` — Nginx + Vue build

---

## 🧪 Тесты

```bash
docker compose run tests
```

---

## 🧩 Особенности реализации

* Рекурсивное построение дерева
* Защита от циклов (нельзя сделать родителя потомком)
* Валидация данных
* Разделение слоев:

  * Repository
  * Service
  * API

---

## 🧠 Почему так сделано

* Backend — источник истины (расчеты)
* Frontend — только UI
* Nginx — проксирование API
* Docker — единая среда запуска

---

## 📈 Возможные улучшения

* Drag & Drop структуры
* Inline редактирование
* Авторизация
* Кэширование
* WebSocket обновления

---

## 👨‍💻 Автор

Тамерлан Хасенов

---
