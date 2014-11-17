/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50173
Source Host           : localhost:3306
Source Database       : weixin

Target Server Type    : MYSQL
Target Server Version : 50173
File Encoding         : 65001

Date: 2014-11-17 19:20:51
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for activeurl
-- ----------------------------
DROP TABLE IF EXISTS `activeurl`;
CREATE TABLE `activeurl` (
  `id` varchar(50) NOT NULL,
  `user_id` varchar(50) NOT NULL,
  `url` varchar(255) NOT NULL,
  `frequent` int(11) NOT NULL DEFAULT '30' COMMENT '频率 单位是分钟',
  `top_num` int(11) NOT NULL DEFAULT '1' COMMENT '阈值 新增内容超过这一值 将会发送',
  `send_mail_num` int(11) NOT NULL DEFAULT '0' COMMENT '总共发送的邮件次数',
  `total_record_num` int(11) NOT NULL DEFAULT '0' COMMENT '总共发送的记录数',
  `get_page_num` int(11) NOT NULL DEFAULT '0' COMMENT '抓取页面的次数',
  `parse_page_num` int(11) NOT NULL DEFAULT '0' COMMENT '解析页面的次数',
  `new_record_num` int(11) NOT NULL DEFAULT '0' COMMENT '距离上次发送邮件新增的记录数',
  `record_contents` text,
  `last_send_time` datetime DEFAULT NULL,
  `create_time` datetime NOT NULL,
  `summary` varchar(255) NOT NULL DEFAULT '' COMMENT '关于URL的描述',
  `status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '当前记录的状态 0 ：未激活  1 ： 激活  2：已删除',
  `fun_index` int(11) NOT NULL DEFAULT '0' COMMENT '使用函数的下标，0表示还没有检测出使用的函数',
  `reason` varchar(1024) DEFAULT '' COMMENT '当前记录失败的原因',
  `last_time` int(11) NOT NULL DEFAULT '0' COMMENT '默认是0，表示还没有计算出实际的last_time值',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of activeurl
-- ----------------------------

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT 'user id',
  `email` varchar(50) NOT NULL,
  `tel` varchar(50) NOT NULL,
  `create_time` datetime NOT NULL,
  `status` tinyint(4) NOT NULL COMMENT 'status of this email  0 cant send email  1 is ok',
  `admin` tinyint(4) NOT NULL DEFAULT '0' COMMENT '是否admin角色，默认不是',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES ('00141610981592244f846f3645c44c6a7de3f33c391f09a000', 'admin@admin.com', '11111111111', '2014-11-16 11:50:15', '0', '0');
