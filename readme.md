Запустить сервисы: `docker-compose up`
Тестовые запросы:

```
    curl -X GET http://localhost:5000/?url=https://www.ozon.ru/category/smartfony-15502/
    curl -X GET http://localhost:5000/?url=https://www.ozon.ru/category/umnye-chasy-15516/
```

Вывод данных из топика `ozon-products`:

```
docker-compose exec broker kafka-console-consumer --topic ozon-products --bootstrap-server broker:9092 --from-beginning
```
