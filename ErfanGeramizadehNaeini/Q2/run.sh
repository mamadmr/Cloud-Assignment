docker run -d --name rds -p 6390:6379 redis:7.0
# redis-cli -h localhost -p 6390 ping for making sure it works