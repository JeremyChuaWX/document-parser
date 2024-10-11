CREATE TABLE IF NOT EXISTS reports (
    id BINARY(16) DEFAULT (UUID_TO_BIN(UUID())),
    report_id VARCHAR(255),
    lab_name VARCHAR(255),
    date_reported DATE,
    date_imported DATE,
    patient_age INT,
    gender ENUM('M', 'F', 'O'),
    patient_id VARCHAR(255),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS tests (
    report_id BINARY(16),
    id INT AUTO_INCREMENT,
    test_name VARCHAR(255),
    category VARCHAR(255),
    test_result VARCHAR(255),
    loinc_code VARCHAR(255),
    PRIMARY KEY (report_id, id),
    FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
);
