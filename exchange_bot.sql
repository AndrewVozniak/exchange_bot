-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Хост: localhost
-- Час створення: Лис 30 2022 р., 21:51
-- Версія сервера: 5.7.33
-- Версія PHP: 7.4.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База даних: `exchange_bot`
--

-- --------------------------------------------------------

--
-- Структура таблиці `admins`
--

CREATE TABLE `admins` (
  `id` int(11) NOT NULL,
  `telegram_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп даних таблиці `admins`
--

INSERT INTO `admins` (`id`, `telegram_id`) VALUES
(2, 934842562);

-- --------------------------------------------------------

--
-- Структура таблиці `coins`
--

CREATE TABLE `coins` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `commission` float NOT NULL DEFAULT '0',
  `parse_link` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп даних таблиці `coins`
--

INSERT INTO `coins` (`id`, `name`, `commission`, `parse_link`) VALUES
(1, 'BTC', 1.1, 'http://rate.sx/1BTC'),
(2, 'SRP', 1, 'http://rate.sx/1XRP'),
(3, 'TRX', 0, 'http://rate.sx/1TRX'),
(4, 'APT', 0, 'http://rate.sx/1APT'),
(5, 'ETH', 0, 'http://rate.sx/1ETH'),
(6, 'MATIC', 0, 'http://rate.sx/1MATIC'),
(7, 'DOGE', 0, 'http://rate.sx/1DOGE'),
(8, 'LTC', 0, 'http://rate.sx/1LTC'),
(9, 'TWT', 0, 'http://rate.sx/1TWT'),
(10, 'BNB', 0, 'http://rate.sx/1BNB');

-- --------------------------------------------------------

--
-- Структура таблиці `config`
--

CREATE TABLE `config` (
  `BOT_TOKEN` varchar(255) NOT NULL,
  `BTC` varchar(255) NOT NULL,
  `RULES` text NOT NULL,
  `BOT_NAME` varchar(255) NOT NULL,
  `ADMIN_TOKEN` varchar(255) NOT NULL,
  `ADMIN_PASSWORD` varchar(255) NOT NULL,
  `SUPPORT` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп даних таблиці `config`
--

INSERT INTO `config` (`BOT_TOKEN`, `BTC`, `RULES`, `BOT_NAME`, `ADMIN_TOKEN`, `ADMIN_PASSWORD`, `SUPPORT`) VALUES
('5824728463:AAGze_2G2n8AomZoFKLKJXgOy6CVdu1o_z4', 'bc1qfg9t7fwn0atn4yf9spca5502vk8dyhq8a9aqd8', 'ПРАВИЛА ОБМЕНА', 'exchange_bot', '5473224995:AAH2Xu9UCdBi5SyMgMUJEySGolz2yZoIWQY', 'ADMIN ', '@andre');

-- --------------------------------------------------------

--
-- Структура таблиці `operations`
--

CREATE TABLE `operations` (
  `id` int(11) NOT NULL,
  `type` varchar(255) NOT NULL,
  `coin` varchar(255) NOT NULL,
  `wallet_number` varchar(255) NOT NULL,
  `amount` decimal(10,5) NOT NULL,
  `user_id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп даних таблиці `operations`
--

INSERT INTO `operations` (`id`, `type`, `coin`, `wallet_number`, `amount`, `user_id`, `name`) VALUES
(1, 'BUY', 'BTC', 'bc1qfg9t7fwn0atn4yf9spca5502vk8dyhq8a9aqd8', '18032.96113', '934842562', ''),
(2, 'SELL', 'APT', '4441114444444444', '12.00000', '934842562', ''),
(3, 'BUY', 'LTC', 'bc1qfg9t7fwn0atn4yf9spca5502vk8dyhq8a9aqd8', '75.86630', '934842562', 'Dzonkan'),
(4, 'BUY', 'BTC', 'bc1qfg9t7fwn0atn4yf9spca5502vk8dyhq8a9aqd8', '18087.75532', '934842562', 'Dzonkan'),
(5, 'BUY', 'ADA', 'bc1qfg9t7fwn0atn4yf9spca5502vk8dyhq8a9aqd8', '3.77197', '934842562', 'Dzonkan');

--
-- Індекси збережених таблиць
--

--
-- Індекси таблиці `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`id`);

--
-- Індекси таблиці `coins`
--
ALTER TABLE `coins`
  ADD PRIMARY KEY (`id`);

--
-- Індекси таблиці `config`
--
ALTER TABLE `config`
  ADD UNIQUE KEY `BOT_TOKEN` (`BOT_TOKEN`);

--
-- Індекси таблиці `operations`
--
ALTER TABLE `operations`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT для збережених таблиць
--

--
-- AUTO_INCREMENT для таблиці `admins`
--
ALTER TABLE `admins`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблиці `coins`
--
ALTER TABLE `coins`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT для таблиці `operations`
--
ALTER TABLE `operations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
