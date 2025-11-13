--name: get_objects
select *
from base.object o
where state_id > -1 and
    case when :user_id is not null then creator_id = :user_id
         else 1=1
    end
order by id;

--name: get_object_by_id
select * from base.object
where id = :id and
    case when :user_id is not null then creator_id = :user_id
         else 1=1
    end;

--name: get_object_by_params^
select * from base.object
where name = :name and address = :address and creator_id = :user_id;

-- name: create_object<!
insert into base.object (state_id, name, creator_id, createdate, guid, address)
values(1, :name, :user_id, now(), upper(uuid_generate_v4()::text), :address)
returning *;

--name: update_object<!
update base.object
set name = :name,
    modifier_id = :user_id,
    modifydate = now(),
    address = :address
where id = :id
returning *;

-- name: delete_object<!
update base.object
set state_id = -1
where id = :id
returning *;
