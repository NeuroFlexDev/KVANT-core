-- Deploy omi:002_questionnaire_forms to pg

BEGIN;

create schema if not exists app;

create table if not exists app.questionnaire_form (
    id            bigserial primary key,
    user_id       integer      not null references dir.user(id) on delete cascade,
    guid          text         not null default upper(uuid_generate_v4()::text),
    title         text         not null,
    description   text,
    status        text         not null default 'draft',
    current_step  integer      not null default 0,
    metadata      jsonb        not null default '{}'::jsonb,
    is_deleted    boolean      not null default false,
    created_at    timestamptz  not null default now(),
    updated_at    timestamptz  not null default now()
);

create unique index if not exists idx_questionnaire_form_guid
    on app.questionnaire_form (guid);

create index if not exists idx_questionnaire_form_user
    on app.questionnaire_form (user_id)
    where is_deleted = false;

create table if not exists app.questionnaire_form_section (
    id            bigserial primary key,
    form_id       bigint       not null references app.questionnaire_form(id) on delete cascade,
    section_key   text         not null,
    title         text,
    order_index   integer      not null default 0,
    data          jsonb        not null default '{}'::jsonb,
    is_completed  boolean      not null default false,
    completed_at  timestamptz,
    created_at    timestamptz  not null default now(),
    updated_at    timestamptz  not null default now()
);

create unique index if not exists idx_questionnaire_form_section_unique
    on app.questionnaire_form_section (form_id, section_key);

create index if not exists idx_questionnaire_form_section_form
    on app.questionnaire_form_section (form_id);

create or replace function app.touch_questionnaire_form_updated_at()
returns trigger
language plpgsql
as $$
begin
    new.updated_at = now();
    return new;
end;
$$;

drop trigger if exists trg_touch_questionnaire_form on app.questionnaire_form;
create trigger trg_touch_questionnaire_form
before update on app.questionnaire_form
for each row
execute procedure app.touch_questionnaire_form_updated_at();

create or replace function app.touch_questionnaire_form_section_updated_at()
returns trigger
language plpgsql
as $$
begin
    new.updated_at = now();
    return new;
end;
$$;

drop trigger if exists trg_touch_questionnaire_form_section on app.questionnaire_form_section;
create trigger trg_touch_questionnaire_form_section
before update on app.questionnaire_form_section
for each row
execute procedure app.touch_questionnaire_form_section_updated_at();

COMMIT;
