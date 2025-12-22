-- Database Migration: Fix user_profiles foreign key constraint
-- This migration updates the user_profiles table to reference the users table instead of chat_sessions

-- First, drop the existing foreign key constraint
ALTER TABLE user_profiles DROP CONSTRAINT IF EXISTS user_profiles_user_id_fkey;

-- Add the correct foreign key constraint to reference the users table
ALTER TABLE user_profiles
ADD CONSTRAINT user_profiles_user_id_fkey
FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE;

-- Update the index to match the new foreign key
DROP INDEX IF EXISTS idx_user_profiles_user_id;
CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);