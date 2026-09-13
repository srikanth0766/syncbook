-- Hotel PMS Database Schema

CREATE TABLE IF NOT EXISTS hotels (
    hotel_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS room_types (
    room_type_id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(hotel_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    total_rooms INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bookings (
    booking_id VARCHAR(255) PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(hotel_id) ON DELETE CASCADE,
    room_type_id INTEGER NOT NULL REFERENCES room_types(room_type_id) ON DELETE CASCADE,
    customer_name VARCHAR(255) NOT NULL,
    customer_email VARCHAR(255) NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'CONFIRMED',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Seed Data: Hotel A with Standard Room (10), Deluxe Room (5), Suite (2)
INSERT INTO hotels (hotel_id, name, location) 
VALUES (1, 'Hotel A', 'New York')
ON CONFLICT (hotel_id) DO NOTHING;

INSERT INTO room_types (room_type_id, hotel_id, name, total_rooms)
VALUES 
    (1, 1, 'Standard Room', 10),
    (2, 1, 'Deluxe Room', 5),
    (3, 1, 'Suite', 2)
ON CONFLICT (room_type_id) DO NOTHING;

SELECT setval('hotels_hotel_id_seq', (SELECT MAX(hotel_id) FROM hotels));
SELECT setval('room_types_room_type_id_seq', (SELECT MAX(room_type_id) FROM room_types));
