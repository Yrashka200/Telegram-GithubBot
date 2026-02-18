# Telegram-GithubBot

A Telegram bot that showcases your GitHub repositories and contribution graph. Built with Python and the Telegram Bot API.

## Features

- 📁 **Browse GitHub Repositories** - Paginated view of all your public non-fork repositories
- 📊 **Contribution Graph** - View your GitHub contribution calendar directly in Telegram
- 🔄 **Smart Caching** - Repository data cached for 10 minutes to reduce API calls
- 📱 **Interactive Navigation** - Easy-to-use inline keyboards for browsing
- ⚡ **Real-time Data** - Always shows current repository information

### Repository Information Displayed:
- Repository name with link
- ⭐ Star count
- 🧠 Primary programming language
- 📅 Last update date
- 📝 Description

## Commands

- `/start` - Launch the bot and show main menu

## Navigation
```
Main Menu
├── 🚀 Projects - Browse your GitHub repositories
└── 🔥 GitHub Graph - View your contribution calendar
```

```
Projects View (paginated)
├── Repository details
├── 🌍 Open Repo - Direct link to GitHub
├── ⬅ Prev / Next ➡ - Navigate between repos
└── 🔙 Back - Return to main menu
```


## Requirements

- Python 3.7 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- GitHub account (public repositories will be displayed)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Yrashka200/Telegram-GithubBo.git
cd Telegram-GithubBo
```


## 2. Install Dependencies
``` bash
pip install pyTelegramBotAPI requests
```

## 3. Get Your Telegram Bot Token
- Open Telegram and search for @BotFather 
- Send /newbot command
- Follow the instructions to create your bot
- Copy the bot token provided

## 4. Configure the Bot
Edit bot.py and set your credentials:
```

``bash
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"        # Replace with your bot token
GITHUB_USERNAME = "YOUR_GITHUB_USERNAME_HERE"  # Replace wit your GitHub username
```

## 5. Run the Bot
```bash
python bot.py
```

## How It Works
- Repository Fetching: When you access Projects, the bot fetches your public repositories from GitHub API
- Caching: Results are cached for 10 minutes to improve performance and respect API limits
- Pagination: Repositories are displayed one at a time with navigation buttons


``` Project Structure
text
GithubBot/
├── bot.py          # Main bot application
└── README.md       # This file
```

### Made by *Yrashka200*
