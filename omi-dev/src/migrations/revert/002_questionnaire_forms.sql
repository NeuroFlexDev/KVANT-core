-- Revert omi:002_questionnaire_forms from pg

BEGIN;

drop trigger if exists trg_touch_questionnaire_form_section on app.questionnaire_form_section;
drop trigger if exists trg_touch_questionnaire_form on app.questionnaire_form;

drop function if exists app.touch_questionnaire_form_section_updated_at();
drop function if exists app.touch_questionnaire_form_updated_at();

drop table if exists app.questionnaire_form_section;
drop table if exists app.questionnaire_form;

COMMIT;
