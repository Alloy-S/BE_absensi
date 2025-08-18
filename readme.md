## Command to Run 

python -m venv be_absensi

source ./be_absensi/Scripts/activate

pip install -r requirements.txt
~~
## Command DB Migration

flask db init

flask db migrate -m "Initial migration"

flask db upgrade

## docker
docker-compose up --build

docker-compose up

docker-compose down

### untuk init db
docker-compose exec web flask db upgrade

### server
docker compose exec web flask db upgrade

### SSL
docker compose run --rm --entrypoint "\
  certbot certonly --webroot -w /var/www/certbot \
  --non-interactive --agree-tos \
  --email email@anda.com \
  -d mybenz.site -d www.mybenz.site" certbot


### migration db

pg_dump -U NAMA_USER_LOKAL -d NAMA_DB_LOKAL -F c -b -v -f data_lokal.dump

scp .\data_lokal.dump username@ip:~/

docker cp ../data_lokal.dump benz-absensi-db:/tmp/data_lokal.dump

docker compose exec db pg_restore -U NAMA_USER_SERVER -d NAMA_DB_SERVER --clean --no-acl --no-owner /tmp/data_lokal.dump

