# modern_infrastructure

## Running the up  
Run ```docker build -t gpt_bot .``` in the project directory  
When the image is ready - run  
```docker run --env-file .env -p 80:80 gpt_bot```  
```docker-compose up -d```
```docker-compose up -duild```

# docker-compose exec bot-telegram-bot-1 bash
# exit or Ctrl+D
# docker-compose up -d --build
# docker-compose down