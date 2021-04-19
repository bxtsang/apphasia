CREATE TABLE public.projects (
    id integer NOT NULL,
    title text NOT NULL,
    owner_id integer NOT NULL,
    description text DEFAULT 'My Project'::text NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    voltypes text DEFAULT 'Project_Volunteer'::text NOT NULL,
    archive_reason text,
    is_active boolean DEFAULT true NOT NULL,
    colour text DEFAULT 'indigo'::text,
    google_drive_id text DEFAULT 'myid'::text NOT NULL
);
CREATE FUNCTION public.is_recurring(project_row public.projects) RETURNS boolean
    LANGUAGE plpgsql STABLE
    AS $$
    DECLARE
    total_events integer;
   BEGIN
    SELECT COUNT(id) into total_events FROM events WHERE project_id = project_row.id;
    IF total_events > 1 THEN RETURN TRUE;
    ELSE RETURN FALSE;
    END IF;
   END; $$;
CREATE FUNCTION public.set_current_timestamp_updated_at() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
  _new record;
BEGIN
  _new := NEW;
  _new."updated_at" = NOW();
  RETURN _new;
END;
$$;
CREATE FUNCTION public.upcoming_date(project_row public.projects) RETURNS date
    LANGUAGE plpgsql STABLE
    AS $$
   BEGIN
    RETURN (SELECT date from events WHERE date >= now() and project_id = project_row.id ORDER BY date LIMIT 1);
   END; $$;
CREATE FUNCTION public.update_events_values() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    days text;
    weeks text;
BEGIN
    IF NEW.name <> OLD.name THEN
         UPDATE events SET name = NEW.name WHERE recurr_id = NEW.id;
    END IF;
    IF NEW.note <> OLD.note THEN
         UPDATE events SET note = NEW.note WHERE recurr_id = NEW.id;
    END IF;
    IF NEW.start_time <> OLD.start_time THEN
        UPDATE events SET start_time = NEW.start_time WHERE recurr_id = NEW.id;
    END IF;
    IF NEW.end_time <> OLD.end_time THEN
        UPDATE events SET end_time = NEW.end_time WHERE recurr_id = NEW.id;
    END IF;
    IF NEW.end_date < OLD.end_date THEN
        DELETE FROM events WHERE date >= NEW.end_date AND recurr_id = NEW.id;
    END IF;
    IF NEW.day <> OLD.day THEN
        days := (NEW.day - OLD.day)::text || ' day';
        UPDATE events t1 SET date = x.myDate FROM (
        SELECT id, (date + days::interval) as myDate FROM events WHERE recurr_id = NEW.id) x
        WHERE t1.id = x.id;
    END IF;
    IF NEW.week <> OLD.week THEN
        weeks := (NEW.week - OLD.week)::text || ' weeks';
        UPDATE events t1 SET date = x.myDate FROM (
        SELECT id, (date + weeks::interval) as myDate FROM events WHERE recurr_id = NEW.id) x
        WHERE t1.id = x.id;
    END IF;
    RETURN NEW;
END;
$$;
CREATE TABLE public.channels (
    channel text NOT NULL
);
CREATE TABLE public.event_pwas (
    event_id integer NOT NULL,
    pwa_id integer NOT NULL,
    project_id integer NOT NULL
);
CREATE TABLE public.event_vols (
    event_id integer NOT NULL,
    vol_id integer NOT NULL,
    project_id integer NOT NULL
);
CREATE TABLE public.events (
    id integer NOT NULL,
    project_id integer,
    date date NOT NULL,
    recurr_id integer,
    note text,
    start_time time with time zone NOT NULL,
    end_time time with time zone NOT NULL,
    name text NOT NULL
);
CREATE SEQUENCE public.events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.events_id_seq OWNED BY public.events.id;
CREATE TABLE public.languages (
    language text NOT NULL,
    description text
);
CREATE TABLE public.latest (
    rc timestamp with time zone
);
CREATE TABLE public.notifications (
    id integer NOT NULL,
    staff_id integer NOT NULL,
    is_read boolean DEFAULT false NOT NULL,
    message text NOT NULL,
    type text NOT NULL,
    entity_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    operation text DEFAULT 'insert'::text NOT NULL
);
CREATE SEQUENCE public.notifications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.notifications_id_seq OWNED BY public.notifications.id;
CREATE TABLE public.people_external (
    id integer NOT NULL,
    email text,
    name text NOT NULL,
    date_joined date DEFAULT now() NOT NULL,
    dob date NOT NULL,
    gender bpchar NOT NULL,
    contact_num integer NOT NULL,
    address text NOT NULL,
    notes text,
    bio text NOT NULL,
    consent boolean NOT NULL,
    channel text
);
CREATE SEQUENCE public.people_external_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.people_external_id_seq OWNED BY public.people_external.id;
CREATE TABLE public.project_pwa (
    project_id integer NOT NULL,
    pwa_id integer NOT NULL
);
CREATE TABLE public.project_pwa_staffs (
    project_id integer NOT NULL,
    pwa_id integer NOT NULL,
    staff_id integer NOT NULL
);
COMMENT ON TABLE public.project_pwa_staffs IS 'Staffs assigned to a PWA for a particular project';
CREATE TABLE public.project_pwa_vols (
    project_id integer NOT NULL,
    pwa_id integer NOT NULL,
    vol_id integer NOT NULL
);
COMMENT ON TABLE public.project_pwa_vols IS 'Volunteers assigned to a PWA for a particular project';
CREATE TABLE public.project_staffs (
    project_id integer NOT NULL,
    staff_id integer NOT NULL
);
CREATE TABLE public.project_task_staffs (
    task_id integer NOT NULL,
    staff_id integer NOT NULL
);
CREATE TABLE public.project_task_status (
    status text NOT NULL
);
CREATE TABLE public.project_tasks (
    project_id integer NOT NULL,
    id integer NOT NULL,
    title text NOT NULL,
    description text,
    status text DEFAULT 'To-do'::text NOT NULL,
    due_date date NOT NULL,
    notes text
);
CREATE TABLE public.project_vol (
    project_id integer NOT NULL,
    vol_id integer NOT NULL,
    approved boolean DEFAULT false NOT NULL,
    interested boolean DEFAULT true NOT NULL
);
CREATE SEQUENCE public.projects_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.projects_id_seq OWNED BY public.projects.id;
CREATE TABLE public.pwa_comms (
    pwa_id integer NOT NULL,
    difficulty text NOT NULL
);
COMMENT ON TABLE public.pwa_comms IS 'Contains a list of communication difficulty of the PWAs';
CREATE TABLE public.pwa_contact_status (
    status text NOT NULL
);
CREATE TABLE public.pwas (
    id integer NOT NULL,
    contact_status text DEFAULT 'Not Contacted'::text NOT NULL,
    media_engagement_details text,
    hospital text,
    speech_therapist text,
    media_willingness boolean,
    stroke_date date,
    wheelchair boolean,
    last_contact_details text,
    comm_mode text DEFAULT 'Whatsapp'::text NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    archive_reason text,
    updated_at timestamp with time zone DEFAULT now()
);
CREATE SEQUENCE public.pwa_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.pwa_id_seq OWNED BY public.pwas.id;
CREATE TABLE public.pwa_languages (
    pwa_id integer NOT NULL,
    language text NOT NULL
);
CREATE TABLE public.pwa_nok (
    pwa_id integer NOT NULL,
    name text NOT NULL,
    contact_num integer NOT NULL,
    email text,
    relationship text NOT NULL
);
CREATE TABLE public.recurring (
    id integer NOT NULL,
    day integer NOT NULL,
    week integer,
    "interval" integer DEFAULT 1 NOT NULL,
    name text NOT NULL,
    frequency text NOT NULL,
    end_date date,
    start_time time with time zone NOT NULL,
    end_time time with time zone NOT NULL,
    infinite boolean DEFAULT false NOT NULL,
    project_id integer,
    start_date date DEFAULT now() NOT NULL,
    note text,
    CONSTRAINT days_of_the_week CHECK (((0 <= day) AND (day <= 6)))
);
COMMENT ON TABLE public.recurring IS 'day: 0-6, Mon-Sun week: 1,2,3,4,-1 First Week - Last Week of the Month Frequency: Weekly, Biweekly, Monthly';
CREATE SEQUENCE public.recurring_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.recurring_id_seq OWNED BY public.recurring.id;
CREATE TABLE public.recurring_pwas (
    recurring_id integer NOT NULL,
    pwa_id integer NOT NULL,
    project_id integer NOT NULL
);
CREATE TABLE public.recurring_vols (
    recurring_id integer NOT NULL,
    project_id integer NOT NULL,
    vol_id integer NOT NULL
);
CREATE TABLE public.roles (
    role text NOT NULL,
    description text NOT NULL
);
CREATE TABLE public.staff_languages (
    staff_id integer NOT NULL,
    language text NOT NULL
);
CREATE TABLE public.staff_supervisors (
    staff_id integer NOT NULL,
    supervisor_id integer NOT NULL,
    CONSTRAINT supervisor_staff CHECK ((staff_id <> supervisor_id))
);
CREATE SEQUENCE public.staffs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
CREATE TABLE public.staffs (
    id integer DEFAULT nextval('public.staffs_id_seq'::regclass) NOT NULL,
    email text NOT NULL,
    name text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    nickname text,
    dob date NOT NULL,
    gender bpchar NOT NULL,
    address text NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    date_joined date NOT NULL,
    contact_num integer NOT NULL,
    is_speech_therapist boolean DEFAULT false NOT NULL,
    profession text NOT NULL,
    ws_place text,
    bio text,
    role text NOT NULL,
    archive_reason text,
    updated_at timestamp with time zone DEFAULT now()
);
CREATE TABLE public.status (
    status text NOT NULL
);
CREATE SEQUENCE public.task_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.task_id_seq OWNED BY public.project_tasks.id;
CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.users_id_seq OWNED BY public.staffs.id;
CREATE TABLE public.vol_ic (
    vol_id integer NOT NULL,
    staff_id integer NOT NULL
);
CREATE TABLE public.vol_languages (
    vol_id integer NOT NULL,
    language text NOT NULL
);
CREATE TABLE public.vol_voltypes (
    vol_id integer NOT NULL,
    voltype text NOT NULL
);
CREATE TABLE public.voltypes (
    type text NOT NULL,
    description text NOT NULL
);
CREATE TABLE public.volunteers (
    id integer NOT NULL,
    nickname text,
    is_speech_therapist boolean DEFAULT false NOT NULL,
    profession text NOT NULL,
    ws_place text,
    status_reason text,
    rejected_date date,
    status text DEFAULT 'Pending Approval'::text NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    archive_reason text,
    updated_at timestamp with time zone DEFAULT now()
);
CREATE SEQUENCE public.volunteers_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE ONLY public.events ALTER COLUMN id SET DEFAULT nextval('public.events_id_seq'::regclass);
ALTER TABLE ONLY public.notifications ALTER COLUMN id SET DEFAULT nextval('public.notifications_id_seq'::regclass);
ALTER TABLE ONLY public.people_external ALTER COLUMN id SET DEFAULT nextval('public.people_external_id_seq'::regclass);
ALTER TABLE ONLY public.project_tasks ALTER COLUMN id SET DEFAULT nextval('public.task_id_seq'::regclass);
ALTER TABLE ONLY public.projects ALTER COLUMN id SET DEFAULT nextval('public.projects_id_seq'::regclass);
ALTER TABLE ONLY public.recurring ALTER COLUMN id SET DEFAULT nextval('public.recurring_id_seq'::regclass);
ALTER TABLE ONLY public.channels
    ADD CONSTRAINT channels_pkey PRIMARY KEY (channel);
ALTER TABLE ONLY public.event_pwas
    ADD CONSTRAINT event_pwas_pkey PRIMARY KEY (pwa_id, event_id, project_id);
ALTER TABLE ONLY public.event_vols
    ADD CONSTRAINT event_vols_pkey PRIMARY KEY (vol_id, event_id, project_id);
ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_id_project_id_key UNIQUE (id, project_id);
ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.languages
    ADD CONSTRAINT languages_pkey PRIMARY KEY (language);
ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.people_external
    ADD CONSTRAINT people_external_contact_num_key UNIQUE (contact_num);
ALTER TABLE ONLY public.people_external
    ADD CONSTRAINT people_external_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.project_pwa_staffs
    ADD CONSTRAINT project_pwa_staffs_pkey PRIMARY KEY (project_id, pwa_id, staff_id);
ALTER TABLE ONLY public.project_pwa_vols
    ADD CONSTRAINT project_pwa_vols_pkey PRIMARY KEY (project_id, pwa_id, vol_id);
ALTER TABLE ONLY public.project_staffs
    ADD CONSTRAINT project_staffs_pkey PRIMARY KEY (project_id, staff_id);
ALTER TABLE ONLY public.project_task_staffs
    ADD CONSTRAINT project_task_staffs_pkey PRIMARY KEY (task_id, staff_id);
ALTER TABLE ONLY public.project_task_status
    ADD CONSTRAINT project_task_status_pkey PRIMARY KEY (status);
ALTER TABLE ONLY public.project_tasks
    ADD CONSTRAINT project_tasks_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.project_vol
    ADD CONSTRAINT project_vol_pkey PRIMARY KEY (project_id, vol_id);
ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.project_pwa
    ADD CONSTRAINT projects_pwa_pkey PRIMARY KEY (project_id, pwa_id);
ALTER TABLE ONLY public.pwa_comms
    ADD CONSTRAINT pwa_comms_pkey PRIMARY KEY (pwa_id, difficulty);
ALTER TABLE ONLY public.pwa_contact_status
    ADD CONSTRAINT pwa_contact_status_pkey PRIMARY KEY (status);
ALTER TABLE ONLY public.pwa_languages
    ADD CONSTRAINT pwa_languages_pkey PRIMARY KEY (pwa_id, language);
ALTER TABLE ONLY public.pwa_nok
    ADD CONSTRAINT pwa_nok_pkey PRIMARY KEY (pwa_id, contact_num);
ALTER TABLE ONLY public.pwas
    ADD CONSTRAINT pwa_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.recurring
    ADD CONSTRAINT recurring_id_project_id_key UNIQUE (id, project_id);
ALTER TABLE ONLY public.recurring
    ADD CONSTRAINT recurring_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.recurring_pwas
    ADD CONSTRAINT recurring_pwas_pkey PRIMARY KEY (recurring_id, pwa_id, project_id);
ALTER TABLE ONLY public.recurring_vols
    ADD CONSTRAINT recurring_vols_pkey PRIMARY KEY (recurring_id, project_id, vol_id);
ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (role);
ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_role_key UNIQUE (role);
ALTER TABLE ONLY public.staff_languages
    ADD CONSTRAINT staff_languages_pkey PRIMARY KEY (staff_id, language);
ALTER TABLE ONLY public.staff_supervisors
    ADD CONSTRAINT staff_supervisors_pkey PRIMARY KEY (supervisor_id, staff_id);
ALTER TABLE ONLY public.staffs
    ADD CONSTRAINT staffs_contact_num_key UNIQUE (contact_num);
ALTER TABLE ONLY public.status
    ADD CONSTRAINT status_pkey PRIMARY KEY (status);
ALTER TABLE ONLY public.staffs
    ADD CONSTRAINT users_email_key UNIQUE (email);
ALTER TABLE ONLY public.staffs
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.vol_languages
    ADD CONSTRAINT vol_languages_pkey PRIMARY KEY (vol_id, language);
ALTER TABLE ONLY public.vol_ic
    ADD CONSTRAINT vol_supervisors_pkey PRIMARY KEY (vol_id, staff_id);
ALTER TABLE ONLY public.vol_voltypes
    ADD CONSTRAINT vol_voltypes_pkey PRIMARY KEY (vol_id, voltype);
ALTER TABLE ONLY public.voltypes
    ADD CONSTRAINT voltypes_pkey PRIMARY KEY (type);
ALTER TABLE ONLY public.volunteers
    ADD CONSTRAINT volunteers_pkey PRIMARY KEY (id);
CREATE TRIGGER set_public_project_tasks_updated_at BEFORE UPDATE ON public.project_tasks FOR EACH ROW EXECUTE PROCEDURE public.set_current_timestamp_updated_at();
COMMENT ON TRIGGER set_public_project_tasks_updated_at ON public.project_tasks IS 'trigger to set value of column "updated_at" to current timestamp on row update';
CREATE TRIGGER set_public_projects_updated_at BEFORE UPDATE ON public.projects FOR EACH ROW EXECUTE PROCEDURE public.set_current_timestamp_updated_at();
COMMENT ON TRIGGER set_public_projects_updated_at ON public.projects IS 'trigger to set value of column "updated_at" to current timestamp on row update';
CREATE TRIGGER set_public_pwas_updated_at BEFORE UPDATE ON public.pwas FOR EACH ROW EXECUTE PROCEDURE public.set_current_timestamp_updated_at();
COMMENT ON TRIGGER set_public_pwas_updated_at ON public.pwas IS 'trigger to set value of column "updated_at" to current timestamp on row update';
CREATE TRIGGER set_public_staffs_updated_at BEFORE UPDATE ON public.staffs FOR EACH ROW EXECUTE PROCEDURE public.set_current_timestamp_updated_at();
COMMENT ON TRIGGER set_public_staffs_updated_at ON public.staffs IS 'trigger to set value of column "updated_at" to current timestamp on row update';
CREATE TRIGGER set_public_volunteers_updated_at BEFORE UPDATE ON public.volunteers FOR EACH ROW EXECUTE PROCEDURE public.set_current_timestamp_updated_at();
COMMENT ON TRIGGER set_public_volunteers_updated_at ON public.volunteers IS 'trigger to set value of column "updated_at" to current timestamp on row update';
CREATE TRIGGER update_events_values_trigger AFTER UPDATE ON public.recurring FOR EACH ROW EXECUTE PROCEDURE public.update_events_values();
ALTER TABLE ONLY public.event_pwas
    ADD CONSTRAINT event_pwas_project_id_event_id_fkey FOREIGN KEY (project_id, event_id) REFERENCES public.events(project_id, id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.event_pwas
    ADD CONSTRAINT event_pwas_project_id_pwa_id_fkey FOREIGN KEY (project_id, pwa_id) REFERENCES public.project_pwa(project_id, pwa_id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.event_vols
    ADD CONSTRAINT event_vols_project_id_event_id_fkey FOREIGN KEY (project_id, event_id) REFERENCES public.events(project_id, id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.event_vols
    ADD CONSTRAINT event_vols_vol_id_project_id_fkey FOREIGN KEY (vol_id, project_id) REFERENCES public.project_vol(vol_id, project_id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_recurr_id_fkey FOREIGN KEY (recurr_id) REFERENCES public.recurring(id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_staff_id_fkey FOREIGN KEY (staff_id) REFERENCES public.staffs(id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.people_external
    ADD CONSTRAINT people_external_channel_fkey FOREIGN KEY (channel) REFERENCES public.channels(channel) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE ONLY public.project_pwa_staffs
    ADD CONSTRAINT project_pwa_staffs_project_id_pwa_id_fkey FOREIGN KEY (project_id, pwa_id) REFERENCES public.project_pwa(project_id, pwa_id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.project_pwa_staffs
    ADD CONSTRAINT project_pwa_staffs_staff_id_fkey FOREIGN KEY (staff_id) REFERENCES public.staffs(id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.project_pwa_vols
    ADD CONSTRAINT project_pwa_vols_project_id_pwa_id_fkey FOREIGN KEY (project_id, pwa_id) REFERENCES public.project_pwa(project_id, pwa_id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.project_pwa_vols
    ADD CONSTRAINT project_pwa_vols_vol_id_fkey FOREIGN KEY (vol_id) REFERENCES public.volunteers(id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.project_staffs
    ADD CONSTRAINT project_staffs_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.project_staffs
    ADD CONSTRAINT project_staffs_staff_id_fkey FOREIGN KEY (staff_id) REFERENCES public.staffs(id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.project_task_staffs
    ADD CONSTRAINT project_task_staffs_staff_id_fkey FOREIGN KEY (staff_id) REFERENCES public.staffs(id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.project_task_staffs
    ADD CONSTRAINT project_task_staffs_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.project_tasks(id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.project_tasks
    ADD CONSTRAINT project_tasks_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.project_tasks
    ADD CONSTRAINT project_tasks_status_fkey FOREIGN KEY (status) REFERENCES public.project_task_status(status) ON UPDATE RESTRICT ON DELETE RESTRICT;
ALTER TABLE ONLY public.project_vol
    ADD CONSTRAINT project_vol_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.project_vol
    ADD CONSTRAINT project_vol_vol_id_fkey FOREIGN KEY (vol_id) REFERENCES public.volunteers(id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.staffs(id) ON UPDATE RESTRICT ON DELETE RESTRICT;
ALTER TABLE ONLY public.project_pwa
    ADD CONSTRAINT projects_pwa_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.project_pwa
    ADD CONSTRAINT projects_pwa_pwa_id_fkey FOREIGN KEY (pwa_id) REFERENCES public.pwas(id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_voltypes_fkey FOREIGN KEY (voltypes) REFERENCES public.voltypes(type) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.pwa_comms
    ADD CONSTRAINT pwa_comms_pwa_id_fkey FOREIGN KEY (pwa_id) REFERENCES public.pwas(id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.pwa_languages
    ADD CONSTRAINT pwa_languages_language_fkey FOREIGN KEY (language) REFERENCES public.languages(language) ON UPDATE RESTRICT ON DELETE RESTRICT;
ALTER TABLE ONLY public.pwa_languages
    ADD CONSTRAINT pwa_languages_pwa_id_fkey FOREIGN KEY (pwa_id) REFERENCES public.pwas(id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.pwa_nok
    ADD CONSTRAINT pwa_nok_pwa_id_fkey FOREIGN KEY (pwa_id) REFERENCES public.pwas(id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.pwas
    ADD CONSTRAINT pwas_contact_status_fkey FOREIGN KEY (contact_status) REFERENCES public.pwa_contact_status(status) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE ONLY public.pwas
    ADD CONSTRAINT pwas_id_fkey FOREIGN KEY (id) REFERENCES public.people_external(id) ON UPDATE RESTRICT ON DELETE RESTRICT;
ALTER TABLE ONLY public.recurring_pwas
    ADD CONSTRAINT recurring_pwas_pwa_id_project_id_fkey FOREIGN KEY (pwa_id, project_id) REFERENCES public.project_pwa(pwa_id, project_id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.recurring_pwas
    ADD CONSTRAINT recurring_pwas_recurring_id_project_id_fkey FOREIGN KEY (recurring_id, project_id) REFERENCES public.recurring(id, project_id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.recurring_vols
    ADD CONSTRAINT recurring_vols_project_id_vol_id_fkey FOREIGN KEY (project_id, vol_id) REFERENCES public.project_vol(project_id, vol_id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.recurring_vols
    ADD CONSTRAINT recurring_vols_recurring_id_project_id_fkey FOREIGN KEY (recurring_id, project_id) REFERENCES public.recurring(id, project_id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.staff_languages
    ADD CONSTRAINT staff_languages_language_fkey FOREIGN KEY (language) REFERENCES public.languages(language) ON UPDATE RESTRICT ON DELETE RESTRICT;
ALTER TABLE ONLY public.staff_languages
    ADD CONSTRAINT staff_languages_staff_id_fkey FOREIGN KEY (staff_id) REFERENCES public.staffs(id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.staff_supervisors
    ADD CONSTRAINT staff_supervisors_staff_id_fkey FOREIGN KEY (staff_id) REFERENCES public.staffs(id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.staff_supervisors
    ADD CONSTRAINT staff_supervisors_supervisor_id_fkey FOREIGN KEY (supervisor_id) REFERENCES public.staffs(id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.staffs
    ADD CONSTRAINT staffs_role_fkey FOREIGN KEY (role) REFERENCES public.roles(role) ON UPDATE RESTRICT ON DELETE RESTRICT;
ALTER TABLE ONLY public.vol_languages
    ADD CONSTRAINT vol_languages_language_fkey FOREIGN KEY (language) REFERENCES public.languages(language) ON UPDATE RESTRICT ON DELETE RESTRICT;
ALTER TABLE ONLY public.vol_languages
    ADD CONSTRAINT vol_languages_vol_id_fkey FOREIGN KEY (vol_id) REFERENCES public.volunteers(id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.vol_ic
    ADD CONSTRAINT vol_supervisors_staff_id_fkey FOREIGN KEY (staff_id) REFERENCES public.staffs(id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.vol_ic
    ADD CONSTRAINT vol_supervisors_vol_id_fkey FOREIGN KEY (vol_id) REFERENCES public.volunteers(id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.vol_voltypes
    ADD CONSTRAINT vol_voltypes_vol_id_fkey FOREIGN KEY (vol_id) REFERENCES public.volunteers(id) ON UPDATE RESTRICT ON DELETE CASCADE;
ALTER TABLE ONLY public.vol_voltypes
    ADD CONSTRAINT vol_voltypes_voltype_fkey FOREIGN KEY (voltype) REFERENCES public.voltypes(type) ON UPDATE RESTRICT ON DELETE RESTRICT;
ALTER TABLE ONLY public.volunteers
    ADD CONSTRAINT volunteers_status_fkey FOREIGN KEY (status) REFERENCES public.status(status) ON UPDATE RESTRICT ON DELETE RESTRICT;
ALTER TABLE ONLY public.volunteers
    ADD CONSTRAINT volunteers_vol_id_fkey FOREIGN KEY (id) REFERENCES public.people_external(id) ON UPDATE RESTRICT ON DELETE RESTRICT;
