schema = {
    'agency': """
    CREATE TABLE IF NOT EXISTS agency
    (
        agency_id                  TEXT NOT NULL,
            agency_name            TEXT NOT NULL,
            agency_url             TEXT NOT NULL,
            agency_timezone        TEXT NOT NULL,
            agency_lang            TEXT,
            agency_phone           TEXT,
            agency_fare_url        TEXT,
            agency_email           TEXT,
            PRIMARY KEY ( agency_id )
    )
    """,
    'calendar_dates': """
    CREATE TABLE IF NOT EXISTS calendar_dates
    (
        service_id					TEXT NOT NULL,
        date						INTEGER NOT NULL,
        exception_type				INTEGER NOT NULL,
        PRIMARY KEY ( service_id, date )
    )
    """,
    'calendar': """
    CREATE TABLE IF NOT EXISTS calendar
    (
        service_id					TEXT NOT NULL,
        monday						INTEGER NOT NULL,
        tuesday					INTEGER NOT NULL,
        wednesday					INTEGER NOT NULL,
        thursday					INTEGER NOT NULL,
        friday						INTEGER NOT NULL,
        saturday					INTEGER NOT NULL,
        sunday						INTEGER NOT NULL,
        start_date 				INTEGER NOT NULL,
        end_date 					INTEGER NOT NULL,
        PRIMARY KEY ( service_id )
    )       
    """,
    'feed_info': """
    CREATE TABLE IF NOT EXISTS feed_info
    (
        feed_publisher_name TEXT NOT NULL,
        feed_publisher_url  TEXT NOT NULL,
        feed_lang           TEXT NOT NULL,
        default_lang        TEXT,
        feed_start_date     INTEGER,
        feed_end_date       INTEGER,
        feed_version        TEXT,
        feed_contact_email  TEXT,
        feed_contact_url    TEXT
    )
    """,
    'routes': """
    CREATE TABLE IF NOT EXISTS routes
    (
        agency_id 				TEXT NOT NULL,
        route_id				TEXT,
        route_short_name		TEXT,
        route_long_name		TEXT,
        route_desc				TEXT,
        route_type				INTEGER NOT NULL,
        route_url				TEXT,
        route_color			TEXT,
        route_text_color		TEXT,
        route_sort_order		INTEGER,
        continuous_pickup		INTEGER,
        continuous_drop_off	INTEGER,
        network_id				TEXT,
        PRIMARY KEY ( route_id )
    ) 
    """,
    'shapes': """
    CREATE TABLE IF NOT EXISTS shapes
    (
        shape_id            TEXT NOT NULL,
        shape_pt_lat        FLOAT NOT NULL,
        shape_pt_lon        FLOAT NOT NULL,
        shape_pt_sequence   INTEGER NOT NULL,
        shape_dist_traveled FLOAT
    )
    """,
    'stop_times': """
    CREATE TABLE IF NOT EXISTS stop_times
    (
        trip_id						TEXT NOT NULL,
        arrival_time					TEXT,
        departure_time					TEXT,
        stop_id						TEXT,
        location_group_id				TEXT,
        location_id					TEXT,
        stop_sequence					INTEGER NOT NULL,
        stop_headsign					TEXT,
        start_pickup_drop_off_window 	TEXT,
        end_pickup_drop_off_window 	TEXT,
        pickup_type					TEXT,
        drop_off_type					TEXT,
        continuous_pickup				INTEGER,
        continuous_drop_off			INTEGER,
        shape_dist_traveled			FLOAT,
        timepoint						INTEGER,
        pickup_booking_rule_id			INTEGER,
        drop_off_booking_rule_id		INTEGER,
        PRIMARY KEY ( trip_id, stop_id, stop_sequence )
    )
    """,
    'stops': """
    CREATE TABLE IF NOT EXISTS stops
    (
        stop_id						TEXT NOT NULL,
        stop_code						TEXT,
        stop_name						TEXT,
        tts_stop_name					TEXT,
        stop_desc						TEXT,
        stop_lat						FLOAT,
        stop_lon						FLOAT,
        zone_id						TEXT,
        stop_url 						TEXT,
        location_type 					TEXT,
        parent_station					TEXT,
        stop_timezone					TEXT,
        wheelchair_boarding			TEXT,
        level_id						TEXT,
        platform_code					TEXT,
        PRIMARY KEY ( stop_id )
    )        
    """,
    'transfers': """
    CREATE TABLE IF NOT EXISTS transfers
    (
        from_stop_id				TEXT,
        to_stop_id					TEXT,
        from_route_id				TEXT,
        to_route_id				TEXT,
        from_trip_id				TEXT,
        to_trip_id					TEXT,
        transfer_type				TEXT NOT NULL,
        min_transfer_time			TEXT
    )
    """,
    'trips': """
    CREATE TABLE IF NOT EXISTS trips
    (
        route_id				TEXT NOT NULL,
        service_id				TEXT NOT NULL,
        trip_id				TEXT NOT NULL,
        trip_headsign			TEXT,
        trip_short_name		TEXT,
        direction_id			TEXT,
        block_id				TEXT,
        shape_id				TEXT,
        wheelchair_accessible	TEXT,
        bikes_allowed			TEXT,
        PRIMARY KEY ( trip_id )
    ) 
    """
}