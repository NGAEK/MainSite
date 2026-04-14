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
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
