# modern_infrastructure

## Running the up  
Run ```docker build -t gpt_bot .``` in the project directory  
When the image is ready - run  
```docker run --env-file .env -p 80:80 gpt_bot```  
```docker-compose up -d```
```docker-compose up -duild```

``` docker-compose exec bot-telegram-bot-1 bash ```  
 exit ``` Ctrl+D ```   
```docker-compose up -d --build```
```docker-compose down```


## Communication with PostgreSQL DB from command line
```
> docker compose exec postgres /bin/bash
psql -U $POSTGRES_USER -d $POSTGRES_DB -c "SELECT * FROM allowed_users"
psql -U $POSTGRES_USER -d $POSTGRES_DB -c "INSERT INTO allowed_users (user_id) VALUES (-9999999999);"
psql -U $POSTGRES_USER -d $POSTGRES_DB -c "DELETE FROM allowed_users WHERE user_id = -9999999999;"
> Ctrl + D
```  

**DB** ```http://localhost:5005/```