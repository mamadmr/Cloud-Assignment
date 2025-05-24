sh
    docker exec -it first-container psql -U myuser -d mydb
   ```
# ایجاد volume  
```bash
docker volume create pgdata
```       
# اجرای کانتینر  
```bash
docker run --name first-container `
-e POSTGRES_PASSWORD=123 `
-e POSTGRES_USER=myuser `
-e POSTGRES_DB=mydb `
-v pgdata:/var/lib/postgresql/data `
-p 5432:5432 `
-d postgres
```   
# توقف و حذف کانتینر 
```bash
docker stop pg-container
docker rm pg-container
```

# فیلم مربوطه               
```bash
https://iutbox.iut.ac.ir/index.php/s/JwnAZfK7be9AesA
```



