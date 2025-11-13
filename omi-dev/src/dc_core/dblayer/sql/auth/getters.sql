-- name: get_user_for_auth^
select *
from dir.user
where
    state_id > 0
    and (edate is null or edate > now())
    and lower(email) = lower(:email)
    and case when coalesce(:pw_hash, null) is not null then
        pw_hash = :pw_hash
    else 1=1 end;
