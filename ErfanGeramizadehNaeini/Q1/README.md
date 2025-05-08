``` docker run --rm -d --name pg -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=ERFAN1234 -e POSTGRES_DB=postgres -p 15432:5432 -v pgdata:/var/lib/postgresql/data postgres:14```

POSTGRES_PASSWORD and POSTGRES_USER for the credentials neede for authenticating
-p neede to bind the first port from the host to the docker container.
And -v needed to perssist data that resides in the path specified.
And at last the image is postgres:14
I wrote a python client that I will explain in the recorded video
