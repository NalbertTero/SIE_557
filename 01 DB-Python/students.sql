CREATE TABLE `final_project`.`students` 
( `student_id` INT NOT NULL AUTO_INCREMENT , 
`last_name` VARCHAR(32) NOT NULL , 
`first_name` VARCHAR(32) NOT NULL , 
`birthdate` DATE NULL , 
`gender` CHAR(1) NULL , 
`grade` ENUM('1','2','4','5','6','7','8','9','10','11','12') NOT NULL , 
PRIMARY KEY (`student_id`)) ENGINE = InnoDB;
