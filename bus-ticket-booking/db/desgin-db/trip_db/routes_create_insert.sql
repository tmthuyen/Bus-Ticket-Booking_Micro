-- select
SELECT * FROM btb_trip_db.routes;
-- create
CREATE TABLE `routes` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `origin` varchar(100) NOT NULL,
  `origin_code` varchar(100) DEFAULT NULL,
  `destination` varchar(100) NOT NULL,
  `destination_code` varchar(100) DEFAULT NULL,
  `base_price` decimal(10,2) NOT NULL,
  `distance_km` decimal(6,1) DEFAULT NULL,
  `estimated_duration` int DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT (now()),
  `updated_at` datetime NOT NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_routes_origin_destination` (`origin`,`destination`),
  UNIQUE KEY `uq_routes_origincode_destinationcode` (`origin_code`,`destination_code`),
  KEY `ix_routes_destination` (`destination`),
  KEY `ix_routes_destination_code` (`destination_code`),
  KEY `ix_routes_origin` (`origin`),
  KEY `ix_routes_origin_code` (`origin_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- insert data
INSERT INTO btb_trip_db.routes
(origin, origin_code, destination, destination_code, base_price, distance_km, estimated_duration)
VALUES
-- TP.HCM → Miền Trung/Bắc
('TP. Hồ Chí Minh','tp-ho-chi-minh','Đà Nẵng','da-nang',        850000, 960.0,  1150),
('TP. Hồ Chí Minh','tp-ho-chi-minh','Huế','hue',               920000, 1050.0, 1260),
('TP. Hồ Chí Minh','tp-ho-chi-minh','Quy Nhơn','quy-nhon',     650000, 650.0,   780),
('TP. Hồ Chí Minh','tp-ho-chi-minh','Nha Trang','nha-trang',   350000, 430.0,   520),
('TP. Hồ Chí Minh','tp-ho-chi-minh','Phan Rang','phan-rang',   280000, 340.0,   410),
('TP. Hồ Chí Minh','tp-ho-chi-minh','Phan Thiết','phan-thiet', 220000, 200.0,   250),
('TP. Hồ Chí Minh','tp-ho-chi-minh','Buôn Ma Thuột','buon-ma-thuot', 320000, 320.0,  390),
('TP. Hồ Chí Minh','tp-ho-chi-minh','Pleiku','pleiku',         600000, 630.0,   760),
('TP. Hồ Chí Minh','tp-ho-chi-minh','Đà Lạt','da-lat',         300000, 310.0,   380),
('TP. Hồ Chí Minh','tp-ho-chi-minh','Vinh','vinh',            1100000, 1350.0, 1620),
('TP. Hồ Chí Minh','tp-ho-chi-minh','Đồng Hới','dong-hoi',     980000, 1200.0, 1440),
('TP. Hồ Chí Minh','tp-ho-chi-minh','Hà Nội','ha-noi',        1200000, 1700.0, 2040),
('TP. Hồ Chí Minh','tp-ho-chi-minh','Hải Phòng','hai-phong',  1250000, 1750.0, 2100),
('TP. Hồ Chí Minh','tp-ho-chi-minh','Thanh Hóa','thanh-hoa',  1150000, 1500.0, 1800),
('TP. Hồ Chí Minh','tp-ho-chi-minh','Ninh Bình','ninh-binh',  1180000, 1600.0, 1920),

-- Cần Thơ → Miền Trung/Bắc
('Cần Thơ','can-tho','Đà Nẵng','da-nang',                      900000, 1100.0, 1320),
('Cần Thơ','can-tho','Nha Trang','nha-trang',                  450000, 600.0,   720),
('Cần Thơ','can-tho','Quy Nhơn','quy-nhon',                    700000, 820.0,   980),
('Cần Thơ','can-tho','Huế','hue',                              970000, 1190.0, 1420),
('Cần Thơ','can-tho','Hà Nội','ha-noi',                       1300000, 1870.0, 2240),

-- Vũng Tàu → Miền Trung
('Vũng Tàu','vung-tau','Nha Trang','nha-trang',                420000, 500.0,   600),
('Vũng Tàu','vung-tau','Đà Nẵng','da-nang',                    880000, 1020.0, 1220),

-- Biên Hòa (Đồng Nai) → Miền Trung
('Biên Hòa','bien-hoa','Nha Trang','nha-trang',                330000, 400.0,   480),
('Biên Hòa','bien-hoa','Đà Nẵng','da-nang',                    820000, 930.0,  1120),

-- Mỹ Tho (Tiền Giang) → Miền Trung
('Mỹ Tho','my-tho','Nha Trang','nha-trang',                    400000, 500.0,   600),
('Mỹ Tho','my-tho','Đà Nẵng','da-nang',                        850000, 1000.0, 1200),

-- Rạch Giá / Cà Mau → Miền Trung/Bắc (đường dài)
('Rạch Giá','rach-gia','Đà Nẵng','da-nang',                    990000, 1250.0, 1500),
('Cà Mau','ca-mau','Hà Nội','ha-noi',                         1400000, 2000.0, 2400);


-- alter table btb_trip_db.routes
-- modify column destination_code varchar(100)