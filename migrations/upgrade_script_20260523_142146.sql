BEGIN TRANSACTION;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

GO

-- Running upgrade  -> 77e99905ae73

CREATE TABLE [LeaveApplication] (
    id INTEGER NOT NULL IDENTITY, 
    [employeeId] INTEGER NOT NULL, 
    type VARCHAR(6) NOT NULL, 
    [startDate] DATETIME NOT NULL, 
    [endDate] DATETIME NOT NULL, 
    reason VARCHAR(500) NOT NULL, 
    status VARCHAR(8) NOT NULL DEFAULT 'Pending', 
    [createdAt] DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    [updatedAt] DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    PRIMARY KEY (id), 
    FOREIGN KEY([employeeId]) REFERENCES [Employee] (id)
);

GO

CREATE TABLE [Payslip] (
    id INTEGER NOT NULL IDENTITY, 
    [employeeId] INTEGER NOT NULL, 
    month INTEGER NOT NULL, 
    year INTEGER NOT NULL, 
    [basicSalary] NUMERIC(10, 2) NOT NULL, 
    allowances NUMERIC(10, 2) NULL, 
    deductions NUMERIC(10, 2) NULL, 
    [netSalary] NUMERIC(10, 2) NOT NULL, 
    [createdAt] DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    [updatedAt] DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    PRIMARY KEY (id), 
    FOREIGN KEY([employeeId]) REFERENCES [Employee] (id)
);

GO

ALTER TABLE [Attendance] ADD [createdAt] DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP;

GO

ALTER TABLE [Attendance] ADD [updatedAt] DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP;

GO

INSERT INTO alembic_version (version_num) OUTPUT inserted.version_num VALUES ('77e99905ae73');

GO

COMMIT;

GO

