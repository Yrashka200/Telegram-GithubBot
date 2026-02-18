
import time
import logging
import requests
from datetime import datetime, timedelta, UTC
import telebot
from telebot import types

# CONFIG 

BOT_TOKEN = "PUT_YOUR_BOT_TOKEN_HERE"
GITHUB_USERNAME = "YOUR_GITHUB_USERNAME_HERE" 

if BOT_TOKEN == "PUT_YOUR_BOT_TOKEN_HERE":
    raise ValueError("Please set your BOT_TOKEN inside the script.")

logging.basicConfig(level=logging.INFO)
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")



github_cache = {
    "repos": None,
    "expires": datetime.now(UTC)
}

CACHE_TIME = timedelta(minutes=10)

def fetch_repos():
    if github_cache["repos"] and datetime.now(UTC) < github_cache["expires"]:
        return github_cache["repos"]

    try:
        url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"
        repos = requests.get(url, timeout=10).json()
        repos = [r for r in repos if not r["fork"]]

        github_cache["repos"] = repos
        github_cache["expires"] = datetime.now(UTC) + CACHE_TIME
        return repos

    except Exception as e:
        logging.error(e)
        return []



user_sessions = {}

def get_session(user_id):
    if user_id not in user_sessions:
        user_sessions[user_id] = {"page": 0}
    return user_sessions[user_id]



def main_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🚀 Projects", callback_data="projects"))
    markup.add(types.InlineKeyboardButton("🔥 GitHub Graph", callback_data="graph"))
    return markup

def pagination_keyboard(repo_name=None):
    markup = types.InlineKeyboardMarkup(row_width=2)

    if repo_name:
        markup.add(
            types.InlineKeyboardButton(
                "🌍 Open Repo",
                url=f"https://github.com/{GITHUB_USERNAME}/{repo_name}"
            )
        )

    markup.add(
        types.InlineKeyboardButton("⬅ Prev", callback_data="prev"),
        types.InlineKeyboardButton("Next ➡", callback_data="next")
    )

    markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="back"))
    return markup



@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        f"👋 Welcome!\nGitHub Portfolio Bot for *{GITHUB_USERNAME}*",
        reply_markup=main_keyboard()
    )



@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    session = get_session(call.from_user.id)
    repos = fetch_repos()

    if call.data == "projects":
        session["page"] = 0

    elif call.data == "next":
        session["page"] += 1

    elif call.data == "prev":
        if session["page"] > 0:
            session["page"] -= 1

    elif call.data == "graph":
        try:
            graph_url = f"https://github.com/users/{GITHUB_USERNAME}/contributions"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(graph_url, headers=headers, timeout=10)

            if response.status_code == 200:
                bot.send_document(
                    call.message.chat.id,
                    ("github_graph.svg", response.content),
                    caption="🔥 Official GitHub Contribution Graph"
                )
            else:
                bot.send_message(call.message.chat.id, "⚠️ Failed to load GitHub graph.")

        except Exception as e:
            logging.error(f"Graph error: {e}")
            bot.send_message(call.message.chat.id, "⚠️ Graph temporarily unavailable.")

        return

    elif call.data == "back":
        bot.edit_message_text(
            "Main Menu 👇",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=main_keyboard()
        )
        return

    if not repos:
        bot.answer_callback_query(call.id, "No repositories found")
        return

    index = session["page"] % len(repos)
    repo = repos[index]

    text = (
        f"🚀 *{repo['name']}*\n\n"
        f"⭐ Stars: {repo['stargazers_count']}\n"
        f"🧠 Language: {repo['language'] or 'Unknown'}\n"
        f"📅 Updated: {repo['updated_at'][:10]}\n\n"
        f"_{repo['description'] or 'No description'}_"
    )

    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=pagination_keyboard(repo['name']),
        disable_web_page_preview=True
    )



def run():
    while True:
        try:
            print("Bot started...")
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print("Restarting...", e)
            time.sleep(5)

if __name__ == "__main__":
    run()
