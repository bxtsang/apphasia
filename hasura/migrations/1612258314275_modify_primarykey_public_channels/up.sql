alter table "public"."channels" drop constraint "channels_pkey";
alter table "public"."channels"
    add constraint "channels_pkey" 
    primary key ( "description" );
