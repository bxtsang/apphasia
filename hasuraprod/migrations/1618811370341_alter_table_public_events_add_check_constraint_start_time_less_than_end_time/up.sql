alter table "public"."events" add constraint "start_time_less_than_end_time" check (start_time <= end_time);
