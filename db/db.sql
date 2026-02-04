CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO tasks (title, description, status) VALUES 
('Setup Database', 'Configure PostgreSQL via Docker Compose', 'pending'),
('Develop Backend', 'Create API to manage tasks', 'pending'),
('Develop Frontend', 'Create UI to view and add tasks', 'pending');
