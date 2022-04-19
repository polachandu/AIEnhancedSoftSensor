DROP DATABASE IF EXISTS PE;
CREATE DATABASE PE;
USE PE;


DROP TABLE IF EXISTS PE;
CREATE TABLE PE(
  ID            INT NOT NULL AUTO_INCREMENT,
  S_T_C 		decimal(7,3) DEFAULT NULL,
  S_Pin_kPa 	decimal(7,3)  DEFAULT NULL,
  S_F_kgh 		decimal(7,3)  DEFAULT NULL,
  S_E_kW 		decimal(7,3)  DEFAULT NULL,
  S_Pout_kPa 	decimal(7,3)  DEFAULT NULL,
  CUR_DATE      DATE  DEFAULT NULL,
  CUR_TIME      TIME DEFAULT NULL,
  PRIMARY KEY(ID)
);
DROP PROCEDURE IF EXISTS InsertPE;
DELIMITER $$

CREATE PROCEDURE InsertPE(D1 decimal(7,3), D2 decimal(7,3), D3 decimal(7,3), D4 decimal(7,3), D6 DATE, D7 TIME)
BEGIN
    INSERT INTO PE(
        S_T_C,
		S_Pin_kPa,
        S_F_kgh, 
        S_E_kW,
        CUR_DATE,
        CUR_TIME 
    )
    VALUES(
        D1,
        D2,
        D3,
        D4,
        D6,
        D7
    );
END$$

DELIMITER ;

DROP PROCEDURE IF EXISTS LoadPE;
DELIMITER $$

CREATE PROCEDURE LoadPE(
     C1 decimal(7,3),
	 C2 decimal(7,3),
     C3 decimal(7,3),
     C4 decimal(7,3),
     C6 DATE,
     C7 TIME
)
BEGIN
    
    DECLARE counter INT DEFAULT 1;
    DECLARE D1 decimal(7,3) DEFAULT C1;
    DECLARE D2 decimal(7,3) DEFAULT C2;
    DECLARE D3 decimal(7,3) DEFAULT C3;
    DECLARE D4 decimal(7,3) DEFAULT C4;
	DECLARE D6 DATE DEFAULT C6;
	DECLARE D7 TIME DEFAULT C7;

    WHILE counter <= 11 DO
        CALL InsertPE(D1,D2,D3,D4,D6,D7);
        SET D1 = rand() ;
        SET D2 = rand() ;
        SET D3 = rand() ;
        SET D4 = rand() ;
        SET D6 = curdate() ;
        SET D7 = curtime() ;
        SET counter = counter + 1;
        
    END WHILE;

END$$

DELIMITER ;

-- CALL LoadPE(0.2,0.3,0.4,0.5,0.6,curdate() ,curtime());

-- SELECT * FROM PE;