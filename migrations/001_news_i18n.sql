-- Добавление колонок для белорусского и английского текста новостей.
-- Выполнить на существующей БД: mysql -u USER -p ngaek < migrations/001_news_i18n.sql

ALTER TABLE `news`
  ADD COLUMN `name_be` VARCHAR(255) NULL DEFAULT NULL AFTER `description`,
  ADD COLUMN `name_en` VARCHAR(255) NULL DEFAULT NULL AFTER `name_be`,
  ADD COLUMN `description_be` TEXT NULL AFTER `name_en`,
  ADD COLUMN `description_en` TEXT NULL AFTER `description_be`;

-- Заполнить переводы из русских полей (замените на ручные переводы позже).
UPDATE `news` SET
  `name_be` = `name`,
  `name_en` = `name`,
  `description_be` = `description`,
  `description_en` = `description`
WHERE `name_be` IS NULL;
