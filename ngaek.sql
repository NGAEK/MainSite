-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Время создания: Апр 30 2025 г., 10:45
-- Версия сервера: 10.4.32-MariaDB
-- Версия PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `ngaek`
--

-- --------------------------------------------------------

--
-- Структура таблицы `news` (name/description — русский; *_be / *_en — белорусский и английский)
--

CREATE TABLE `news` (
                        `id` int(11) NOT NULL,
                        `name` varchar(255) NOT NULL,
                        `date` date NOT NULL,
                        `description` text NOT NULL,
                        `name_be` varchar(255) DEFAULT NULL,
                        `name_en` varchar(255) DEFAULT NULL,
                        `description_be` text DEFAULT NULL,
                        `description_en` text DEFAULT NULL,
                        `image_path` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `news`
--

INSERT INTO `news` (`id`, `name`, `date`, `description`, `name_be`, `name_en`, `description_be`, `description_en`, `image_path`) VALUES
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
 'Наши студенты заняли первое место в республиканском конкурсе профессионального мастерства по специальности \"Программное обеспечение\".',
 'Перамога ў конкурсе прафесійнага майстэрства',
 'Victory in the professional skills competition',
 'Нашы студэнты занялі першае месца ў рэспубліканскім конкурсе прафесійнага майстэрства па спецыяльнасці «Праграмнае забеспячэнне».',
 'Our students won first place in the national professional skills competition in the Software specialty.',
 '/static/images/news_images/images.png');

-- --------------------------------------------------------

--
-- Структура таблицы `admin_users`
--

CREATE TABLE `admin_users` (
                               `id` int(11) NOT NULL,
                               `username` varchar(64) NOT NULL,
                               `password_hash` varchar(255) NOT NULL,
                               `is_active` tinyint(1) NOT NULL DEFAULT 1,
                               `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
                               `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `admin_users`
--

INSERT INTO `admin_users` (`id`, `username`, `password_hash`, `is_active`, `created_at`, `updated_at`) VALUES
(1, 'admin', '$2b$12$k7dOeMUC/9L4i8Vx9Z9zku.I9M9ygis1WF0QAP8z668UYZLTKzvRa', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- --------------------------------------------------------

--
-- Структура таблицы `site_visits`
--

CREATE TABLE `site_visits` (
                              `id` bigint(20) NOT NULL,
                              `visit_date` date NOT NULL,
                              `visitor_key` char(64) NOT NULL,
                              `first_seen` datetime NOT NULL,
                              `last_seen` datetime NOT NULL,
                              `hits` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `site_tabs`
--

CREATE TABLE `site_tabs` (
                            `id` int(11) NOT NULL,
                            `slug` varchar(120) NOT NULL,
                            `title` varchar(255) NOT NULL,
                            `menu_title` varchar(120) NOT NULL,
                            `content_html` mediumtext DEFAULT NULL,
                            `sort_order` int(11) NOT NULL DEFAULT 100,
                            `is_active` tinyint(1) NOT NULL DEFAULT 1,
                            `open_in_new_tab` tinyint(1) NOT NULL DEFAULT 0,
                            `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
                            `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `site_pages`
--

CREATE TABLE `site_pages` (
                             `id` int(11) NOT NULL,
                             `slug` varchar(120) NOT NULL,
                             `title` varchar(255) NOT NULL,
                             `content_html` mediumtext DEFAULT NULL,
                             `sort_order` int(11) NOT NULL DEFAULT 100,
                             `is_active` tinyint(1) NOT NULL DEFAULT 1,
                             `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
                             `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `news`
--
ALTER TABLE `news`
    ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `admin_users`
--
ALTER TABLE `admin_users`
    ADD PRIMARY KEY (`id`),
    ADD UNIQUE KEY `uq_admin_users_username` (`username`);

--
-- Индексы таблицы `site_visits`
--
ALTER TABLE `site_visits`
    ADD PRIMARY KEY (`id`),
    ADD UNIQUE KEY `uq_site_visits_date_visitor` (`visit_date`,`visitor_key`),
    ADD KEY `idx_site_visits_visit_date` (`visit_date`);

--
-- Индексы таблицы `site_tabs`
--
ALTER TABLE `site_tabs`
    ADD PRIMARY KEY (`id`),
    ADD UNIQUE KEY `uq_site_tabs_slug` (`slug`),
    ADD KEY `idx_site_tabs_active_sort` (`is_active`,`sort_order`);

--
-- Индексы таблицы `site_pages`
--
ALTER TABLE `site_pages`
    ADD PRIMARY KEY (`id`),
    ADD UNIQUE KEY `uq_site_pages_slug` (`slug`),
    ADD KEY `idx_site_pages_active_sort` (`is_active`,`sort_order`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `news`
--
ALTER TABLE `news`
    MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT для таблицы `admin_users`
--
ALTER TABLE `admin_users`
    MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT для таблицы `site_visits`
--
ALTER TABLE `site_visits`
    MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT для таблицы `site_tabs`
--
ALTER TABLE `site_tabs`
    MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT для таблицы `site_pages`
--
ALTER TABLE `site_pages`
    MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
