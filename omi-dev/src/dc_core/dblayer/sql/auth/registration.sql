-- name: confirm_user<!
update dir.user
set state_id = 1,
    modifier = coalesce(email_new, email),
    modifydate = now(),
    email = coalesce(email_new, email),
    email_new = null,
    pw_hash = coalesce(:pw_hash_new, pw_hash_new, pw_hash),
    keyword = null,
    pw_hash_new = null
where guid = :uuid and keyword = :keyword
returning email;

-- name: change_password!
update dir.user
set modifier = :user,
    modifydate = now(),
    pw_hash = coalesce(:pw_hash_new, pw_hash)
where email = :user;

-- name: change_email<!
update dir.user
set state_id = 2,
    modifier = :user,
    modifydate = now(),
    email_new = :email_new,
    keyword = round(random()*899999)+100000,
    pw_hash_new = null
where email = :user
returning *;

--name: forgot_password<!
update dir.user
set state_id = 3,
    modifydate = now(),
    keyword = round(random()*899999)+100000,
    email_new = null,
    pw_hash_new = null
where email = :user
returning *;

--name: refresh_code<!
update dir.user
set modifydate = now(),
    keyword = round(random()*899999)+100000
where guid = :uuid and keyword is not null
returning *;
