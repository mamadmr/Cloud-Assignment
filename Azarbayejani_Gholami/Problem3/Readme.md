sh
docker run -d \
--name redis \
-p 6379:6379 \
--network ctf-net \
redis:latest     
```  

# ساخت ایمیج برای Celery Worker      
```bash
docker build -f Dockerfile.worker -t celery_worker_i .

```

# ساخت ایمیج برای Celery Tester (کلاینت تست)   
 
```bash
docker build -f Dockerfile.test -t celery_test_i .
```
# اجرای کانتینر celery_worker_c 

```bash
docker run -d \
--name celery_worker_c \
-v /var/run/docker.sock:/var/run/docker.sock \
--restart=always \
--network ctf-net \
celery_worker_i
```  
       
# اجرای کانتینر تست (Tester)  

```bash
docker run -d \
--name celery_tester \
-v /var/run/docker.sock:/var/run/docker.sock \
--restart=no \
--network ctf-net \
worker_test_i
```        

# ساخته شدن و حذف شدن کانتینر جدید
(![images](3_1.jpg))
(![images](3_2.jpg))
# لاگ کانتینر ها
(![images](3_3.jpg))
(![images](3_4.jpg))
