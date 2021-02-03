alter table "public"."pwas" add foreign key ("wheelchair") references "public"."answers"("answer") on update restrict on delete restrict;
