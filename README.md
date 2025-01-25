# Flask Movie Web App

A Flask-based web application for managing users and their favorite movies. This project integrates with the OMDB API to fetch movie details and stores user data in a SQLite database.

## Features

- **User Management**: Add, list, and delete users.
- **Movie Management**: Add, update, and delete movies from a user's favorite list.
- **API Integration**: Fetch movie details (e.g., director, year, and IMDb rating) from the OMDB API.
- **Error Handling**: Custom error pages for 404 and 500 errors.

## Technologies Used

- **Backend**: Flask
- **Database**: SQLite
- **API**: OMDB API
- **Environment Management**: Python `dotenv`

## Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:masterschool-weiterbildung/moviweb_app.git
   cd moviweb_app
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the `.env` file:
   - Create a `.env` file in the project root.
   - Add your OMDB API key:
     ```
     key=your_omdb_api_key
     ```

5. Run the application:
   ```bash
   python app.py
   ```

## Project Structure

```
flask-movie-webapp/
├── datamanager/              # Interface and Implmentation
├── instance/
│   └── moviwebapp.db         # SQLite database
├── templates/                # HTML templates
├── static/                   # Static files (CSS, JS)
├── models.py                 # SQLAlchemy models
├── app.py                    # Flask application
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
└── README.md                 # Project documentation
```

## API Integration

The application uses the OMDB API to fetch movie details:
- Endpoint: `https://www.omdbapi.com/`
- Response includes director, year, and IMDb rating.

## Error Pages

- **404**: Custom page for not found errors.
- **500**: Custom page for server errors.

## Author

Jerome de Dios
