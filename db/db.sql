CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'en cours',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO tasks (title, description, status) VALUES 
('Mettre en place la base de données', 'Configurer PostgreSQL via Docker Compose', 'fait'),
('Mettre en place le Backend', 'Créer une API pour gérer les tâches', 'en cours'),
('Mettre en place le Frontend', 'Créer une interface utilisateur pour afficher et ajouter des tâches', 'en cours');
