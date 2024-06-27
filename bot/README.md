# modern_infrastructure

## Running the up  
Run ```docker build -t gpt_bot .``` in the project directory  
When the image is ready - run  
```docker run --env-file .env -p 80:80 gpt_bot```