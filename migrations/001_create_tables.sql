
-- migrations/001_create_tables.sql
CREATE TABLE IF NOT EXISTS users (
  user_id SERIAL PRIMARY KEY,
  role VARCHAR(20) NOT NULL,
  name TEXT,
  email TEXT,
  phone TEXT,
  timezone TEXT,
  profile JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS doctor_availability (
  availability_id SERIAL PRIMARY KEY,
  doctor_id INTEGER REFERENCES users(user_id),
  date DATE,
  start_time TIME,
  end_time TIME,
  status VARCHAR(20) DEFAULT 'available',
  meta JSONB
);
CREATE TABLE IF NOT EXISTS appointments (
  booking_id SERIAL PRIMARY KEY,
  doctor_id INTEGER REFERENCES users(user_id),
  patient_id INTEGER REFERENCES users(user_id),
  start_dt TIMESTAMP WITH TIME ZONE,
  end_dt TIMESTAMP WITH TIME ZONE,
  status VARCHAR(20) DEFAULT 'booked',
  source VARCHAR(50),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS reminder_settings (
  reminder_setting_id SERIAL PRIMARY KEY,
  doctor_id INTEGER REFERENCES users(user_id),
  patient_id INTEGER REFERENCES users(user_id),
  reminder_days INTEGER DEFAULT 7,
  reminder_channel VARCHAR(20) DEFAULT 'email',
  enabled BOOLEAN DEFAULT TRUE,
  last_sent_at TIMESTAMP WITH TIME ZONE
);
CREATE TABLE IF NOT EXISTS slot_feedback (
  feedback_id SERIAL PRIMARY KEY,
  client_id INTEGER REFERENCES users(user_id),
  doctor_id INTEGER REFERENCES users(user_id),
  selected_slot TIMESTAMP WITH TIME ZONE,
  recommended_slots JSONB,
  accepted BOOLEAN,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
