
-- User table for authentication and profile
CREATE TABLE "user" (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    emailid VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    firstname VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(50) NOT NULL,
    industry VARCHAR(100) NOT NULL,
    profession VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

-- PHQ-9 assessment submissions table
CREATE TABLE phq9_assessment (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES "user"(user_id) ON DELETE CASCADE,
    responses JSONB,
    total_score INT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE phq9_assessment
ADD COLUMN doctors_notes TEXT,
ADD COLUMN patients_notes TEXT;