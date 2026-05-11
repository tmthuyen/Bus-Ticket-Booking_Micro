SELECT * FROM btb_trip_db.trips;

-- CREATE
CREATE TABLE `trips` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `route_id` bigint NOT NULL,
  `departure_time` datetime NOT NULL,
  `arrival_time` datetime DEFAULT NULL,
  `bus_plate` varchar(15) DEFAULT NULL,
  `status` varchar(9) NOT NULL DEFAULT 'SCHEDULED',
  `total_seats` int NOT NULL,
  `available_seats` int NOT NULL,
  `created_at` datetime NOT NULL DEFAULT (now()),
  `updated_at` datetime NOT NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `ix_trips_route_id` (`route_id`),
  KEY `ix_trips_bus_plate` (`bus_plate`),
  KEY `ix_trips_departure_time` (`departure_time`),
  CONSTRAINT `trips_ibfk_1` FOREIGN KEY (`route_id`) REFERENCES `routes` (`id`) ON DELETE RESTRICT,
  CONSTRAINT `ck_trips_avail_le_total` CHECK ((`available_seats` <= `total_seats`)),
  CONSTRAINT `ck_trips_available_nonneg` CHECK ((`available_seats` >= 0)),
  CONSTRAINT `ck_trips_total_gt0` CHECK ((`total_seats` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

/* === TP.HCM -> Đà Nẵng ===
   Slot VN: 06:00 & 20:00  (UTC: 23:00(-1d) & 13:00)
*/
USE btb_trip_db;
INSERT INTO trips (route_id, departure_time, arrival_time, bus_plate, status, total_seats, available_seats)
SELECT r.id,
       '2025-11-19 23:00:00',                                 -- 06:00 VN 20/11
       DATE_ADD('2025-11-19 23:00:00', INTERVAL r.estimated_duration MINUTE),
       '51B-123.45', 'SCHEDULED', 40, 40
FROM routes r
WHERE r.origin_code='tp-ho-chi-minh' AND r.destination_code='da-nang';

INSERT INTO trips (route_id, departure_time, arrival_time, bus_plate, status, total_seats, available_seats)
SELECT r.id,
       '2025-11-20 13:00:00',                                 -- 20:00 VN 20/11
       DATE_ADD('2025-11-20 13:00:00', INTERVAL r.estimated_duration MINUTE),
       '51B-678.90', 'SCHEDULED', 40, 40
FROM routes r
WHERE r.origin_code='tp-ho-chi-minh' AND r.destination_code='da-nang';


/* === TP.HCM -> Huế === */
INSERT INTO btb_trip_db.trips (route_id, departure_time, arrival_time, bus_plate, status, total_seats, available_seats)
SELECT r.id, '2025-11-19 23:30:00',
       DATE_ADD('2025-11-19 23:30:00', INTERVAL r.estimated_duration MINUTE),
       '51B-234.56', 'SCHEDULED', 40, 40
FROM routes r
WHERE r.origin_code='tp-ho-chi-minh' AND r.destination_code='hue';

INSERT INTO trips (route_id, departure_time, arrival_time, bus_plate, status, total_seats, available_seats)
SELECT r.id, '2025-11-20 13:30:00',
       DATE_ADD('2025-11-20 13:30:00', INTERVAL r.estimated_duration MINUTE),
       '51B-987.65', 'SCHEDULED', 40, 40
FROM routes r
WHERE r.origin_code='tp-ho-chi-minh' AND r.destination_code='hue';


/* === TP.HCM -> Quy Nhơn === */
INSERT INTO btb_trip_db.trips (route_id, departure_time, arrival_time, bus_plate, status, total_seats, available_seats)
SELECT r.id, '2025-11-19 23:00:00',
       DATE_ADD('2025-11-19 23:00:00', INTERVAL r.estimated_duration MINUTE),
       '51B-345.67', 'SCHEDULED', 40, 40
FROM routes r
WHERE r.origin_code='tp-ho-chi-minh' AND r.destination_code='quy-nhon';

INSERT INTO trips (route_id, departure_time, arrival_time, bus_plate, status, total_seats, available_seats)
SELECT r.id, '2025-11-20 13:00:00',
       DATE_ADD('2025-11-20 13:00:00', INTERVAL r.estimated_duration MINUTE),
       '51B-876.54', 'SCHEDULED', 40, 40
FROM routes r
WHERE r.origin_code='tp-ho-chi-minh' AND r.destination_code='quy-nhon';


/* === TP.HCM -> Hà Nội (đường dài) === */
INSERT INTO trips (route_id, departure_time, arrival_time, bus_plate, status, total_seats, available_seats)
SELECT r.id, '2025-11-19 22:00:00',
       DATE_ADD('2025-11-19 22:00:00', INTERVAL r.estimated_duration MINUTE),
       '51B-456.78', 'SCHEDULED', 40, 40
FROM routes r
WHERE r.origin_code='tp-ho-chi-minh' AND r.destination_code='ha-noi';

INSERT INTO trips (route_id, departure_time, arrival_time, bus_plate, status, total_seats, available_seats)
SELECT r.id, '2025-11-20 12:00:00',
       DATE_ADD('2025-11-20 12:00:00', INTERVAL r.estimated_duration MINUTE),
       '51B-765.43', 'SCHEDULED', 40, 40
FROM routes r
WHERE r.origin_code='tp-ho-chi-minh' AND r.destination_code='ha-noi';


/* === Cần Thơ -> Đà Nẵng === */
INSERT INTO btb_trip_db.trips (route_id, departure_time, arrival_time, bus_plate, status, total_seats, available_seats)
SELECT r.id, '2025-11-19 23:00:00',
       DATE_ADD('2025-11-19 23:00:00', INTERVAL r.estimated_duration MINUTE),
       '65B-111.22', 'SCHEDULED', 40, 40
FROM routes r
WHERE r.origin_code='can-tho' AND r.destination_code='da-nang';

INSERT INTO trips (route_id, departure_time, arrival_time, bus_plate, status, total_seats, available_seats)
SELECT r.id, '2025-11-20 13:00:00',
       DATE_ADD('2025-11-20 13:00:00', INTERVAL r.estimated_duration MINUTE),
       '65B-333.44', 'SCHEDULED', 40, 40
FROM routes r
WHERE r.origin_code='can-tho' AND r.destination_code='da-nang';


/* === Vũng Tàu -> Nha Trang === */
INSERT INTO trips (route_id, departure_time, arrival_time, bus_plate, status, total_seats, available_seats)
SELECT r.id, '2025-11-19 23:30:00',
       DATE_ADD('2025-11-19 23:30:00', INTERVAL r.estimated_duration MINUTE),
       '72B-555.66', 'SCHEDULED', 40, 40
FROM routes r
WHERE r.origin_code='vung-tau' AND r.destination_code='nha-trang';

INSERT INTO trips (route_id, departure_time, arrival_time, bus_plate, status, total_seats, available_seats)
SELECT r.id, '2025-11-20 13:30:00',
       DATE_ADD('2025-11-20 13:30:00', INTERVAL r.estimated_duration MINUTE),
       '72B-777.88', 'SCHEDULED', 40, 40
FROM routes r
WHERE r.origin_code='vung-tau' AND r.destination_code='nha-trang';
