alter table "public"."events" drop constraint "events_pkey";
alter table "public"."events"
    add constraint "events_pkey" 
    primary key ( "id" );
