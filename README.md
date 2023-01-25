### Парсер категории "Смартфоны" на сайте shop.kz и предоставление доступа по API

Скрипты можно использовать оп отдельности. К примеру, если запустить parser.py, то он спарсит все смартфоны и сохранит в smartphones.json. После этого можно запустить api.py и можно получить цены примерно по следующей ссылке http://127.0.0.1:8000/smartphones?price=539990

#### Использование без docker
Устанавливаем зависимости
```
pip install -r requirements.txt
```
и запускаем скрипты
```
python3 /app/parser.py
```
```
python3 /app/api.py
```
___
#### Использование с docker
* Docker engine должен быть установлен на вашей ОС

Собираем образ. Если не хватает прав, запускаем через **root** или **sudo**
```
sudo docker build -t shop_kz .
```
Запускаем контейнер на основе созданного образа
```
sudo docker run -d --name mycontainer -p 80:80 shop_kz
```
Если контейнер не запустился
```
sudo docker ps -a
```
копируем id нашего контейнера и запускаем его вручную
```
sudo docker run id_контейнера
```
После этого переходим по ссылку http://127.0.0.1/docs
