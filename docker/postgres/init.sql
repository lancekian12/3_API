CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,  -- Change to lowercase
    last_name VARCHAR(100) NOT NULL,    -- Change to lowercase
    email VARCHAR(80) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE funds (
    id SERIAL PRIMARY KEY,
    amount DECIMAL(10, 2) NOT NULL,
    userId INTEGER REFERENCES users(id),  -- Use lowercase "users"
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);