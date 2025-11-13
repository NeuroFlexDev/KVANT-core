--name: get_questionnaires
select *
from base.questionnaire o;

--name: get_questionnaire_by_id
select * from base.questionnaire
where id = :questionnaire_id;

-- name: create_questionnaire<!
insert into base.questionnaire (state_id, creator_id, createdate, guid)
values(1, :user_id, now(), upper(uuid_generate_v4()::text))
returning *;

--name: update_questionnaire<!
update base.questionnaire
set modifier_id = :user_id,
    modifydate = now(),
    name = :name
where id = :questionnaire_id
returning *;

-- name: delete_questionnaire<!
update base.questionnaire
set state_id = -1
where id = :questionnaire_id
returning id;
