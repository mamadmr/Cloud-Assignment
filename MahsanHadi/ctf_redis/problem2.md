PROBLEM 2

docker run --name ctf_redis -p 6379:6379 -d redis    اجرای کانتینر ردیس

python3 consumer.py      اجرای برنامه برای دریافت پیام ها (منتظر میماند تا برنامه فرستنده اجرا شود)

مانیتور پیام و کلید ها با redis insight

python3 producer.py     اجرای برنامه برای ارسال پیام ها
python3 consumer.py     دریافت پیام ها