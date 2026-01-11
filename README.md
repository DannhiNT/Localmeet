# LocalMeet

LocalMeet is a community-driven web application that allows local residents and organizations to create, discover, and manage events happening in a specific area. Users can browse events, view details, and register interest, helping hosts better estimate attendance and coordinate logistics.

## Features (open for development)

- Create and manage local events
- Browse upcoming events in the community
- User registration and interest tracking
- Email notifications after registration closes
- Simple and lightweight setup using SQLite

## Tech Stack

- **Backend**: Python, Flask
- **Database**: SQLite
- **Environment Management**: `venv`, `python-dotenv`, `flaskenv`
- **ORM**: Flask-SQLAlchemy (if applicable)

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/DannhiNT/Localmeet.git
cd LocalMeet
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\\Scripts\\activate  # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env`file in the root directory to store OAuth Secrets:

```env
SECRET_KEY=your_secret_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
OAUTHLIB_INSECURE_TRANSPORT=1
```

Create a `.flaskenv` file:

```env
FLASK_DATA_FILE="local-meet"
```

## Running the Application

```bash
flask --app localmeet run --debug
```

The app will be available at:

```
http://127.0.0.1:5000/events
```

or

```
http://localhost:5000/events
```

## Database

- Uses **SQLite** for local development
- Database file: `local-meet.sqlite3`

## Future Improvements

- Event categories and tags
- Location-based search and filtering
- Admin dashboard for event moderation
- Production deployment (Docker / Cloud)

## License

This project is licensed under the MIT License.

## Ownership

This project was created and is maintained by Nhi Nguyen (Justine). All contributions are welcome, and ownership remains with the original author.

## Acknowledgements

Built as a learning and community-focused project to explore Flask, backend development, and event-driven applications.
