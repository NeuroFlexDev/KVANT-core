-- name: get_users
select *,
    (select name from dir.state where id = u.state_id) as state_name
from dir.user u
order by id;

-- name: get_user_by_email^
select *,
    (select name from dir.state where id = u.state_id) as state_name
from dir.user u
where email = :email;

-- name: get_user_by_id^
select *
from dir.user
where id = :id;

--name: get_user_by_guid^
select *, (coalesce(modifydate, now()) + interval ':timeout minutes' < now()) as is_expired
from dir.user
where guid = :uuid;

-- name: create_user<!
insert into dir.user (state_id, creator, createdate, email, first_name, middle_name, last_name, pw_hash, guid, keyword, role_ids)
values(0, :user, now(), :email, :first_name, :middle_name, :last_name, :pw_hash, upper(uuid_generate_v4()::text), round(random()*899999)+100000, '{3}')
ON CONFLICT (email) DO UPDATE
SET modifydate = now(),
    keyword = round(random()*899999)+100000,
    pw_hash_new = :pw_hash
returning *;

-- name: create_user_omi<!
insert into dir.user (state_id, creator, createdate, email, first_name, middle_name, last_name, pw_hash, guid, keyword, role_ids,
    phone, organization, activity_id)
values(0, :user, now(), :email, :first_name, :middle_name, :last_name, :pw_hash, upper(uuid_generate_v4()::text), round(random()*899999)+100000, '{3}',
    :phone, :organization, :activity_id)
ON CONFLICT (email) DO UPDATE
SET modifydate = now(),
    keyword = round(random()*899999)+100000,
    pw_hash_new = :pw_hash
returning *;

-- name: update_user<!
update dir.user
set state_id = 1,
    modifier = :user,
    modifydate = now(),
    first_name = coalesce(:first_name, first_name),
    middle_name = coalesce(:middle_name, middle_name),
    last_name = coalesce(:last_name, last_name),
    --pw_hash = coalesce(:pw_hash, pw_hash),
    edate = coalesce(:edate, edate),
    is_admin = coalesce(:is_admin, is_admin),
    role_ids = coalesce(:role_ids, role_ids)
where email = :email
returning *;

-- name: delete_user<!
update dir.user
set state_id = -1
where email = :email
returning id;
