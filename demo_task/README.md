# Process analyser  
  
This is a simple application to analyser running processes on **Windows** machine and provide information if their IDs are even or not. Saving this data as JSON.  
  
## Running the application  
1. Ensure that Docker Daemon is running.  
2. Open the terminal in the project folder. *Commands are for PowerShell terminal*  
3. Build Docker Image `docker build -t process-analyser .`  
4. Run Docker: `docker run --rm --pid=host -v /:/hostfs <Path_to_save_JSON>:/app -it process-analyser`, e.g.:  
`docker run --rm --pid=host -v /:/hostfs -v /c/Users/Ivan/Dropbox/pro/Danilveich/modern_infrastructure/demo_task:/app -it process-analyser`  
5. Enjoy your freshly generated JSON!

## Details  
One can provide regexp expression to filter names, to use the expression put the files in files_to_check folder.  
Also, if one would like to filter generated patterns by name with some regular expression, feel free to modify .env file.  
