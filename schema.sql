CREATE TABLE IF NOT EXISTS sources (
    id SERIAL PRIMARY KEY,
    source_name VARCHAR(255) NOT NULL,
    country VARCHAR(10) NOT NULL,
    source_type VARCHAR(100),
    api_available BOOLEAN DEFAULT FALSE,
    feed_available BOOLEAN DEFAULT FALSE,
    partner_required BOOLEAN DEFAULT FALSE,
    robots_status VARCHAR(50),
    tos_status VARCHAR(50),
    legal_basis VARCHAR(255),
    allowed_use TEXT,
    attribution_required BOOLEAN DEFAULT FALSE,
    refresh_interval VARCHAR(50),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS properties (
    id SERIAL PRIMARY KEY,
    listing_id VARCHAR(255),
    source_name VARCHAR(255),
    source_url TEXT,
    title TEXT,
    description TEXT,
    price NUMERIC(18,2),
    currency VARCHAR(10) DEFAULT 'MXN',
    property_type VARCHAR(100),
    bedrooms INTEGER,
    bathrooms INTEGER,
    parking_spaces INTEGER,
    square_meters NUMERIC(12,2),
    lot_meters NUMERIC(12,2),
    state VARCHAR(255),
    municipality VARCHAR(255),
    colonia VARCHAR(255),
    address TEXT,
    latitude NUMERIC(10,6),
    longitude NUMERIC(10,6),
    listing_status VARCHAR(50),
    broker_name VARCHAR(255),
    broker_phone VARCHAR(100),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    last_seen_at TIMESTAMP,
    legal_status VARCHAR(50),
    UNIQUE (source_name, listing_id)
);

CREATE TABLE IF NOT EXISTS compliance_audit (
    id SERIAL PRIMARY KEY,
    source_name VARCHAR(255),
    legal_basis VARCHAR(255),
    robots_ok BOOLEAN,
    tos_ok BOOLEAN,
    api_ok BOOLEAN,
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS source_registry (
    source_key VARCHAR(255) PRIMARY KEY,
    source_name VARCHAR(255) NOT NULL,
    source_type VARCHAR(100),
    platform VARCHAR(100),
    country VARCHAR(10),
    state VARCHAR(255),
    municipality VARCHAR(255),
    language VARCHAR(20),
    url TEXT,
    discovery_method VARCHAR(100),
    access_method VARCHAR(255),
    robots_policy TEXT,
    crawl_policy TEXT,
    crawl_frequency VARCHAR(50),
    enabled BOOLEAN DEFAULT FALSE,
    content_types JSONB,
    geographic_scope JSONB,
    extraction_strategy VARCHAR(255),
    parser_adapter VARCHAR(255),
    deduplication_strategy VARCHAR(255),
    last_crawled_at TIMESTAMP,
    last_success_at TIMESTAMP,
    last_error TEXT,
    attribution_metadata TEXT,
    legal_basis VARCHAR(255),
    allowed_use TEXT,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS community_content (
    id SERIAL PRIMARY KEY,
    content_id VARCHAR(255) NOT NULL,
    source_key VARCHAR(255) REFERENCES source_registry(source_key) ON DELETE SET NULL,
    source_name VARCHAR(255),
    source_type VARCHAR(100),
    platform VARCHAR(100),
    content_type VARCHAR(100),
    title TEXT,
    content TEXT,
    author_display_name VARCHAR(255),
    published_at TIMESTAMP,
    source_url TEXT,
    parent_url TEXT,
    discussion_id VARCHAR(255),
    comment_id VARCHAR(255),
    engagement_metrics JSONB,
    state VARCHAR(255),
    municipality VARCHAR(255),
    neighborhood VARCHAR(255),
    property_type VARCHAR(100),
    asking_price NUMERIC(18,2),
    rent_price NUMERIC(18,2),
    bedrooms INTEGER,
    bathrooms INTEGER,
    square_meters NUMERIC(12,2),
    transaction_context TEXT,
    housing_program_references JSONB,
    financing_references JSONB,
    relevant_entities JSONB,
    extracted_keywords JSONB,
    language VARCHAR(20),
    sentiment VARCHAR(50),
    crawl_timestamp TIMESTAMP,
    legal_status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (source_name, content_id)
);

CREATE TABLE IF NOT EXISTS property_followups (
    id SERIAL PRIMARY KEY,
    property_id INTEGER NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
    note TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'open',
    next_follow_up DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS alliance_contacts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(100) NOT NULL,
    company VARCHAR(255),
    phone VARCHAR(100),
    email VARCHAR(255),
    state VARCHAR(255),
    municipality VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS kpi_entries (
    id SERIAL PRIMARY KEY,
    metric_date DATE NOT NULL UNIQUE,
    properties_added INTEGER NOT NULL DEFAULT 0 CHECK (properties_added >= 0),
    appointments INTEGER NOT NULL DEFAULT 0 CHECK (appointments >= 0),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS monitoring_alerts (
    id SERIAL PRIMARY KEY,
    keyword VARCHAR(255) NOT NULL,
    property_id INTEGER REFERENCES properties(id) ON DELETE SET NULL,
    source_name VARCHAR(255),
    status VARCHAR(50) DEFAULT 'new',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS export_history (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    report_type VARCHAR(50) NOT NULL,
    format VARCHAR(20) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    filters JSONB,
    status VARCHAR(30) DEFAULT 'completed'
);
