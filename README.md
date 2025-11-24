# Free Fire API - Python Edition

A comprehensive FastAPI-based REST API wrapper for accessing Free Fire game data including player statistics, account information, guild details, and more.

## Features

- 🎮 Player statistics (K/D ratio, matches, wins, kills)
- 👤 Account information (nickname, level, profile)
- 🏰 Guild/Clan information
- 🗺️ Craftland profile data
- ❤️ Send likes to players
- 📚 Interactive API documentation (Swagger UI)
- 🌍 Multi-region support (14+ regions)

## Quick Start

### 1. Installation

The dependencies are already installed via `uv`. Make sure you have Python 3.11+ installed.

### 2. Configuration (Optional)

For features requiring API keys (like sending likes), create a `.env` file:

```bash
cp .env.example .env
