# Library
School final project  
Frontend and design: [nicovuka](https://github.com/nicovuka), [curryx04](https://github.com/curryx04)
Backend and project architecture: [knamroud](https://github.com/knamroud)
## Requirements
You need nothing but Docker to run this project.   
## Deployment
To run the project, edit the .env file as you wish and after installing docker run  
```bash
./scripts/start.sh
```
The scripts are made to run on any Unix-like system using bash.  
To run on Windows, create an `init/init.sql` file containing:  
```bash
GRANT USAGE ON \`$DB_NAME\`.* TO \`$DB_USER\`@localhost;  
GRANT CREATE ON \`$DB_NAME\`.* TO \`$DB_USER\`@localhost;  
```
And run `docker-compose up`  