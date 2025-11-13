--name: get_questionnaire_objects
select *,
    case when :calc_type = 'estimate' then (estimate->'result'->'estimate'->'cost'->>'value')::double precision
         when :calc_type = 'resource' then (estimate->'result'->'resource'->'cost'->>'value')::double precision
         when :calc_type = 'average' then (estimate->'result'->'average'->'cost'->>'value')::double precision
         else 0::double precision
    end as cost
from base.questionnaire_object
where state_id > -1 and
    case when :user_id is not null then creator_id = :user_id
         else 1=1
    end
order by id;

--name: get_questionnaire_object_by_id^
select *,
    case when :calc_type = 'estimate' then (estimate->'result'->'estimate'->'cost'->>'value')::double precision
         when :calc_type = 'resource' then (estimate->'result'->'resource'->'cost'->>'value')::double precision
         when :calc_type = 'average' then (estimate->'result'->'average'->'cost'->>'value')::double precision
         else 0::double precision
    end as cost
from base.questionnaire_object
where id = :id and
    case when :user_id is not null then creator_id = :user_id
         else 1=1
    end;

--name: get_questionnaire_object_by_object_id
select *,
    case when :calc_type = 'estimate' then (estimate->'result'->'estimate'->'cost'->>'value')::double precision
         when :calc_type = 'resource' then (estimate->'result'->'resource'->'cost'->>'value')::double precision
         when :calc_type = 'average' then (estimate->'result'->'average'->'cost'->>'value')::double precision
         else 0::double precision
    end as cost
from base.questionnaire_object
where object_id = :object_id and state_id > -1 and
    case when :user_id is not null then creator_id = :user_id
         else 1=1
    end
order by id;

--name: get_questionnaire_object_by_params^
select * from base.questionnaire_object
where name = :name and object_id = :object_id and questionnaire_id = :questionnaire_id and creator_id = :user_id;

-- name: create_questionnaire_object<!
insert into base.questionnaire_object (state_id, name, creator_id, createdate, guid, questionnaire_id, object_id, params)
WITH RECURSIVE r AS (
    select id, concat(pos, '.') as pos, name, parent_id, q.value, validation, condition, param, right('00' || pos, 3) || '.' as ps
    from base.question q
    where questionnaire_id = :questionnaire_id and parent_id is null and state_id > -1
    union
    select q.id, concat(r.pos, q.pos, '.'), q.name, q.parent_id, q.value, q.validation, q.condition, q.param, concat(r.ps, right(concat('00', q.pos), 3), '.')
    from base.question q
    join r on q.parent_id = r.id
    where state_id > -1
)
select 0, :name, :user_id, now(), upper(uuid_generate_v4()::text), :questionnaire_id, :object_id, array_to_json(array_agg(pr.obj))
from (select jsonb_build_object(param, o.value, 'desc', pos) as obj
      from r
      left join (select * from json_each_text((
                    select row_to_json(pr.*) from (
                        select name as a1, address as a2, 'Жилое здание (Ф1.3)' as a3, 'Да' as a125
                        from base.object where id = :object_id) pr))) o on o.key = r.param
      where param is not null
      order by ps) pr
returning *;

-- name: copy_questionnaire_object<!
insert into base.questionnaire_object (state_id, name, creator_id, createdate, guid, questionnaire_id, object_id, params)
select 0, concat_ws(' ', name, 'copy'), :user_id, now(), upper(uuid_generate_v4()::text), questionnaire_id, object_id, params
from base.questionnaire_object
where id = :questionnaire_object_id
returning *;

--name: update_questionnaire_object<!
update base.questionnaire_object
set state_id = :state_id,
    modifier_id = :user_id,
    modifydate = now(),
    name = :name,
    questionnaire_id = :questionnaire_id,
    object_id = :object_id,
    params = :params,
    response = :response,
    estimate = :estimate
where id = :id
returning *;

-- name: delete_questionnaire_object<!
update base.questionnaire_object
set state_id = -1,
    modifier_id = :user_id
where id = :id
returning *;

--name: recording_response<!
update base.questionnaire_object
set state_id = 2,
    modifydate = now(),
    response = coalesce(:response, response),
    estimate = coalesce(:estimate, estimate)
where id = :id
returning *;

