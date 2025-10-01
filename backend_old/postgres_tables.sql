
-- DSM-5 assessment results table
CREATE TABLE dsm_5_assessment (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES "user"(user_id) ON DELETE CASCADE,
    severity VARCHAR(50) NOT NULL,
    q9_flag BOOLEAN NOT NULL,
    mdd_assessment VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
-- Drop tables if they exist
DROP TABLE IF EXISTS phq9_assessment;
DROP TABLE IF EXISTS "user";

-- User table for authentication and profile
CREATE TABLE "user" (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    emailid VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    firstname VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    age VARCHAR(10) NOT NULL,
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
    submitted_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
