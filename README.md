# CineMatch

## Overview

CineMatch is a personal project built with Python to practice API integration, data processing, error handling, and command-line application development.

It helps users discover movies and TV shows by finding similar titles, exploring trending content, and generating random recommendations based on quality filters.

---

## Features

### 1. Find Similar Movies & TV Shows

Search for a movie or TV show and get recommendations based on the selected title.

Users can:

* Choose between movies and TV shows
* Search for a title
* Select a result from the search list
* View similar recommendations
* Explore details of recommended titles

---

### 2. Trending Today

View currently trending movies or TV shows from TMDB.

The application displays popular titles and allows users to view more information about each one.

---

### 3. Surprise Me

Discover something new with random recommendations.

CineMatch generates recommendations using TMDB's discovery system and filters results based on:

* Minimum rating
* Number of votes
* Popularity

This helps provide higher-quality suggestions instead of completely random titles.

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
python cinematch.py
```

## What I Learned

Building this project helped me practice:

- Working with APIs and external data
- Processing JSON responses
- Handling errors and user input
- Managing environment variables securely
- Writing modular Python code
- Designing a command-line application
