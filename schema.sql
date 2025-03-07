DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `token` varchar(255) NOT NULL,
  `leader_card_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token` (`token`)
);

DROP TABLE IF EXISTS `room`;
CREATE TABLE `room` (
  `room_id` bigint NOT NULL AUTO_INCREMENT,
  `live_id` bigint NOT NULL,
  `joined_user_count` int NOT NULL,
  `max_user_count` int NOT NULL,
  `status` int NOT NULL DEFAULT 1,
  PRIMARY KEY (`room_id`)
);

-- TODO: 外部キー制約を貼る
DROP TABLE IF EXISTS `room_member`;
CREATE TABLE `room_member` (
  `room_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `select_difficulty` int NOT NULL,
  `is_host` boolean NOT NULL,
  `judge_count_list` varchar(255),
  `score` int,
  PRIMARY KEY (`room_id`, `user_id`)
);
