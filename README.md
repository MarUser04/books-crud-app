# Book CRUD App

Simple Book CRUD App that helps you organize the books you have read, the ones you have not and edit them.

## Client

UI built with Angular and Bootstrap.
The app has the following parts:

- `BooksDashboardComponent`, with all the logic and HTML template of the UI.
- `BookService`, services that connects to the API,
- `BookModel`, with the structure of a Book.
- Test files for the component and the service.

## Run the client Locally

- Go to the **client** folder.
- Run `npm install`
- Run `npm start` or `ng serve`(for this you need the [angular-cli](https://github.com/angular/angular-cli))
- The app will be running in `localhost:4200`
- To run the tests you need to run `ng test`.

## Backend

CRUD API built with Python, Flask and some of its features like sqlalchemy.

## Run the API Locally

- Go to the **api** folder.
- You can use a virtual environment like [venv](https://docs.python.org/es/3/library/venv.html).
- Start `venv` using `venv\Scripts\activate` on Windows or `source venv/bin/activate
` on Mac.
- Run `pip install .` to install the dependencies (`requirements.txt`)
- Start the app with `python api.py`
- The app will be running in `localhost:5000`and all the endpoints lives under `/books`. Example: GET `http://localhost:5000/books/b9728cd5f0f14159869ae198f9895845`
- To run the tests run the command `pytest`.

## Docker Compose

The app uses docker compose to manager the container both frontend and backend. Each part of the application has a `Dockerfile` that contains instructions for generating each Docker image.

- The first time run this command in the root folder:  `docker-compose up --build`
- The application will be ready to use in the `localhost:4200`
- Then, you can use `docker-compose up` to starts the container based on the existing image.
