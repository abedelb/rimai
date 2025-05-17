
# Docker demo 

1- go to (cd docker-demo )
    1. docker build . -t my-application  // to build you application
    2. docker run -p 8000:8000 my-application  // run your application

2 - go to your browser and hit localhost:8000 // you should get a response from your dockerized application


# Docker compose run services

1 - go to (cd services )
2 - run docker-compose up // it will run 3 applications at once (postges, minio, metabase)
3 - go to http://localhost:9001 // and connect to minio using 'minioadmin' as user and password
4 - go to http://localhost:3000 // you should find metabase and follow instruction to create and setup your account


# Terrafom set up infrastructure

1 - Go to terraform folder
2 - run terraform init // initialize terraform
3 - run terrafrom plan // see the plan that will be applied
4 - run terrafrom apply // apply the state of your infrastructure


# go to src 

1 - create python3 environment 
    - python3 -m venv .venv

2 - source .venv/bin/activate  // activate your environment

3 - pip install -r requirements.txt // install requirements 

4- run your code 
    'python injector.py run'

5 - to clean up your database run 
    'python injector.py reset


