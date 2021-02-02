ALTER TABLE "public"."pwas" ADD COLUMN "speak_media" text;
ALTER TABLE "public"."pwas" ALTER COLUMN "speak_media" DROP NOT NULL;
ALTER TABLE "public"."pwas" ADD CONSTRAINT pwa_speak_media_fkey FOREIGN KEY (speak_media) REFERENCES "public"."answers" (answer) ON DELETE restrict ON UPDATE cascade;
