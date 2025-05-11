Videos on iutbox: 
https://iutbox.iut.ac.ir/index.php/s/75FQo3fm87nFnNP

 
 
 (a):


    i) sudo docker run --name my-postgres -e POSTGRES_PASSWORD=1234 -d docker.arvancloud.ir/postgres


        --name my-postgres: names the container.
        -e POSTGRES_PASSWORD=1234: sets the default password for the postgres user.
        -d: runs the container in the background.
        docker.arvancloud.ir/postgres: pulls the PostgreSQL image from ArvanCloud’s registry instead of Docker Hub




    ii)
    - docker volume create pgdata
        Creates a named Docker volume called pgdata to store database files persistently.


    - sudo docker network create --subnet=172.25.0.0/16  custom-net
        Creates a custom bridge network with a fixed subnet.
        Useful for assigning static IPs to containers, which helps in CTF setups.


    - sudo docker run --name my-postgres-persistent   --network custom-net   --ip 172.25.0.10   -e POSTGRES_PASSWORD=1234   -v pgdata:/var/lib/postgresql/- - data   -p 55432:5432   -d docker.arvancloud.ir/postgres






 
(b):
    i) sudo docker exec -it my-postgres-persistent psql -U postgres
        Opens an interactive terminal (-it) inside the running PostgreSQL container.
        Runs the psql CLI as the postgres user.
        Allows you to run SQL commands directly in the container.




