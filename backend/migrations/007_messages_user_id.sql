-- Database Migration: Add user_id column to messages table for user-specific message tracking
-- This migration adds a user_id column to the messages table to track which user sent each message

-- Add user_id column to messages table
ALTER TABLE messages ADD COLUMN user_id TEXT;

-- Add foreign key constraint to link user_id to users table
-- Note: This is a soft constraint since we're adding it to an existing table
-- The user_id will be populated for new messages and can be NULL for existing messages

-- Update existing messages to have a default user_id if needed (optional)
-- UPDATE messages SET user_id = 'anonymous' WHERE user_id IS NULL;

-- Create an index on the new user_id column for better performance
CREATE INDEX IF NOT EXISTS idx_messages_user_id ON messages(user_id);

-- Update the foreign key constraint if needed to include user_id
-- Note: The foreign key relationship will be enforced in the application layer