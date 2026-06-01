CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TABLE IF NOT EXISTS news (
  id             SERIAL PRIMARY KEY,
  name           VARCHAR(255)  NOT NULL,
  date           DATE          NOT NULL,
  description    TEXT          NOT NULL,
  name_be        VARCHAR(255),
  name_en        VARCHAR(255),
  description_be TEXT,
  description_en TEXT,
  image_path     VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS admin_users (
  id            SERIAL PRIMARY KEY,
  username      VARCHAR(64)   NOT NULL,
  password_hash VARCHAR(255)  NOT NULL,
  is_active     BOOLEAN       NOT NULL DEFAULT TRUE,
  created_at    TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
  CONSTRAINT uq_admin_users_username UNIQUE (username)
);

CREATE OR REPLACE TRIGGER trg_admin_users_updated_at
  BEFORE UPDATE ON admin_users
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TABLE IF NOT EXISTS site_visits (
  id           BIGSERIAL PRIMARY KEY,
  visit_date   DATE         NOT NULL,
  visitor_key  CHAR(64)     NOT NULL,
  first_seen   TIMESTAMP    NOT NULL,
  last_seen    TIMESTAMP    NOT NULL,
  hits         INT          NOT NULL DEFAULT 1,
  CONSTRAINT uq_site_visits_date_visitor UNIQUE (visit_date, visitor_key)
);

CREATE INDEX IF NOT EXISTS idx_site_visits_visit_date ON site_visits (visit_date);

CREATE TABLE IF NOT EXISTS site_tabs (
  id              SERIAL PRIMARY KEY,
  slug            VARCHAR(120)  NOT NULL,
  title           VARCHAR(255)  NOT NULL,
  menu_title      VARCHAR(120)  NOT NULL,
  content_html    TEXT,
  sort_order      INT           NOT NULL DEFAULT 100,
  is_active       BOOLEAN       NOT NULL DEFAULT TRUE,
  open_in_new_tab BOOLEAN       NOT NULL DEFAULT FALSE,
  created_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
  CONSTRAINT uq_site_tabs_slug UNIQUE (slug)
);

CREATE INDEX IF NOT EXISTS idx_site_tabs_active_sort ON site_tabs (is_active, sort_order);

CREATE OR REPLACE TRIGGER trg_site_tabs_updated_at
  BEFORE UPDATE ON site_tabs
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TABLE IF NOT EXISTS site_pages (
  id           SERIAL PRIMARY KEY,
  slug         VARCHAR(120)  NOT NULL,
  title        VARCHAR(255)  NOT NULL,
  content_html TEXT,
  sort_order   INT           NOT NULL DEFAULT 100,
  is_active    BOOLEAN       NOT NULL DEFAULT TRUE,
  branch_id    VARCHAR(64),
  created_at   TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
  updated_at   TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
  CONSTRAINT uq_site_pages_slug UNIQUE (slug)
);

CREATE INDEX IF NOT EXISTS idx_site_pages_active_sort ON site_pages (is_active, sort_order);

CREATE OR REPLACE TRIGGER trg_site_pages_updated_at
  BEFORE UPDATE ON site_pages
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

INSERT INTO news (id, name, date, description, name_be, name_en, description_be, description_en, image_path)
VALUES
  (1,
   'День открытых дверей',
   '2025-05-15',
   'Приглашаем всех желающих на день открытых дверей, который состоится 25 мая в 15:00 в главном корпусе колледжа.',
   'Дзень адкрытых дзвярэй',
   'Open Day',
   'Запрашаем усіх жадаючых на дзень адкрытых дзвярэй, які адбудзецца 25 мая а 15:00 у галоўным корпусе каледжа.',
   'We invite everyone to the open day on 25 May at 15:00 in the main college building.',
   '/static/images/news_images/1655471619_4-kartinkof-club-p-kartinki-na-den-otkritikh-dverei-4.jpg'),
  (2,
   'Победа в конкурсе профмастерства',
   '2025-05-16',
   'Наши студенты заняли первое место в республиканском конкурсе профессионального мастерства по специальности "Программное обеспечение".',
   'Перамога ў конкурсе прафесійнага майстэрства',
   'Victory in the professional skills competition',
   'Нашы студэнты занялі першае месца ў рэспубліканскім конкурсе прафесійнага майстэрства па спецыяльнасці «Праграмнае забеспячэнне».',
   'Our students won first place in the national professional skills competition in the Software specialty.',
   '/static/images/news_images/images.png')
ON CONFLICT DO NOTHING;

SELECT setval('news_id_seq', (SELECT COALESCE(MAX(id), 0) FROM news));

INSERT INTO admin_users (username, password_hash, is_active)
VALUES ('admin', '$2b$12$k7dOeMUC/9L4i8Vx9Z9zku.I9M9ygis1WF0QAP8z668UYZLTKzvRa', TRUE)
ON CONFLICT DO NOTHING;
