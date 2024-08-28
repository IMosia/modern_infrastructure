"""
Weeb app with Flask to manage users
"""

import os
import logging
import asyncio

from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from logfmter import Logfmter

formatter = Logfmter(
    keys=["at", "logger", "level", "msg"],
    mapping={"at": "asctime", "logger": "name", "level": "levelname", "msg": "message"},
    datefmt='%H:%M:%S %d/%m/%Y'
)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
enabled_handlers = [stream_handler]

if os.getenv("LOG_TO_FILE", "False").lower() == "true":
    file_handler = logging.FileHandler("./logs/manager.log")
    file_handler.setFormatter(formatter)
    enabled_handlers.append(file_handler)

logging.basicConfig(
    level=logging.INFO,
    handlers=enabled_handlers
)

# Set a higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='templates')
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Health check file path
HEALTH_FILE_PATH = "/tmp/health"


def get_db_connection():
    """Establish a connection to the database."""
    try:
        logger.info("Establishing database connection.")
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=int(os.getenv("DB_PORT"))
        )
        return conn
    except Exception as e:
        logger.error(f"Error establishing database connection: {e}")
        raise

def check_db_health():
    """
    Check if the database connection is healthy.
    """
    try:
        conn = await get_db_connection()
        await conn.fetchval("SELECT 1")
        await conn.close()
        with open(HEALTH_FILE_PATH, "w", encoding="utf-8") as health_file:
            health_file.write("healthy")
        return True
    except Exception as e:
        logger.error("Error checking database health: %s", e)
        if os.path.exists(HEALTH_FILE_PATH):
            os.remove(HEALTH_FILE_PATH)
        return False


@app.route('/')
def index():
    """Render the index page with a list of allowed users."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT au.user_id, ub.balance, ub.images_generated AS images_generated
            FROM allowed_users au
            LEFT JOIN user_balances ub ON au.user_id = ub.user_id
            ORDER BY au.user_id
        """)
        allowed_users = cur.fetchall()
        logger.info("Fetched allowed users successfully.")
        return render_template('index.html', allowed_users=allowed_users)
    except Exception as e:
        logger.error(f"Error fetching allowed users: {e}")
        flash("Could not load allowed users.", 'error')
        return render_template('index.html', allowed_users=[])
    finally:
        logger.info("Closing database connection.")
        cur.close()
        conn.close()


@app.route('/allow', methods=['POST'])
def allow_user():
    """Allow a user to access the bot."""
    user_id = request.form.get('user_id')
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT user_id FROM allowed_users WHERE user_id = %s", (user_id,))
        existing_user = cur.fetchone()
        if existing_user:
            flash(f"User {user_id} is already allowed.", 'info')
        else:
            cur.execute("INSERT INTO allowed_users (user_id) VALUES (%s)", (user_id,))
            conn.commit()
            flash(f"User {user_id} has been allowed.", 'success')
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('index'))


@app.route('/disable', methods=['POST'])
def disable_user():
    """Disable a user from accessing the bot."""
    user_id = request.form.get('user_id')
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT user_id FROM allowed_users WHERE user_id = %s", (user_id,))
        existing_user = cur.fetchone()
        if not existing_user:
            flash(f"User {user_id} is not currently allowed.", 'info')
        else:
            cur.execute("DELETE FROM allowed_users WHERE user_id = %s", (user_id,))
            conn.commit()
            flash(f"User {user_id} access revoked.", 'warning')
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('index'))

@app.route('/set_balance', methods=['POST'])
def set_balance():
    """Set the balance for a user."""
    user_id = request.form.get('user_id')
    balance = request.form.get('balance')
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT user_id FROM allowed_users WHERE user_id = %s", (user_id,))
        existing_user = cur.fetchone()
        if not existing_user:
            flash(f"User {user_id} is not currently allowed.", 'info')
            logger.info(f"User {user_id} is not currently allowed when setting balance.")
        else:
            cur.execute(
                """
                INSERT INTO user_balances (user_id, balance, images_generated)
                VALUES (%s, %s, 0)
                ON CONFLICT (user_id)
                DO UPDATE SET balance = EXCLUDED.balance
                """,
                (user_id, balance)
            )
            conn.commit()
            flash(f"User {user_id} balance has been set to {balance}.", 'success')
            logger.info(f"User {user_id} balance set to {balance}.")
    except Exception as e:
        logger.error(f"Error setting balance for user {user_id}: {e}")
        flash(f"Error setting balance for user {user_id}.", 'error')
    finally:
        logger.info("Closing database connection.")
        cur.close()
        conn.close()
    return redirect(url_for('index'))


@app.route('/health')
def health():
    """
    Health check endpoint.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT 1")
        cur.fetchone()
        return "OK", 200
    except psycopg2.Error as e:
        return f"Error: {str(e)}", 500
    finally:
        cur.close()
        conn.close()

def main():
    logger.info("Checking database connection...")
    loop = asyncio.get_event_loop()
    health_check_passed = loop.run_until_complete(check_db_health())
    if not health_check_passed:
        logger.error("Database connection is not healthy. Exiting.")
        return
    logger.info("Database connection is healthy.")
    app.run(debug=True)

if __name__ == '__main__':
    main()
    
