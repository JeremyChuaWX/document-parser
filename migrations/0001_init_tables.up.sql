CREATE TABLE IF NOT EXISTS reports (
    id BINARY(16) DEFAULT (UUID_TO_BIN(UUID())),
    report_id VARCHAR(255),
    lab_name VARCHAR(255),
    date_reported DATE,
    date_imported DATE,
    patient_age INT,
    gender ENUM('M', 'F', 'O'),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS tests (
    id BINARY(16) DEFAULT (UUID_TO_BIN(UUID())),
    report_id BINARY(16),
    name VARCHAR(255),
    category VARCHAR(255),
    subcategory VARCHAR(255),
    result VARCHAR(255),
    unit VARCHAR(255),
    loinc VARCHAR(255),
    PRIMARY KEY (id),
    FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
);
