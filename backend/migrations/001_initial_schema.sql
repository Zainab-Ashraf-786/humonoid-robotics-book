-- Database Migration: Physical AI & Humanoid Robotics - RAG Chatbot Tables
-- This migration creates the necessary tables for the chatbot application
-- Target Platform: Neon Serverless Postgres

-- Create chat_sessions table
-- Stores information about chat sessions including user_id and timestamps
CREATE TABLE IF NOT EXISTS chat_sessions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create messages table
-- Stores the chat messages associated with each session
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (session_id) REFERENCES chat_sessions(session_id) ON DELETE CASCADE
);

-- Create user_selections table
-- Stores user selections and related Q&A from the chatbot interaction
CREATE TABLE IF NOT EXISTS user_selections (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    selected_text TEXT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (session_id) REFERENCES chat_sessions(session_id) ON DELETE CASCADE
);

-- Create indexes for performance optimization
-- Index on messages for fast retrieval by session and chronological order
CREATE INDEX IF NOT EXISTS idx_messages_session_timestamp
ON messages(session_id, timestamp);

-- Index on chat sessions for fast user-based retrieval
CREATE INDEX IF NOT EXISTS idx_chat_sessions_user_created
ON chat_sessions(user_id, created_at);

-- Index on user selections for fast retrieval by session
CREATE INDEX IF NOT EXISTS idx_user_selections_session_created
ON user_selections(session_id, created_at);

-- Additional indexes for efficient filtering
-- Index on messages role for fast filtering by message type
CREATE INDEX IF NOT EXISTS idx_messages_role 
ON messages(role);

-- Index on chat_sessions updated_at for fast sorting of recent sessions
CREATE INDEX IF NOT EXISTS idx_chat_sessions_updated 
ON chat_sessions(updated_at);

-- Create a function to automatically update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create a trigger to automatically update updated_at on chat_sessions
DROP TRIGGER IF EXISTS update_chat_sessions_updated_at ON chat_sessions;
CREATE TRIGGER update_chat_sessions_updated_at 
    BEFORE UPDATE ON chat_sessions 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Insert a sample session record for testing (optional)
-- INSERT INTO chat_sessions (session_id, user_id) 
-- VALUES ('sess_test_001', 'user_test') 
-- ON CONFLICT (session_id) DO NOTHING;

-- Insert sample messages for testing (optional)
-- INSERT INTO messages (session_id, role, content) 
-- VALUES 
--     ('sess_test_001', 'user', 'Hello, can you help me understand ROS 2 nodes?'),
--     ('sess_test_001', 'assistant', 'ROS 2 nodes are the fundamental building blocks of ROS 2 applications...')
-- ON CONFLICT DO NOTHING;

-- Insert sample user selection for testing (optional)  
-- INSERT INTO user_selections (session_id, selected_text, question, answer)
-- VALUES 
--     ('sess_test_001', 'ROS 2 nodes are the basic computational units', 'What are nodes?', 'Nodes are executables that use ROS client libraries to communicate with other nodes.')
-- ON CONFLICT DO NOTHING;

-- Grant permissions (if needed)
-- GRANT USAGE ON SCHEMA public TO app_user;
-- GRANT ALL PRIVILEGES ON TABLE chat_sessions TO app_user;
-- GRANT ALL PRIVILEGES ON TABLE messages TO app_user;
-- GRANT ALL PRIVILEGES ON TABLE user_selections TO app_user;

-- Grant sequence permissions for auto-incrementing keys
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_user;
-- GRANT USAGE, SELECT ON SEQUENCE chat_sessions_id_seq TO app_user;
-- GRANT USAGE, SELECT ON SEQUENCE messages_id_seq TO app_user;
-- GRANT USAGE, SELECT ON SEQUENCE user_selections_id_seq TO app_user;