# backend
Backend for python flask App

Należy pobrać projekt z repozytorium

````
git clone https://github.com/hanz0pro/backend.git
````

Należy utworzyć sieć 

````
docker network create mynet
````

Uruchomić baze danych 

````
docker run -d \
  --name mydb \
  --network mynet \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=admin \
  -e POSTGRES_DB=tododb \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  postgres:17
````

W folderze z backendem, aby uruchomić backend : 

````
docker build -t myapp-backend-dev ./backend
````

a następnie : 

````
docker run -d \
  --name backend \
  --network mynet \
  -e DATABASE_URL="postgresql://postgres:admin@mydb:5432/tododb" \
  -e JWT_SECRET_KEY="super-secret-key" \
  -e JWT_ACCESS_TOKEN_EXPIRES_MINUTES=15 \
  -e JWT_REFRESH_TOKEN_EXPIRES_DAYS=30 \
  -p 5000:5000 \
  myapp-backend-dev
````

Backend będzie dostępny pod 

````
http://localhost:5000
````