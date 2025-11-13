-- name: get_users_omi
select *,
    (select name from dir.state where id = u.state_id) as state_name
from dir.user u
where state_id = any(string_to_array(:states,',')::int[])
order by id;

-- name: get_user_by_email^
select *,
    (select name from dir.state where id = u.state_id) as state_name
from dir.user u
where email = :email;

--name: get_user_by_guid^
select *, (coalesce(modifydate, now()) + interval ':timeout minutes' < now()) as is_expired
from dir.user
where guid = :uuid;

-- name: user_accept<!
update dir.user
set state_id = 1,
    modifier = :user,
    modifydate = now()
where email = :email
returning id;

-- name: create_user_omi<!
insert into dir.user (state_id, createdate, email, guid)
values(0, now(), :email, upper(uuid_generate_v4()::text))
returning *;

-- name: update_user_omi<!
update dir.user
set --state_id = 1,
    modifier = :user,
    modifydate = now(),
    first_name = :first_name,
    middle_name = :middle_name,
    last_name = :last_name,
    --pw_hash = coalesce(:pw_hash, pw_hash),
    edate = :edate,
    --is_admin = coalesce(:is_admin, is_admin),
    role_ids = :role_ids,
    phone = :phone,
    organization = :organization
    --activity_id = :activity_id,
    --calc_number = :calc_number
where email = :email
returning *;

-- name: delete_user_omi<!
update dir.user
set state_id = -1,
    modifier = :user,
    modifydate = now()
where email = :email
returning id;

--name: replenish_account<!
update dir.user
set modifier = :user,
    modifydate = now(),
    calc_number = coalesce(calc_number, 0) + :value
where email = :email
returning *;
