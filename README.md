# Ttronics - monitoring

---

Сервис управления устройствами и батареями с REST API, документацией и готовым окружением через Docker.

---

## Установка и запуск через Docker

### 1. Клонируйте репозиторий:
```bash
git clone https://github.com/S1immer/ttronic
```

Перейдите в папку проекта:
```bash
cd ttronics_api
```
Скопируйте шаблон настроек:
```bash
cp .env.example .env
```
Перейдите в файл .env и подставьте в DATABASE_URL валидный URL: 
```
postgresql+asyncpg://postgres:password@db:5432/ttronics_db 
```
### 2. Запустите:
Запуск:
```bash
docker-compose up --build -d
```
Остановить:
```bash
docker-compose down
```
Просмотр логов:
```bash
docker-compose logs -f
```
---

##### API будет доступен по адресу - http://127.0.0.1:8000
##### Swagger документация - http://127.0.0.1:8000/docs
##### pgAdmin - http://127.0.0.1:5050

---
**Зайти в базу данных можно следующим способом:**
##### 1. Откройте pgAdmin в браузере.
- Перейдите по адресу - http://127.0.0.1:5050

##### 2. Откройте pgAdmin в браузере.
**Данные для входа в pgAdmin:** 
- **Email:** admin@admin.com
- **Password:** admin

##### 3. Подключите сервер PostgreSQL в pgAdmin:
1. Нажмите **Add New Server**.
2. На вкладке General → **Name:** ttronics-db.
3. На вкладке Connection:
    - **Host name/address:** db
    - **Port:** 5432
    - **Maintenance DB:** ttronics_db
    - **Username:** postgres
    - **Password:** password
4. Нажмите **save**.
    - Теперь в левом дереве появится сервер и база — можно открывать Tables, правой кнопкой → View/Edit Data → All Rows.

---

## API Эндпоинты

### Устройства:
- `GET /device` - список устройств
- `POST /devices` - создать устройство
- `GET /devices/{device_id}` - получить устройство
- `PUT /devices/{device_id}` - обновить устройство
- `DELETE /devices/{device_id}` - удалить устройство

### АКБ:
- `GET /batteries` - список АКБ
- `POST /batteries` - создать АКБ
- `GET /batteries/{battery_id}` - получить АКБ
- `PUT /batteries/{battery_id}` - обновить АКБ
- `DELETE /batteries/{battery_id}` - удалить АКБ

### Привязка АКБ:
- `POST /batteries/{battery_id}/attach/to/{device_id}` - привязать АКБ к устройству
- `POST /batteries/{battery_id}/detach/from/{device_id}` - отвязать АКБ от устройства

___

## Описание проекта:

**Сервис имитирует работу системы управления батареями:**
- устройства могут иметь до 5 батарей
- можно привязывать / отвязывать батареи
- CRUD операции для всех сущностей
- удобный просмотр таблиц через pgAdmin