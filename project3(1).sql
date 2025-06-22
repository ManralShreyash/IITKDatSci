USE emp_record;

CREATE TABLE emp_record_table (
    EMP_ID VARCHAR(10) primary key, 
    FIRST_NAME VARCHAR(50),
    LAST_NAME VARCHAR(50),
    GENDER VARCHAR(10),
    ROLE VARCHAR(50),
    DEPT VARCHAR(50),
    EXP FLOAT,
    COUNTRY VARCHAR(50),
    CONTINENT VARCHAR(50),
    SALARY FLOAT,
    EMP_RATING FLOAT,
    MANAGER_ID INT,
    PROJ_ID INT,
    constraint fk_ert foreign key (MANAGER_ID) REFERENCES emp_record_table(EMP_ID)
);

CREATE TABLE proj_table (
    PROJECT_ID VARCHAR(10) primary key,
    PROJ_Name VARCHAR(100),
    DOMAIN VARCHAR(100),
    START_DATE DATE,
    CLOSURE_DATE DATE,
    DEV_QTR VARCHAR(10),
    STATUS VARCHAR(50)
);

alter table emp_record_table
add constraint fk_pt FOREIGN KEY (PROJ_ID) REFERENCES proj_table(PROJECT_ID);

CREATE TABLE data_science_team (
    EMP_ID VARCHAR(10) primary key,
    FIRST_NAME VARCHAR(50),
    LAST_NAME VARCHAR(50),
    GENDER VARCHAR(10),
    ROLE VARCHAR(50),
    DEPT VARCHAR(50),
    EXP FLOAT,
    COUNTRY VARCHAR(50),
    CONTINENT VARCHAR(50),
    constraint fk_ds foreign key (EMP_ID) references emp_record_table(EMP_ID)
);

LOAD DATA LOCAL INFILE 'C:\Users\Shreyash\OneDrive\Desktop\Shreyash\IITK DATA SCIENCE\project 3/emp_record_table.csv'
INTO TABLE emp_record_table
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA	 LOCAL INFILE 'C:\Users\Shreyash\OneDrive\Desktop\Shreyash\IITK DATA SCIENCE\project 3/proj_table.csv'
INTO TABLE proj_table
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:\Users\Shreyash\OneDrive\Desktop\Shreyash\IITK DATA SCIENCE\project 3/data_science_team.csv'
INTO TABLE data_science_team
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


/*Step 3: Basic Employee Listing*/
SELECT EMP_ID, FIRST_NAME, LAST_NAME, GENDER, DEPT
FROM emp_record_table;

-- Step 4: Filter by Ratings
-- Less than 2
SELECT EMP_ID, FIRST_NAME, LAST_NAME, GENDER, DEPT, EMP_RATING
FROM emp_record_table
WHERE EMP_RATING < 2;

-- Greater than 4
SELECT EMP_ID, FIRST_NAME, LAST_NAME, GENDER, DEPT, EMP_RATING
FROM emp_record_table
WHERE EMP_RATING > 4;

-- Between 2 and 4
SELECT EMP_ID, FIRST_NAME, LAST_NAME, GENDER, DEPT, EMP_RATING
FROM emp_record_table
WHERE EMP_RATING BETWEEN 2 AND 4;

-- Step 5: Concatenate Name for Finance Employees
SELECT CONCAT(FIRST_NAME, ' ', LAST_NAME) AS NAME
FROM emp_record_table
WHERE DEPT = 'Finance';

-- Step 6: Employees Who Have Reportees
SELECT MANAGER_ID, COUNT(*) AS Num_Reportees
FROM emp_record_table
WHERE MANAGER_ID IS NOT NULL
GROUP BY MANAGER_ID;

-- Step 7: Healthcare and Finance Employees
SELECT * FROM emp_record_table WHERE DEPT = 'Healthcare'
UNION
SELECT * FROM emp_record_table WHERE DEPT = 'Finance';

-- Step 8: Group By Department and Show Max Rating
SELECT EMP_ID, FIRST_NAME, LAST_NAME, ROLE, DEPT, EMP_RATING,
       MAX(EMP_RATING) OVER (PARTITION BY DEPT) AS Max_Rating
FROM emp_record_table;

-- Step 9: Min/Max Salary by Role
SELECT ROLE, MIN(SALARY) AS Min_Salary, MAX(SALARY) AS Max_Salary
FROM emp_record_table
GROUP BY ROLE;

-- Step 10: Rank Employees by Experience
SELECT EMP_ID, FIRST_NAME, LAST_NAME, EXP,
       RANK() OVER (ORDER BY EXP DESC) AS Exp_Rank
FROM emp_record_table;

-- Step 11: View for High Salary Employees
CREATE VIEW High_Salary_Employees AS
SELECT * FROM emp_record_table
WHERE SALARY > 6000;

-- Step 12: Nested Query for >10 Years Experience
SELECT * FROM emp_record_table
WHERE EXP > (SELECT AVG(EXP) FROM emp_record_table WHERE EXP > 10);

-- Step 13: Stored Procedure for >3 Years Experience
DELIMITER //

CREATE PROCEDURE GetExperiencedEmployees()
BEGIN
    SELECT * FROM emp_record_table WHERE EXP > 3;
END //

DELIMITER ;

-- Step 14: Stored Function to Check Standard Job Profile
DELIMITER //

CREATE FUNCTION check_job_standard(exp FLOAT)
RETURNS VARCHAR(50)
DETERMINISTIC
BEGIN
    DECLARE ROLE VARCHAR(50);
    IF exp <= 2 THEN
        SET ROLE = 'JUNIOR DATA SCIENTIST';
    ELSEIF exp <= 5 THEN
        SET ROLE = 'ASSOCIATE DATA SCIENTIST';
    ELSEIF exp <= 10 THEN
        SET ROLE = 'SENIOR DATA SCIENTIST';
    ELSEIF exp <= 12 THEN
        SET ROLE = 'LEAD DATA SCIENTIST';
    ELSEIF exp <= 16 THEN
        SET ROLE = 'MANAGER';
    ELSE
        SET ROLE = 'SENIOR MANAGER';
    END IF;
    RETURN ROLE;
END //

DELIMITER ;

-- Usage:
SELECT EMP_ID, ROLE, check_job_standard(EXP) AS STANDARD_ROLE
FROM data_science_team;

-- Step 15: Create Index for Performance on FIRST_NAME
-- Analyze performance before
EXPLAIN SELECT * FROM emp_record_table WHERE FIRST_NAME = 'Eric';

-- Create index
CREATE INDEX idx_firstname ON emp_record_table(FIRST_NAME);

-- Step 16: Calculate Bonus
SELECT EMP_ID, FIRST_NAME, SALARY, EMP_RATING,
       (SALARY * 0.05 * EMP_RATING) AS BONUS
FROM emp_record_table;

-- Step 17: Average Salary by Continent and Country
SELECT CONTINENT, COUNTRY, AVG(SALARY) AS Avg_Salary
FROM emp_record_table
GROUP BY CONTINENT, COUNTRY;













