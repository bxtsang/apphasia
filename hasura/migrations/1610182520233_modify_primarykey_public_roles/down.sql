alter table "public"."roles" drop constraint "roles_pkey";
alter table "public"."roles"
    add constraint "roles_pkey" 
    primary key ( "id" );
