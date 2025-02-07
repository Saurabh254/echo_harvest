# Playerctl Monitoring Tool  

## Overview  
The **Playerctl Monitoring Tool** is a real-time media player tracking system that listens to **Playerctl** events, stores playback activity in a **PostgreSQL** database, and broadcasts updates via **WebSockets**. This tool enables seamless media monitoring, allowing applications to react to media playback changes dynamically.  

It is designed for use cases such as:  
- **Media Player Analytics** – Track playback history, song changes, and player status.  
- **Live Dashboards** – Display real-time media activity on user interfaces.  
- **Event-Driven Integrations** – Automate actions based on media events, such as pausing music when receiving a call.  

This project leverages:  
- **SQLAlchemy** for database management  
- **Alembic** for schema migrations  
- **Redis** for caching and event distribution  
- **WebSockets** for real-time event publishing  

## Features  
- Tracks media player activity (play, pause, stop, track change, etc.)  
- Stores event data in a PostgreSQL database  
- Uses Redis for caching and efficient event handling  
- Publishes real-time updates via WebSockets  

## Technologies Used  
- **Python** – Core language  
- **SQLAlchemy** – ORM for PostgreSQL  
- **Alembic** – Database migrations  
- **Redis** – For event distribution and caching  
- **PostgreSQL** – Database for storing player activity  
- **Playerctl** – CLI tool for controlling media players  

## Usage  
- The tool listens for Playerctl events and logs them in PostgreSQL.  
- Real-time media events are published via WebSockets for external applications to consume.  

## License  
MIT License  

---

Let me know if you need more refinements! 🚀
