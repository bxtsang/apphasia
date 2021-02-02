alter table "public"."pwas" add foreign key ("channel") references "public"."channels"("channel") on update cascade on delete restrict;
