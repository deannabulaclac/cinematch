# CineMatch

A command-line movie and TV show recommendation application powered by **The Movie Database (TMDB) API**.

## Overview

CineMatch is a Python-based application designed to help users discover movies and TV shows based on their interests. Instead of searching endlessly for something to watch, users can find similar titles, explore trending content, or receive random recommendations based on highly rated titles.

The project focuses on practicing API integration, data processing, error handling, and building a user-friendly command-line application.

---

## Features

### Find Similar Movies & TV Shows

Search for a movie or TV show and get recommendations based on the selected title.

Users can:

* Choose between movies and TV shows
* Search for a title
* Select a result from the search list
* View similar recommendations
* Explore details of recommended titles

---

### Trending Today

View currently trending movies or TV shows from TMDB.

The application displays popular titles and allows users to view more information about each one.

---

### Surprise Me

Discover something new with random recommendations.

CineMatch generates recommendations using TMDB's discovery system and filters results based on:

* Minimum rating
* Number of votes
* Popularity

This helps provide higher-quality suggestions instead of completely random titles.

---

### Title Information

For every selected movie or TV show, CineMatch displays:

* Title
* Type (Movie/TV Show)
* Genres
* Release date
* Rating
* Language
* Overview

Users can also open the poster image directly in their browser.

---

## Technologies Used

* **Python 3**
* **TMDB API**
* `requests` — API requests
* `python-dotenv` — environment variable management
* `pyfiglet` — command-line banner
* `webbrowser` — poster preview
* `random` — random recommendations

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/cinematch.git
cd cinematch
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your TMDB API key

Create a `.env` file in the project directory:

```env
TMDB_API_KEY=your_api_key_here
```

You can get your API key from [The Movie Database (TMDB)](https://www.themoviedb.org/).

### 4. Run the application

```bash
python project.py
```

---

## Project Structure

```
cinematch/
│
├── project.py          # Main application
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── .gitignore          # Ignored files
├── LICENSE             # MIT License
└── README.md           # Documentation
```

---

## How It Works

CineMatch communicates with the TMDB API to retrieve movie and TV show information.

The application uses different API endpoints to:

* Search for movies and TV shows
* Retrieve similar titles
* Display trending content
* Generate random recommendations
* Load genre information

Since TMDB uses different response formats for movies and TV shows, helper functions are used to normalize data such as:

* Movie titles (`title`) and TV titles (`name`)
* Movie release dates (`release_date`) and TV release dates (`first_air_date`)

This allows the application to handle both media types consistently.

---

## Design Decisions

### Modular Function Design

The application is separated into multiple functions, each responsible for a specific task:

* API communication
* Searching titles
* Formatting information
* Displaying recommendations
* Handling user interaction

This makes the code easier to understand, maintain, and expand.

### Secure API Key Management

Instead of storing the API key directly in the source code, CineMatch uses environment variables through `.env`.

This prevents sensitive credentials from being accidentally exposed when sharing the project publicly.

### Quality-Based Recommendations

The random recommendation feature uses TMDB filters such as rating and vote count to avoid suggesting low-quality titles.

---

## Future Improvements

Possible improvements for future versions:

* Add a favorites/watchlist feature
* Save user preferences
* Add genre and language filters
* Create a graphical user interface
* Add streaming availability information
* Build a web version using a framework such as Flask or Django

---

## Acknowledgements

Movie and TV show information is provided by:

**The Movie Database (TMDB)**
https://www.themoviedb.org/

CineMatch is not affiliated with or endorsed by TMDB.

---

## License

This project is licensed under the **MIT License**.
