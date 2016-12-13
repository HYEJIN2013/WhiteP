CREATE TABLE `t` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `target_id` int(11) NOT NULL,
  `status` int(11) NOT NULL DEFAULT '0',
  `executed_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_targetId` (`target_id`),
  KEY `idx_status_executedAt` (`status`,`executed_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
