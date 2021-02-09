ALTER TABLE "public"."pwas" ADD COLUMN "last_stroke" text;
ALTER TABLE "public"."pwas" ALTER COLUMN "last_stroke" DROP NOT NULL;
ALTER TABLE "public"."pwas" ADD CONSTRAINT pwa_last_stroke_fkey FOREIGN KEY (last_stroke) REFERENCES "public"."last_stroke" (when) ON DELETE restrict ON UPDATE restrict;
