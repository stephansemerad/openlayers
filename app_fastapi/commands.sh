python -m venv venv      
venv\scripts\activate

python -m pip install uvicorn
python -m pip install fastapi
python -m pip install jinja2
python -m pip install sqlalchemy
python -m pip install psycopg2-binary

python -m pip install --upgrade pip

python -m pip freeze > requirements.txt
python -m pip install -r requirements.txt


uvicorn main:app --reload --host 0.0.0.0 --port 5000
curl http://localhost:5000/ # Should show {"message":"Hello World"}

docker build -t app_fastapi .
docker run -d --name app_fastapi -p 8080:5000 app_fastapi
docker ps
curl http://localhost:8080/ # Should show {"message":"Hello World"}

docker stop  app_fastapi    
docker rm  app_fastapi    
docker ps

docker image prune -f
docker container prune -f

