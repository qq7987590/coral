#deploy test pg
docker run --name diveclass -d -p 5432:5432 -e POSTGRES_PASSWORD=123456 -e PGDATA=/data/ -e POSTGRES_USER=admin -e POSTGRES_DB=my_db postgres
#run test pg
#psql --host=127.0.0.1 --username=admin --password --dbname=my_db