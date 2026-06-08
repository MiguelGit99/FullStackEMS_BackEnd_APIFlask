BEGIN TRANSACTION;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

GO

-- Running upgrade  -> 35b1b8827cb9

CREATE TABLE [User] (
    id INTEGER NOT NULL IDENTITY, 
    email VARCHAR(255) NOT NULL, 
    password VARCHAR(255) NOT NULL, 
    role VARCHAR(8) NOT NULL, 
    [createdAt] DATETIME NOT NULL, 
    [updatedAt] DATETIME NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE (email)
);

GO

CREATE TABLE brands (
    brand_id INTEGER NOT NULL IDENTITY, 
    brand_name VARCHAR(255) NOT NULL, 
    PRIMARY KEY (brand_id)
);

GO

CREATE TABLE products (
    product_id INTEGER NOT NULL IDENTITY, 
    product_name VARCHAR(255) NOT NULL, 
    brand_id INTEGER NOT NULL, 
    category_id INTEGER NOT NULL, 
    model_year SMALLINT NOT NULL, 
    list_price DECIMAL(10, 2) NOT NULL, 
    PRIMARY KEY (product_id)
);

GO

CREATE TABLE [Employee] (
    id INTEGER NOT NULL IDENTITY, 
    [userId] INTEGER NOT NULL, 
    [firstName] VARCHAR(100) NOT NULL, 
    [lastName] VARCHAR(100) NOT NULL, 
    email VARCHAR(255) NOT NULL, 
    phone VARCHAR(50) NOT NULL, 
    position VARCHAR(100) NOT NULL, 
    [basicSalary] NUMERIC(10, 2) NOT NULL, 
    allowances NUMERIC(10, 2) NOT NULL, 
    deductions NUMERIC(10, 2) NOT NULL, 
    [employmentStatus] VARCHAR(8) NOT NULL, 
    [joinDate] DATETIME NOT NULL, 
    [isDeleted] BIT NOT NULL, 
    bio TEXT NOT NULL, 
    department VARCHAR(18) NOT NULL, 
    [createdAt] DATETIME NOT NULL, 
    [updatedAt] DATETIME NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY([userId]) REFERENCES [User] (id), 
    UNIQUE ([userId])
);

GO

INSERT INTO alembic_version (version_num) OUTPUT inserted.version_num VALUES ('35b1b8827cb9');

GO

-- Running upgrade 35b1b8827cb9 -> 2b6d204ccf88

CREATE TABLE [Attendance] (
    [employeeId] INTEGER NOT NULL IDENTITY, 
    date DATETIME NOT NULL, 
    [checkIn] DATETIME NULL, 
    [checkOut] DATETIME NULL, 
    status VARCHAR(7) NULL, 
    [workingHours] INTEGER NOT NULL, 
    [dayType] VARCHAR(17) NULL, 
    PRIMARY KEY ([employeeId])
);

GO

UPDATE alembic_version SET version_num='2b6d204ccf88' WHERE alembic_version.version_num = '35b1b8827cb9';

GO

COMMIT;

GO

