-- add current date as partition
ALTER TABLE csv_contacts
  add IF NOT EXISTS PARTITION (created_date='${TODAY}')
  LOCATION '${INPUT}/uploads/created_date=${TODAY}/';


-- alter table csv_contacts drop if exists
-- partition(created_date='2020-02-02');
