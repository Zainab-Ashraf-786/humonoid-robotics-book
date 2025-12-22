import os
import logging
from typing import Optional, List, Dict
from datetime import datetime
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import aiosqlite
import urllib.parse

# Load environment variables to check the setting
load_dotenv()
# Disable database functionality - will be set from environment
DISABLE_DATABASE = os.getenv("DISABLE_DATABASE", "True").lower() in ("true", "1", "yes", "on")

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global database instance
db_manager: Optional['DatabaseManager'] = None

class DatabaseManager:
    """
    Async database manager supporting both PostgreSQL and SQLite
    """

    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        if not self.database_url:
            raise ValueError("DATABASE_URL must be set in environment variables")

        # Determine database type from URL
        self.is_sqlite = self.database_url.startswith('sqlite://')

        # Connection pool for PostgreSQL or connection for SQLite
        self.pool = None
        self.db_path = None

        if self.is_sqlite:
            # Extract file path from SQLite URL
            self.db_path = self.database_url.replace('sqlite:///', '')

    def _get_query_params(self, query: str):
        """
        Convert PostgreSQL-style ($1, $2, etc.) to SQLite-style (?)
        """
        if self.is_sqlite:
            # Replace $1, $2, $3, etc. with ?
            import re
            return re.sub(r'\$\d+', '?', query)
        return query

    def _execute_query(self, conn, query: str, *params):
        """
        Execute a query with the appropriate parameter style
        """
        if self.is_sqlite:
            return conn.execute(query, params)
        else:
            return conn.execute(query, *params)

    def _execute_many_query(self, conn, query: str, params_list):
        """
        Execute a query multiple times with different parameters
        """
        if self.is_sqlite:
            return conn.executemany(query, params_list)
        else:
            return conn.executemany(query, params_list)

    async def _fetch_one(self, conn, query: str, *params):
        """
        Fetch one row from query results
        """
        query = self._get_query_params(query)
        if self.is_sqlite:
            cursor = await conn.execute(query, params)
            return await cursor.fetchone()
        else:
            return await conn.fetchrow(query, *params)

    async def _fetch_all(self, conn, query: str, *params):
        """
        Fetch all rows from query results
        """
        query = self._get_query_params(query)
        if self.is_sqlite:
            cursor = await conn.execute(query, params)
            return await cursor.fetchall()
        else:
            return await conn.fetch(query, *params)

    async def _fetch_val(self, conn, query: str, *params):
        """
        Fetch a single value from query results
        """
        query = self._get_query_params(query)
        if self.is_sqlite:
            cursor = await conn.execute(query, params)
            row = await cursor.fetchone()
            return row[0] if row else None
        else:
            return await conn.fetchval(query, *params)

    async def initialize(self):
        """
        Initialize the database connection
        """
        if DISABLE_DATABASE:
            logger.info("⚠️ Database disabled. Skipping DB initialization.")
            return

        try:
            if self.is_sqlite:
                # For SQLite, we just test the connection by opening and closing
                async with aiosqlite.connect(self.db_path) as db:
                    await db.execute("SELECT 1")
                    logger.info("SQLite database connection test successful")
            else:
                # For PostgreSQL
                import asyncpg
                self.pool = await asyncpg.create_pool(
                    dsn=self.database_url,
                    min_size=1,  # Reduced min size for development
                    max_size=10,  # Reduced max size for development
                    command_timeout=60,
                    statement_cache_size=0,  # Disable statement cache for Neon compatibility
                    server_settings={
                        'search_path': 'public',
                    }
                )
                logger.info("PostgreSQL connection pool initialized successfully")

                # Test connection
                if self.is_sqlite:
                    cursor = await conn.execute("SELECT 1")
                    await cursor.fetchone()
                    logger.info("SQLite connection test successful")
                else:
                    await conn.fetchval("SELECT 1")
                    logger.info("PostgreSQL connection test successful")
        except Exception as e:
            logger.error(f"Failed to initialize database connection: {e}")
            raise

    @asynccontextmanager
    async def acquire_connection(self):
        """
        Context manager for acquiring a database connection
        """
        if DISABLE_DATABASE:
            # When database is disabled, yield None
            yield None
        elif self.is_sqlite:
            # For SQLite, create a new connection
            conn = await aiosqlite.connect(self.db_path)
            try:
                yield conn
            finally:
                await conn.close()
        elif not self.pool:
            raise RuntimeError("Database pool not initialized")
        else:
            # For PostgreSQL
            conn = await self.pool.acquire()
            try:
                yield conn
            finally:
                await self.pool.release(conn)

    async def create_session(self, user_id: str) -> str:
        """
        Create a new chat session

        Args:
            user_id: Unique identifier for the user

        Returns:
            session_id: Unique identifier for the created session

        """
        if DISABLE_DATABASE:
            # Generate a session ID without storing it in database
            session_id = f"sess_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{user_id[:8]}"
            logger.info(f"Database disabled. Generated session: {session_id} (not stored)")
            return session_id

        try:
            session_id = f"sess_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{user_id[:8]}"

            async with self.acquire_connection() as conn:
                if conn is None:  # This shouldn't happen if DISABLE_DATABASE is False
                    return f"sess_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{user_id[:8]}"

                if self.is_sqlite:
                    # SQLite version
                    query = """
                    INSERT INTO chat_sessions (session_id, user_id, created_at, updated_at)
                    VALUES (?, ?, ?, ?)
                    """
                    await conn.execute(
                        query,
                        session_id,
                        user_id,
                        datetime.utcnow(),
                        datetime.utcnow()
                    )
                    await conn.commit()
                else:
                    # PostgreSQL version
                    query = """
                    INSERT INTO chat_sessions (session_id, user_id, created_at, updated_at)
                    VALUES ($1, $2, $3, $4)
                    """
                    await conn.execute(
                        query,
                        session_id,
                        user_id,
                        datetime.utcnow(),
                        datetime.utcnow()
                    )

                logger.info(f"Created chat session: {session_id} for user: {user_id}")
                return session_id

        except Exception as e:
            logger.error(f"Error creating session for user {user_id}: {e}")
            raise

    async def save_message(self, session_id: str, role: str, content: str, user_id: Optional[str] = "anonymous") -> bool:
        """
        Save a message to the database

        Args:
            session_id: Session identifier
            role: 'user' or 'assistant'
            content: Message text content
            user_id: User identifier (defaults to 'anonymous')

        Returns:
            bool: Success status
        """
        if role not in ['user', 'assistant']:
            raise ValueError(f"Invalid role: {role}. Must be 'user' or 'assistant'")

        if DISABLE_DATABASE:
            # Skip saving to database if disabled, just log the action
            logger.info(f"Database disabled. Skipping save for {role} message in session: {session_id}")
            return True

        try:
            async with self.acquire_connection() as conn:
                if conn is None:
                    return True  # Skip saving if connection is None

                query = """
                INSERT INTO messages (session_id, role, content, user_id, timestamp, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """
                await conn.execute(
                    query,
                    session_id,
                    role,
                    content,
                    user_id,
                    datetime.utcnow(),
                    datetime.utcnow()
                )

                if self.is_sqlite:
                    await conn.commit()

                logger.info(f"Saved {role} message for session: {session_id} by user: {user_id}")
                return True

        except Exception as e:
            logger.error(f"Error saving message for session {session_id}: {e}")
            return False

    async def get_chat_history(self, session_id: str, limit: int = 50) -> List[Dict]:
        """
        Retrieve chat history for a session

        Args:
            session_id: Session identifier
            limit: Maximum number of messages to retrieve

        Returns:
            List of message dictionaries
        """
        if DISABLE_DATABASE:
            # Return empty history when database is disabled
            logger.info(f"Database disabled. Returning empty chat history for session: {session_id}")
            return []

        try:
            async with self.acquire_connection() as conn:
                if conn is None:
                    return []

                query = """
                SELECT session_id, role, content, timestamp, created_at
                FROM messages
                WHERE session_id = $1
                ORDER BY timestamp ASC
                LIMIT $2
                """
                rows = await conn.fetch(query, session_id, limit)

                messages = []
                for row in rows:
                    message = {
                        "session_id": row['session_id'],
                        "role": row['role'],
                        "content": row['content'],
                        "timestamp": row['timestamp'],
                        "created_at": row['created_at']
                    }
                    messages.append(message)

                logger.info(f"Retrieved {len(messages)} messages for session: {session_id}")
                return messages

        except Exception as e:
            logger.error(f"Error retrieving chat history for session {session_id}: {e}")
            return []

    async def save_selection(self, session_id: str, selected_text: str, question: str, answer: str) -> bool:
        """
        Save a user selection with context

        Args:
            session_id: Session identifier
            selected_text: Text the user selected/highlighted
            question: Question about the selected text
            answer: Answer provided by the system

        Returns:
            bool: Success status
        """
        if DISABLE_DATABASE:
            # Skip saving to database if disabled, just log the action
            logger.info(f"Database disabled. Skipping save for selection in session: {session_id}")
            return True

        try:
            async with self.acquire_connection() as conn:
                if conn is None:
                    return True  # Skip saving if connection is None

                query = """
                INSERT INTO user_selections (session_id, selected_text, question, answer, created_at)
                VALUES ($1, $2, $3, $4, $5)
                """
                await conn.execute(
                    query,
                    session_id,
                    selected_text,
                    question,
                    answer,
                    datetime.utcnow()
                )

                logger.info(f"Saved user selection for session: {session_id}")
                return True

        except Exception as e:
            logger.error(f"Error saving user selection for session {session_id}: {e}")
            return False

    async def get_user_selections(self, session_id: str) -> List[Dict]:
        """
        Retrieve user selections for a session

        Args:
            session_id: Session identifier

        Returns:
            List of selection dictionaries
        """
        if DISABLE_DATABASE:
            # Return empty selections when database is disabled
            logger.info(f"Database disabled. Returning empty selections for session: {session_id}")
            return []

        try:
            async with self.acquire_connection() as conn:
                if conn is None:
                    return []

                query = """
                SELECT selected_text, question, answer, created_at
                FROM user_selections
                WHERE session_id = $1
                ORDER BY created_at ASC
                """
                rows = await conn.fetch(query, session_id)

                selections = []
                for row in rows:
                    selection = {
                        "selected_text": row['selected_text'],
                        "question": row['question'],
                        "answer": row['answer'],
                        "created_at": row['created_at']
                    }
                    selections.append(selection)

                logger.info(f"Retrieved {len(selections)} selections for session: {session_id}")
                return selections

        except Exception as e:
            logger.error(f"Error retrieving user selections for session {session_id}: {e}")
            return []

    async def update_session(self, session_id: str):
        """
        Update the session's last activity timestamp

        Args:
            session_id: Session identifier
        """
        if DISABLE_DATABASE:
            # Skip updating if database is disabled
            logger.info(f"Database disabled. Skipping update for session: {session_id}")
            return

        try:
            async with self.acquire_connection() as conn:
                if conn is None:
                    return

                query = """
                UPDATE chat_sessions
                SET updated_at = $1
                WHERE session_id = $2
                """
                await conn.execute(query, datetime.utcnow(), session_id)

        except Exception as e:
            logger.error(f"Error updating session {session_id}: {e}")

    async def close(self):
        """
        Close the database connection pool
        """
        if DISABLE_DATABASE:
            # Skip closing if database is disabled
            logger.info("Database disabled. Skipping close operation.")
            return

        if self.pool:
            await self.pool.close()
            logger.info("Database connection pool closed")



















# Global database instance
db_manager: Optional['DatabaseManager'] = None


async def get_db():
    """
    Get the global database instance
    """
    global db_manager
    if DISABLE_DATABASE:
        logger.info("Database disabled. Returning None for get_db.")
        return None

    if not db_manager:
        db_manager = DatabaseManager()
        await db_manager.initialize()
    return db_manager


async def create_tables():
    """
    Create required database tables if they don't exist
    """
    if DISABLE_DATABASE:
        logger.info("⚠️ Database disabled. Skipping table creation.")
        return

    global db_manager
    if not db_manager:
        db_manager = DatabaseManager()
        await db_manager.initialize()

    try:
        async with db_manager.acquire_connection() as conn:
            if conn is None:
                return


            # Create chat_sessions table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS chat_sessions (
                    id INTEGER PRIMARY KEY,
                    session_id TEXT UNIQUE NOT NULL,
                    user_id TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # Create messages table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES chat_sessions(session_id) ON DELETE CASCADE
                );
            """)

            # Create user_selections table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS user_selections (
                    id INTEGER PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    selected_text TEXT NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES chat_sessions(session_id) ON DELETE CASCADE
                );
            """)

            # Create indexes for better performance
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_session_timestamp
                ON messages(session_id, timestamp);
            """)

            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_chat_sessions_user_created
                ON chat_sessions(user_id, created_at);
            """)

            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_user_selections_session_created
                ON user_selections(session_id, created_at);
            """)


            logger.info("Database tables created successfully")

    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


async def init_database():
    """
    Initialize database with tables and initial setup
    """
    if DISABLE_DATABASE:
        logger.info("⚠️ Database disabled. Skipping DB initialization.")
        return

    try:
        await create_tables()
        logger.info("Database initialization completed successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise