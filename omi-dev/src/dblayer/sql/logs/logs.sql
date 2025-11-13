--name: get_logs
select *
from log.log
where creator_id = coalesce(:user_id, creator_id)
      and createdate between coalesce(:date_from, '2000-01-01'::timestamp) and coalesce(:date_to, now())
      and table_name = coalesce(:table_name, table_name)
      and record_id = coalesce(:record_id, record_id)
      and action = coalesce(:action, action)
order by id;

-- name: create_log<!
insert into log.log (creator_id, createdate, table_name, record_id, action)
values(:user_id, now(), :table_name, :record_id, :action)
returning *;