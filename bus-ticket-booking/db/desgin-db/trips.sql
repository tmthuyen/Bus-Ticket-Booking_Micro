-- ===== Enums =====
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'trip_status') THEN
        CREATE TYPE trip_status AS ENUM ('SCHEDULED','BOARDING','DEPARTED','CANCELLED','COMPLETED');
    END IF;
END $$;

-- ===== routes =====
CREATE TABLE IF NOT EXISTS routes (
    id                 BIGSERIAL PRIMARY KEY,
    origin             VARCHAR(100) NOT NULL,
    destination        VARCHAR(100) NOT NULL,
    base_price         NUMERIC(10,2) NOT NULL,
    distance_km        NUMERIC(6,1),
    estimated_duration INTEGER,
    CONSTRAINT uq_routes_origin_destination UNIQUE (origin, destination)
);

CREATE INDEX IF NOT EXISTS idx_routes_origin ON routes(origin);
CREATE INDEX IF NOT EXISTS idx_routes_destination ON routes(destination);

-- ===== trips =====
CREATE TABLE IF NOT EXISTS trips (
    id               BIGSERIAL PRIMARY KEY,
    route_id         BIGINT NOT NULL REFERENCES routes(id) ON DELETE RESTRICT,
    departure_time   TIMESTAMPTZ NOT NULL,
    arrival_time     TIMESTAMPTZ,
    bus_plate        VARCHAR(15),
    status           trip_status NOT NULL DEFAULT 'SCHEDULED',
    total_seats      INTEGER NOT NULL,
    available_seats  INTEGER NOT NULL,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT ck_trips_available_nonneg CHECK (available_seats >= 0),
    CONSTRAINT ck_trips_total_gt0        CHECK (total_seats > 0),
    CONSTRAINT ck_trips_avail_le_total   CHECK (available_seats <= total_seats)
);

CREATE INDEX IF NOT EXISTS idx_trips_route_id       ON trips(route_id);
CREATE INDEX IF NOT EXISTS idx_trips_departure_time ON trips(departure_time);
CREATE INDEX IF NOT EXISTS idx_trips_bus_plate      ON trips(bus_plate);

-- cập nhật updated_at tự động ở Postgres (trigger)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_proc WHERE proname = 'set_timestamp') THEN
        CREATE OR REPLACE FUNCTION set_timestamp()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    END IF;
END $$;

DROP TRIGGER IF EXISTS trg_trips_set_timestamp ON trips;
CREATE TRIGGER trg_trips_set_timestamp
BEFORE UPDATE ON trips
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

-- ===== seats =====
CREATE TABLE IF NOT EXISTS seats (
    id           BIGSERIAL PRIMARY KEY,
    trip_id      BIGINT NOT NULL REFERENCES trips(id) ON DELETE CASCADE,
    seat_number  VARCHAR(10) NOT NULL,
    floor        INTEGER,
    is_booked    BOOLEAN NOT NULL DEFAULT FALSE,
    booked_at    TIMESTAMPTZ,

    CONSTRAINT uq_seats_trip_seat_number UNIQUE (trip_id, seat_number),
    CONSTRAINT ck_seats_floor_1_2 CHECK (floor IS NULL OR floor IN (1,2))
);

CREATE INDEX IF NOT EXISTS idx_seats_trip_id ON seats(trip_id);
