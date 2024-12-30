# control
Приложение для управления оборудованием

## Назначение приложения

Моделирование решений для реальных АСУ ТП

## Сервер сообщений (alarm_server)

### Функции

- получение данных от сервера
- создание сообщения в зависимости от значения сигнала
- запись сообщения в базу данных

### Компоненты

alarm.db - база данных сообщений.

### Алгоритмы работы



## Сервер имитационной модели (data_simulator)

### Функции

- получение данных от клиента
- отправка данных клиенту
- сохранение данных

### Компоненты

sim.db - база конфигурации, значений, сообщений
db.py - класс для работы с базой данных

- создание баз данных
- создание тестовых данных
- создание конфигурационных данных 

server.py - предоставление интерфейсов для работы с базой данных через socket
client.py - имитатор получения данных

## Клиент

### Функции

- запрос данных от сервера
- отправка данных в сервер