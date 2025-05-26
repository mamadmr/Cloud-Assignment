PROBLEM 1

docker volume create persistent_data    ساخت volume برای ذخیره دائمی داده ها

docker run --name ctf_postgres \    نام کانتینر
  -e POSTGRES_USER=mahsan \     نام کاربر دیتابیس
  -e POSTGRES_PASSWORD=mahsan \     پسورد کاربر
  -e POSTGRES_DB=ctf \      نام دیتابیس
  -v ctf_postgres:/var/lib/postgresql/data \    تعیین volume برای ذخیره دائم داده های دیتابیس 
  -p 5432:5432 \    تعیین پورت
  -d postgres      اجرا در پس زمینه

docker exec -it ctf_postgres psql -U mahsan -d ctf    اتصال به دیتابیسی که ساختیم با کاربری که تعریف کردیم در کانتینر

CREATE TABLE sample_table (
  name VARCHAR(50) PRIMARY KEY
);

INSERT INTO sample_table (name) VALUES
('Mahsan'),
('Hadi');

SELECT * FROM sample_table;

docker stop ctf_postgres
docker rm ctf_postgres
