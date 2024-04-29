# Process analyser  
  
This is a simple application to analyser running processes on **Windows** machine and provide information if their IDs are even or not. Saving this data as JSON.  
  
## Running the application  
1. Ensure that Docker Daemon is running.  
2. Open terminal in the project folder. *Commands are for PowerShell terminal*  
3. Build Docker Image `docker build -t process-analyser .`  
4. Run Docker: `docker run --rm -v /:/hostfs <Path_to_save_JSON>:/app process-analyser`, e.g.:  
`docker run --rm -v /:/hostfs -v /c/Users/Ivan/Dropbox/pro/Danilveich/demo_task:/app process-analyser`  
5. Enjoy your freshly generated JSON!




