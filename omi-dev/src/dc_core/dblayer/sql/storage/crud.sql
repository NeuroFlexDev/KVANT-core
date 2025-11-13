--name: get_statements
select *
from base.statement o
where creator_id = :user_id and
    case when :state_id is null then state_id > -1
         else state_id = :state_id
    end
order by id desc;

--name: get_statement_by_id
select * from base.statement
where creator_id = :user_id and id = :id;

--name: get_statement_by_guid^
select * from base.statement
where guid = :guid;

-- name: create_statement<!
insert into base.statement (state_id, creator_id, createdate, guid, statementtype_id)
values(0, :user_id, now(), upper(uuid_generate_v4()::text), :statementtype_id)
returning *;

--name: update_statement<!
with upd as (
    update base.statement
        set state_id = 1,
            modifier_id = :user_id,
            modifydate = now(),
            statementtype_id = :statementtype_id,
            topic = :topic,
            body = :body
        where id = :id
        returning *
)
select *, (select name from dir.statementtype st where st.id = upd.statementtype_id) as statementtype_name
from upd;

-- name: delete_statement<!
update base.statement
set state_id = -1,
    modifier_id = :user_id,
    modifydate = now()
where id = :id
returning *;


--name: get_attachment_by_guid^
select * from base.attachment
where guid = :guid;

--name: get_attachments_by_statement_guid
select a.*
from base.attachment a
join base.statement s on s.id = a.statement_id
where s.creator_id = :user_id and s.guid = :statement_guid
order by id;

-- name: create_attachment<!
insert into base.attachment (state_id, creator_id, createdate, guid, path_to_object, statement_id, file_name, content_type)
values(0, :user_id, now(), upper(uuid_generate_v4()::text), :path_to_object, :statement_id, :file_name, :content_type)
returning *;

-- name: update_attachment<!
update base.attachment
set state_id = -1,
    modifier_id = :user_id,
    modifydate = now()
where id = :id
returning *;

-- name: delete_attachment<!
update base.attachment
set state_id = -1,
    modifier_id = :user_id,
    modifydate = now()
where guid = :guid
returning *;
