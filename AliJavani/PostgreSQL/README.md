docker run --name db-postgres -e POSTGRES_PASSWORD=1234 -d -v postgres_data:/var/lib/postgresql/data postgres
--name = اسم پایگاه داده
-e = پسورد
-d = اینکه تویی پس زمین اجرا بشه 
-v = اون حافظه که داریم بش اختصاص میدیم که اگه کانتینر پاک شد داده درون اون ذخیر بمونن

 https://iutbox.iut.ac.ir/index.php/apps/files/files/12105877?dir=/cloud
