CREATE TABLE pdf_reports (
    report_id VARCHAR(255) PRIMARY KEY,
    lab_name VARCHAR(255),
    date_reported DATE,
    date_imported DATE,
    patient_age INT,
    gender ENUM('M', 'F', 'O'),
    patient_id VARCHAR(255)
);

CREATE TABLE test_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    report_id VARCHAR(255),
    test_name VARCHAR(255),
    category VARCHAR(255),
    test_result VARCHAR(255),
    loinc_code VARCHAR(255),
    CONSTRAINT fk_report
        FOREIGN KEY (report_id)
        REFERENCES pdf_reports(report_id)
        ON DELETE CASCADE
);
