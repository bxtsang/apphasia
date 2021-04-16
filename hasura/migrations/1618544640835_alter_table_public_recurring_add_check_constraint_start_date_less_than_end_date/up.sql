alter table "public"."recurring" drop constraint "start_date_end_date";
alter table "public"."recurring" add constraint "start_date_less_than_end_date" check (start_date <= end_date);
