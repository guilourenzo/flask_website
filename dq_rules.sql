CREATE TABLE `BucketList`.`tbl_dq_rules` (
  `id_rules` BIGINT NOT NULL AUTO_INCREMENT,
  `rules_name` VARCHAR(30) NOT NULL,
  `rules_description` VARCHAR(50) NULL,
  `rules_environment` VARCHAR(20) NULL,
  `rules_command` VARCHAR(200) NULL,
  `rules_created` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `rules_updated` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `rules_active` BIT DEFAULT TRUE NOT NULL,
  PRIMARY KEY (`id_rules`));
  
  DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createDQRule`(
	IN p_rules_name VARCHAR(30),
	IN p_rules_description VARCHAR(50),
	IN p_rules_environment VARCHAR(20),
	IN p_rules_command VARCHAR(200),
	IN p_rules_active BIT
)
BEGIN
    if ( select exists (select 1 from BucketList.tbl_dq_rules where rules_name = p_rules_name and rules_active=1) ) THEN
     
        select 'Rules Exists !!';
     
    ELSE
     
        insert into BucketList.tbl_dq_rules
        (
            rules_name,
            rules_description,
            rules_environment,
            rules_command,
            rules_active            
        )
        values
        (
            p_rules_name,
            p_rules_description,
            p_rules_environment,
            p_rules_command,
            p_rules_active   
        );
     
    END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_returnDQRule`(
    IN p_rules_name VARCHAR(50)
)
BEGIN
    select * from BucketList.tbl_dq_rules where rules_name = p_rules_name and rules_active='S';
END$$
DELIMITER ;
