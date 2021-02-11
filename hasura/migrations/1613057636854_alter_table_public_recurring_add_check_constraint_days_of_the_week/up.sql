alter table "public"."recurring" add constraint "days_of_the_week" check (0 <= day AND day <= 6);
