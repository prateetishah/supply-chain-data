## System Architecture:

### API (Python, Flask): 
Handles data processing, business logic, communication with the relational database, and caching.
	Flask-Cache: To cache the backend data.
	SQLite: Relational database to store the dataset.
### Frontend (React): 
To create the web interface for querying the data.
	Axios: To make API requests from the React components to the Flask Backend.
	localStorage: To store data locally in the client’s browser.
	React-Paginate: To paginate the large data.
### Performance Testing (Locust): 
To simulate the user load and assess the system’s performance.
### Web Server (Unicorn): 
To handle concurrent user requests.

## Communication Flow:

1. User interact with React component to select desired filters to query the data.
2. The React component makes API requests using axios to the Flask Backend.
3. Flask API interacts with SQLite database to retrieve the data based on user requests.
4. Backend caches the retrieved data to reduce the database load.
5. API responds to the Frontend. Frontend processes the data and caches in the localStorage/browser’s cache to make the system efficient. Frontend also applies pagination to display the data.
6. Frontend updates the user interface based on the data.

## Data Model:

Resource of Dataset: https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis

Loaded the csv file data into SQLite Database. Developed a command line interface which takes a csv file name as an argument, creates a database in the memory and creates the fields of the table dynamically based on the csv file.

## Technologies Used:

### Backend:
	Python
	Flask
	Flask-Cache
	SQLite
### Frontend:
	React
	Axios
	Local Storage
### Performance Testing:
	Locust
### Web Server:
	Gunicorn

## Local Development Setup:

### Dependencies:
	Python 2.7.18
	Flask 3.0.3
	Flask-Caching 2.1.0
	Flask-Cors 4.0.0
	SQLite3 3.36.0
	React 18.2.0
	axios 1.6.8
	react-paginate 8.2.0
	gunicorn 22.0.0
	locust 2.26.0

### Steps:
1. Clone the repository. (git clone https://github.com/prateetishah/supply-chain-data.git)
2. Navigate to the project directory. (cd supply-chain-data)
3. Install the dependencies.
4. Run the backend to start the server. (python3 main.py)
5. Navigate to frontend directory. (cd frontend)
6. Run the frontend. (npm start)
7. Select the filters from the UI to query the data.
8. Configure the number of workers ing unicorn.config.py file or specify in command line for concurrent user requests. (gunicorn --config gunicorn.conf.py main:app OR gunicorn --config gunicorn.conf.py --workers=3 main:app)
9. Test the performance of the system using locust interface. (locust -f test.py)
