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





