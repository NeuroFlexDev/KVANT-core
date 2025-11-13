-- Verify omi:002_questionnaire_forms on pg

BEGIN;

select 1 from app.questionnaire_form limit 1;
select 1 from app.questionnaire_form_section limit 1;

COMMIT;
