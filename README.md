# xberry-task
Potential improvements:
 1. I realized later on maybe I should have separated the API from the interface, instead rendering templates, I wanted to later but I ran out of time
 2. 2 of the tests fail, cause I couldn't set up Celery on the test env correctly, I tried to mock it but failed, tried to build all the containers and then run test, but failed
 3. I was wondering if maybe I should return a task id and set up an endpoint for checking task status and then getting it, but I wasn't sure
 
1. **Clone the Repository**

  Open your terminal and run the following command to clone the repository:
  ```bash
  git clone https://github.com/jwojci/xberry-task/
  cd url_shortener
  ```
2. **Create a .env file in the root of your project directory with the following variables:**
  ```bash
  DB_URL = "postgresql://postgres:password@db:5432/xberrytask"
  BASE_URL = "http://localhost:8000"
  REDIS_BROKER_URL = "redis://redis:6379/0"
  REDIS_BACKEND_URL = "redis://redis:6379/0"
  ```
3. **Build and start the application**
  ```bash
  docker-compose up --build
  ```
5. **Then navigate to http://localhost:8000 or whatever url you specified in your .env BASE_URL**

6. **To run tests:**
   ```bash
   docker-compose run test
   ```


