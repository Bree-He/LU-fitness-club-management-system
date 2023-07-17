CREATE EVENT pt_class_weekly_renewal_event
ON SCHEDULE
EVERY 1 WEEK
STARTS CURRENT_TIMESTAMP + INTERVAL 1 WEEK
DO
  INSERT INTO pt_class (pt_class_id, pt_class_name, avail_date, start_time, end_time, capacity, trainer_id)
  SELECT pt_class_id, pt_class_name, start_time, end_time, capacity, trainer_id, DATE_ADD(avail_date, INTERVAL 7 DAY)
  FROM pt_class
  WHERE avail_date = (SELECT MAX(avail_date) FROM pt_class);
