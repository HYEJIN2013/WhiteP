CREATE DATABASE IF NOT EXISTS session;
GRANT ALL PRIVILEGES ON session.* to 'assist'@'localhost' identified by 'assist';
USE session;
-- --------------------------------------------------------

--
-- Table structure for table `movies`
--

CREATE TABLE IF NOT EXISTS `movies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `movie` varchar(70) NOT NULL,
  `theater` varchar(50) NOT NULL,
  `zip` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=8 ;

--
-- Dumping data for table `movies`
--

INSERT INTO `movies` (`id`, `movie`, `theater`, `zip`) VALUES
(1, 'Valentine''s Day', 'Regal Fredericksburg 15', 22401),
(2, 'Dear John', 'Regal Fredericksburg 15', 22401),
(3, 'The Wolfman', 'Regal Fredericksburg 15', 22401),
(4, 'From Paris with Love', 'Marquee Cinemas Southpoint 9', 22401),
(5, 'The Book of Eli', 'Allen Cinema 4 Mesilla Valley', 88005),
(6, 'The Wolfman', 'Allen Cinema 4 Mesilla Valley', 88005),
(7, 'Avatar3D', 'Allen Cinema 4 Mesilla Valley', 88005);

-- --------------------------------------------------------

--
-- Table structure for table `stores`
--

CREATE TABLE IF NOT EXISTS `stores` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(25) NOT NULL,
  `type` varchar(25) NOT NULL,
  `address` varchar(30) NOT NULL,
  `city` varchar(25) NOT NULL,
  `zip` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=14 ;

--
-- Dumping data for table `stores`
--

INSERT INTO `stores` (`id`, `name`, `type`, `address`, `city`, `zip`) VALUES
(1, 'Starbucks', 'coffee', '2511 Lohman Ave', 'Las Cruces', 88005),
(2, 'Milagro Coffee Y Espresso', 'coffee', '1733 E. University Ave', 'Las Cruces', 88005),
(3, 'Starbucks', 'coffee', '1500 South Valley',  'Las Cruces', 88005),
(4, 'Bean', 'coffee', '2011 Avenida De Mesilla',  'Las Cruces', 88005),
(5, 'Hyperion Espresso', 'coffee', '301 William St.',  'Fredericksburg', 22401),
(6, 'Starbucks', 'coffee', '2001 Plank Road', 'Fredericksburg', 22401),
(7, 'Caribou Coffee', 'coffee', '1251 Carl D Silver Parkway', 'Fredericksburg',  22401),
(8, 'Pancho Villa Mexican Rest', 'Mexican restaurant', '10500 Spotsylvania Ave', 'Fredericksburg', 22401),
(9, 'Chipotle', 'Mexican restaurant', '5955 Kingstowne', 'Fredericksburg', 22401),
(10, 'El Comedor', 'Mexican restaurant', '2190 Avenida De  Mesilla', 'Las Cruces', 88005),
(11, 'Los Compas', 'Mexican restaurant', '603 S Nevarez St.',  'Las Cruces', 88005),
(12, 'La Fuente', 'Mexican restaurant', '1710 S Espina',  'Las Cruces', 88005),
(13, 'Peet''s', 'coffee', '2260 Locust',  'Las Cruces', 88005);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(12) NOT NULL,
  `password` varchar(256) NOT NULL,
  `zipcode` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `zipcode`) VALUES
(1, 'raz', '2d7a56995013d429316fae93b3b7b7bf5eaab6e2fabe1f32fe25549cb676d0c2', 88005),
(2, 'ann', '057ba03d6c44104863dc7361fe4578965d1887360f90a0895882e58a6248fc86', 22401),
(3, 'lazy', '65e84be33532fb784c48129675f9eff3a682b27168c0ea744b2cf58ee02337c5', 22401);
