--name: get_questions
with a as (
    select id, questionnaire_id, params from base.questionnaire_object where id = :questionnaire_object_id
),
b as (
    WITH RECURSIVE r AS (
        select id, concat(pos, '.') as pos, name, unit, parent_id, q.value as values,
        validation, condition, param, datatype, right('00' || pos, 3) || '.' as ps,
        section_code, calc_expr, q.dir_tablename, q.dir_columnname, q.multiplicator
        from base.question q
        where questionnaire_id = (select questionnaire_id from a) and parent_id is null and state_id > -1
        union
        select q.id, concat(r.pos, q.pos, '.'), q.name, q.unit, q.parent_id, q.value,
            q.validation, q.condition, q.param, q.datatype, concat(r.ps, right(concat('00', q.pos), 3), '.'),
        	q.section_code, q.calc_expr, q.dir_tablename, q.dir_columnname, q.multiplicator
        from base.question q
        join r on q.parent_id = r.id
        where state_id > -1
    )
    select r.*,
           (select * from dir.get_list(dir_tablename , dir_columnname)) as dir_values,
           t.value as val
    from r
    left join (
        select json_object_keys(val) as key, val->>json_object_keys(val) as value from (
            select (value::jsonb-'desc')::json as val from (
                select * from jsonb_array_elements((select params from base.questionnaire_object where id = (select id from a)))
                ) t1
            ) t2
        ) t on t.key = r.param
    --left join omi_model.d_omi_sections s on s.id = r.section_id
    where case when :full then 1=1 else param is not null end
    order by ps
)
select id, pos, name, unit, parent_id, coalesce(dir_values, values) as values,
    validation, condition, param, datatype, ps, section_code, calc_expr, val, multiplicator
from b;

--name: get_questions_by_questionnaire_id
WITH RECURSIVE r AS (
    select id, concat(pos, '.') as pos, name, unit, parent_id, q.value as values,
        validation, condition, param, datatype, right('00' || pos, 3) || '.' as ps, section_code
    from base.question q
    where questionnaire_id = :questionnaire_id and parent_id is null and state_id > -1
    union
    select q.id, concat(r.pos, q.pos, '.'), q.name, q.unit, q.parent_id, q.value,
        q.validation, q.condition, q.param, q.datatype, concat(r.ps, right(concat('00', q.pos), 3), '.'), q.section_code
    from base.question q
    join r on q.parent_id = r.id
    where state_id > -1
)
select *
from r
where param is not null
order by ps;