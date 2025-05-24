##  ویژگی‌ها

* استفاده از FastAPI برای طراحی REST API
* Celery + Redis برای پردازش وظایف در پس‌زمینه
* PostgreSQL به‌عنوان پایگاه‌داده
* ذخیره‌سازی داده فقط در صورت موفقیت آمیز بودن تسک Celery
* حذف کانتینرها به‌صورت ایمن
* بازگرداندن آدرس منحصربه‌فرد هر کانتینر (IP/PORT)

---

##  ساختار پروژه

```
project/
├── .env                   
├── Dockerfile             
├── docker-compose.yml      
├── requirements.txt        
└── app/
    ├── main.py             
    ├── tasks.py           
    ├── database.py        
    └── models.py         
```

---

## 📡 APIها

### 🎯 ساخت کانتینر

```http
POST /create
```

📥 پاسخ:

```json
{
  "message": "Container is being created",
  "task_id": "...",
  "container_name": "ctf_container_ab12",
  "ip": "172.18.0.X",
  "port": 1337
}
```

---

### ❌ حذف کانتینر

```http
DELETE /delete/{container_name}
```

📥 پاسخ:

```json
{ "message": "Container deleted successfully" }
```

---

### 🔄 بررسی وضعیت Task

```http
GET /task/{task_id}
```

📥 پاسخ:

```json
{
  "status": "SUCCESS",
  "result": {
    "ip": "172.18.0.X",
    "port": 1337
  }
}
```
