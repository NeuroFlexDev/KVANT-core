-- name: list_forms
select id,
       guid,
       user_id,
       title,
       description,
       status,
       current_step,
       metadata,
       is_deleted,
       created_at,
       updated_at
from app.questionnaire_form
where user_id = :user_id
  and is_deleted = false
order by created_at desc;

-- name: get_form_by_id^
select id,
       guid,
       user_id,
       title,
       description,
       status,
       current_step,
       metadata,
       is_deleted,
       created_at,
       updated_at
from app.questionnaire_form
where id = :form_id
  and user_id = :user_id
  and is_deleted = false;

-- name: get_form_with_sections^
select f.*,
       coalesce(
           jsonb_agg(
               jsonb_build_object(
                   'id', s.id,
                   'form_id', s.form_id,
                   'section_key', s.section_key,
                   'title', s.title,
                   'order_index', s.order_index,
                   'data', s.data,
                   'is_completed', s.is_completed,
                   'completed_at', s.completed_at,
                   'created_at', s.created_at,
                   'updated_at', s.updated_at
               ) order by s.order_index
           ) filter (where s.id is not null),
           '[]'::jsonb
       ) as sections
from app.questionnaire_form f
left join app.questionnaire_form_section s on s.form_id = f.id
where f.id = :form_id
  and f.user_id = :user_id
  and f.is_deleted = false
group by f.id;

-- name: create_form<!
insert into app.questionnaire_form (
    user_id,
    title,
    description,
    status,
    current_step,
    metadata
) values (
    :user_id,
    :title,
    :description,
    coalesce(:status, 'draft'),
    coalesce(:current_step, 0),
    coalesce((:metadata)::jsonb, '{}'::jsonb)
) returning *;

-- name: update_form<!
update app.questionnaire_form
set title = coalesce(:title, title),
    description = coalesce(:description, description),
    status = coalesce(:status, status),
    current_step = coalesce(:current_step, current_step),
    metadata = coalesce((:metadata)::jsonb, metadata),
    updated_at = now()
where id = :form_id
  and user_id = :user_id
  and is_deleted = false
returning *;

-- name: mark_form_deleted<!
update app.questionnaire_form
set is_deleted = true,
    updated_at = now()
where id = :form_id
  and user_id = :user_id
  and is_deleted = false
returning *;

-- name: list_sections
select id,
       form_id,
       section_key,
       title,
       order_index,
       data,
       is_completed,
       completed_at,
       created_at,
       updated_at
from app.questionnaire_form_section
where form_id = :form_id
order by order_index;

-- name: get_section^
select id,
       form_id,
       section_key,
       title,
       order_index,
       data,
       is_completed,
       completed_at,
       created_at,
       updated_at
from app.questionnaire_form_section
where form_id = :form_id
  and section_key = :section_key;

-- name: upsert_section<!
insert into app.questionnaire_form_section (
    form_id,
    section_key,
    title,
    order_index,
    data,
    is_completed,
    completed_at
) values (
    :form_id,
    :section_key,
    :title,
    :order_index,
    coalesce((:data)::jsonb, '{}'::jsonb),
    :is_completed,
    :completed_at
)
on conflict (form_id, section_key)
do update
set title = coalesce(excluded.title, app.questionnaire_form_section.title),
    order_index = coalesce(excluded.order_index, app.questionnaire_form_section.order_index),
    data = excluded.data,
    is_completed = excluded.is_completed,
    completed_at = excluded.completed_at,
    updated_at = now()
returning *;
