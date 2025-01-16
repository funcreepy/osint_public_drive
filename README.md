# google_docs

Скрипт позволяет автоматизировать поиск владельцев google документов. Для этого необходимо создать файл urls.txt и выгрузить в него все необходимые URL 
Формат заполнения файла
```
https://docs.google.com/spreadsheets/d/{random_string}
```
Скрипт работает в многопоточном режиме 

Requirements:
В системе должен быть уставноен [xeuledoc](https://github.com/Malfrats/xeuledoc)

# yandex disk 

Скрипт позволяет массово извлечь владельцев файлов в яндекс диске
Строка для запуска

`python3 yandex_disk_owner_extractor.py -o output_file input_file "cookie_string"`

В конце скрипт выдаст файл формата url - owner
