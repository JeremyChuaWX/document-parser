DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'gender_enum') THEN
        CREATE TYPE gender_enum AS ENUM ('M', 'F', 'O');
    END IF;
END $$;

CREATE TABLE IF NOT EXISTS reports (
    id UUID DEFAULT gen_random_uuid(),
    report_id VARCHAR(255),
    lab_name VARCHAR(255),
    date_reported DATE,
    date_imported DATE,
    patient_age INT,
    gender gender_enum,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS tests (
    id UUID DEFAULT gen_random_uuid(),
    report_id UUID,
    name VARCHAR(255),
    category VARCHAR(255),
    subcategory VARCHAR(255),
    result VARCHAR(255),
    unit VARCHAR(255),
    loinc VARCHAR(255),
    PRIMARY KEY (id),
    FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
);
