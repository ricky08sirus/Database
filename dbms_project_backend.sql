-- Table: Flights
CREATE TABLE flights (
    Flight_ID INT NOT NULL AUTO_INCREMENT,
    Flight_Number VARCHAR(20) NOT NULL,
    Airline VARCHAR(50) NOT NULL,
    Status ENUM('Scheduled', 'In-Flight', 'Landed', 'Cancelled') NOT NULL DEFAULT 'Scheduled',
    Runway_ID INT DEFAULT NULL,
    Size ENUM('Small', 'Large') NOT NULL,
    Scheduled_Time INT NOT NULL,
    PRIMARY KEY (Flight_ID),
    KEY Runway_ID (Runway_ID),
    CONSTRAINT flights_ibfk_1 FOREIGN KEY (Runway_ID) REFERENCES runways (Runway_ID) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table: Maintenance
CREATE TABLE maintenance (
    Maintenance_ID INT NOT NULL AUTO_INCREMENT,
    Runway_ID INT NOT NULL,
    Description TEXT,
    PRIMARY KEY (Maintenance_ID),
    KEY Runway_ID (Runway_ID),
    CONSTRAINT maintenance_ibfk_1 FOREIGN KEY (Runway_ID) REFERENCES runways (Runway_ID) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table: Runways
CREATE TABLE runways (
    Runway_ID INT NOT NULL AUTO_INCREMENT,
    Runway_Name VARCHAR(50) NOT NULL,
    Runway_Status ENUM('Available', 'Occupied', 'Under Maintenance', 'Closed') NOT NULL DEFAULT 'Available',
    Length INT NOT NULL,
    Size ENUM('Small', 'Large') NOT NULL,
    Shutdown_Weather ENUM('None', 'Rainy', 'Snowy') NOT NULL DEFAULT 'None',
    PRIMARY KEY (Runway_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table: Runway Schedules
CREATE TABLE runway_schedules (
    Schedule_ID INT NOT NULL AUTO_INCREMENT,
    Runway_ID INT NOT NULL,
    Flight_ID INT NOT NULL,
    Scheduled_Time INT NOT NULL,
    Duration INT NOT NULL DEFAULT 5,
    PRIMARY KEY (Schedule_ID),
    KEY Runway_ID (Runway_ID),
    KEY Flight_ID (Flight_ID),
    CONSTRAINT runway_schedules_ibfk_1 FOREIGN KEY (Runway_ID) REFERENCES runways (Runway_ID) ON DELETE CASCADE,
    CONSTRAINT runway_schedules_ibfk_2 FOREIGN KEY (Flight_ID) REFERENCES flights (Flight_ID) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table: Weather
CREATE TABLE weather (
    Current_Weather ENUM('Optimal', 'Rainy', 'Snowy') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Procedure: ScheduleFlights
DELIMITER $$
CREATE PROCEDURE ScheduleFlights()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE flight_id INT;
    DECLARE flight_size ENUM('Small', 'Large');
    DECLARE flight_schedule_time INT;
    DECLARE runway_id INT;
    DECLARE runway_size ENUM('Small', 'Large');
    DECLARE runway_available BOOLEAN;

    DECLARE flight_cursor CURSOR FOR
        SELECT Flight_ID, Size, Scheduled_Time
        FROM flights
        WHERE Status = 'Scheduled' AND Runway_ID IS NULL
        ORDER BY Scheduled_Time;

    DECLARE runway_cursor CURSOR FOR
        SELECT Runway_ID, Size
        FROM runways
        WHERE Runway_Status = 'Available'
        ORDER BY Scheduled_Time;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN flight_cursor;

    read_loop: LOOP
        FETCH flight_cursor INTO flight_id, flight_size, flight_schedule_time;

        IF done THEN
            LEAVE read_loop;
        END IF;

        SET runway_available = FALSE;

        OPEN runway_cursor;

        runway_loop: LOOP
            FETCH runway_cursor INTO runway_id, runway_size;

            IF done THEN
                LEAVE runway_loop;
            END IF;

            IF NOT EXISTS (
                SELECT 1
                FROM runway_schedules rs
                WHERE rs.Runway_ID = runway_id
                AND (
                    (rs.Scheduled_Time < flight_schedule_time + 5)
                    OR
                    (rs.Scheduled_Time + rs.Duration > flight_schedule_time)
                )
            ) THEN
                INSERT INTO runway_schedules (Runway_ID, Flight_ID, Scheduled_Time, Duration)
                VALUES (runway_id, flight_id, flight_schedule_time, 5);

                UPDATE runways
                SET Runway_Status = 'Occupied'
                WHERE Runway_ID = runway_id;

                UPDATE flights
                SET Runway_ID = runway_id
                WHERE Flight_ID = flight_id;

                SET runway_available = TRUE;
                LEAVE runway_loop;
            END IF;
        END LOOP;

        CLOSE runway_cursor;

        IF NOT runway_available THEN
            ITERATE read_loop;
        END IF;
    END LOOP;

    CLOSE flight_cursor;
END$$
DELIMITER ;

-- Procedure: UpdateRunwayStatusForWeather
DELIMITER $$
CREATE PROCEDURE UpdateRunwayStatusForWeather(
    IN p_Weather_Condition ENUM('Rainy', 'Snowy', 'Optimal')
)
BEGIN
    IF p_Weather_Condition IN ('Rainy', 'Snowy') THEN
        UPDATE runways
        SET Runway_Status = 'Closed'
        WHERE Shutdown_Weather = p_Weather_Condition
        AND Runway_Status = 'Available';
    END IF;

    IF p_Weather_Condition = 'Optimal' THEN
        UPDATE runways
        SET Runway_Status = 'Available'
        WHERE Shutdown_Weather IN ('Rainy', 'Snowy')
        AND Runway_Status = 'Closed';
    END IF;
END$$
DELIMITER ;

-- Trigger: Maintenance_End
DELIMITER $$
CREATE TRIGGER Maintenance_End
AFTER DELETE ON maintenance
FOR EACH ROW
BEGIN
    UPDATE runways r
    JOIN weather w ON w.Current_Weather IS NOT NULL
    SET r.Runway_Status =
        CASE
            WHEN w.Current_Weather IN ('Rainy', 'Snowy') THEN 'Closed'
            WHEN w.Current_Weather = 'Optimal' THEN 'Available'
        END
    WHERE r.Runway_ID = OLD.Runway_ID;
END$$
DELIMITER ;

-- Function: ClosedRunways
DELIMITER $$
CREATE FUNCTION ClosedRunways() RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE closed_count INT;

    SELECT COUNT(*) INTO closed_count
    FROM runways
    WHERE Runway_Status = 'Closed'
    AND Shutdown_Weather IN ('Rainy', 'Snowy');
    
    RETURN closed_count;
END$$
DELIMITER ;
