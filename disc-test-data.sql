-- Insert Manufacturers
INSERT INTO Manufacturer (name, country) VALUES
    ('Innova', 'USA'),
    ('Discraft', 'USA'),
    ('Dynamic Discs', 'USA'),
    ('Latitude 64', 'Sweden'),
    ('MVP Disc Sports', 'USA');

-- Insert Disc Types
INSERT INTO DiscType (typeName, description) VALUES
    ('Distance Driver', 'Maximum distance disc with sharp edge'),
    ('Fairway Driver', 'Controlled distance disc with moderate edge'),
    ('Midrange', 'All-purpose disc with rounded edge'),
    ('Putter', 'Slow speed disc for approaching and putting');

-- Insert Flight Ratings (Speed, Glide, Turn, Fade)
INSERT INTO FlightRating (speed, glide, turn, fade) VALUES
    (13, 5, -1, 3),  -- High-speed driver
    (7, 5, 0, 2),    -- Fairway driver
    (5, 5, -1, 1),   -- Midrange
    (2, 3, 0, 1),    -- Putter
    (11, 6, -2, 2),  -- Distance driver
    (4, 4, 0, 2);    -- Approach disc

-- Insert Owners
INSERT INTO Owner (firstName, lastName, phoneNumber) VALUES
    ('John', 'Smith', '555-0101'),
    ('Sarah', 'Johnson', '555-0102'),
    ('Mike', 'Williams', '555-0103'),
    ('Emily', 'Brown', '555-0104'),
    ('David', 'Jones', '555-0105');

-- Insert Discs
INSERT INTO Disc (ownerID, flightRatingID, discTypeID, manufacturerID, color, name, weight) VALUES
    (1, 1, 1, 1, 'Blue', 'Destroyer', 175.00),
    (1, 2, 2, 1, 'Red', 'Teebird', 170.00),
    (2, 3, 3, 2, 'Pink', 'Buzzz', 177.00),
    (3, 4, 4, 3, 'White', 'Judge', 174.00),
    (4, 5, 1, 4, 'Orange', 'Saint Pro', 169.00),
    (5, 6, 3, 5, 'Green', 'Reactor', 178.00),
    (2, 1, 1, 2, 'Purple', 'Force', 174.00),
    (3, 3, 3, 1, 'Yellow', 'Roc3', 180.00),
    (4, 4, 4, 2, 'Black', 'Luna', 173.00),
    (5, 2, 2, 3, 'Red', 'Escape', 172.00);