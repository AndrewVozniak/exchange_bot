-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Хост: localhost
-- Час створення: Лис 29 2022 р., 10:47
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
-- Структура таблиці `config`
--

CREATE TABLE `config` (
  `BOT_TOKEN` varchar(255) NOT NULL,
  `BTC` varchar(255) NOT NULL,
  `CARD_NUMBER` varchar(255) NOT NULL,
  `RULES` text NOT NULL,
  `BOT_NAME` varchar(255) NOT NULL,
  `ADMIN_TOKEN` varchar(255) NOT NULL,
  `ADMIN_PASSWORD` varchar(255) NOT NULL,
  `SUPPORT` varchar(255) NOT NULL,
  `DESCRIPTION` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп даних таблиці `config`
--

INSERT INTO `config` (`BOT_TOKEN`, `BTC`, `CARD_NUMBER`, `RULES`, `BOT_NAME`, `ADMIN_TOKEN`, `ADMIN_PASSWORD`, `SUPPORT`, `DESCRIPTION`) VALUES
('5824728463:AAGze_2G2n8AomZoFKLKJXgOy6CVdu1o_z4', 'bc1qfg9t7fwn0atn4yf9spca5502vk8dyhq8a9aqd8', '4441 1144 4444 1111', 'Бонус\r\n\r\nНаш обменник предлагает всем своим клиентам поучаствовать в партнёрской программе.\r\n\r\nПриглашайте друзей по специальной ссылке и получайте 5% от нашей комиссии от всех обменов, совершенных ими.\r\n\r\nПриглашенные пользователи фиксируются за Вами бессрочно!\r\n\r\nПриглашено пользователей:\r\nБонусный баланс: 0,00 ₽\r\nСсылка для приглашения:\r\nhttps://t.me/btc_exchanger_robot?start=934842562\'', 'exchange_bot', '5978700331:AAFjlGketecP-Oh1Q4QN3fdTAjIdki_oaBM', 'ADMIN ', '@andre', 'Обменник ExcheBTC успешно работает на рынке обмена криптовалют с 2019 года, неизменно предлагая лучший сервис, высокую скорость обработки обменов и низкие комиссии.\r\n\r\nВ нашей работе мы придерживаемся высоких стандартов, используем новейшее ПО и сводим человеческий фактор к минимуму, день за днём подтверждая свой статус лучшего Telegram-обменника BTC на рынке.\r\n\r\nОбмены осуществляются в автоматическом режиме круглосуточно и без выходных.\r\n\r\nСайт - https://coinexchange24-7.site/');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
