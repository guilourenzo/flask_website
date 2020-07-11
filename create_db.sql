#CREATE DATABASE BucketList;

CREATE TABLE `BucketList`.`tbl_user` (
  `user_id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_name` VARCHAR(50) NULL,
  `user_username` VARCHAR(50) NULL,
  `user_password` VARCHAR(150) NULL,
  PRIMARY KEY (`user_id`));
  
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN p_name VARCHAR(50),
    IN p_username VARCHAR(50),
    IN p_password VARCHAR(150)
)
BEGIN
    if ( select exists (select 1 from BucketList.tbl_user where user_username = p_username) ) THEN
     
        select 'Username Exists !!';
     
    ELSE
     
        insert into BucketList.tbl_user
        (
            user_name,
            user_username,
            user_password
        )
        values
        (
            p_name,
            p_username,
            p_password
        );
     
    END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_returnUser`(
    IN p_username VARCHAR(50)
)
BEGIN
    select user_password from BucketList.tbl_user where user_username = p_username;
END$$
DELIMITER ;