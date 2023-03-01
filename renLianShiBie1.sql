/*
 Navicat Premium Data Transfer

 Source Server         : root
 Source Server Type    : MySQL
 Source Server Version : 50739 (5.7.39-log)
 Source Host           : 127.0.0.1:3306
 Source Schema         : renLianShiBie1

 Target Server Type    : MySQL
 Target Server Version : 50739 (5.7.39-log)
 File Encoding         : 65001

 Date: 15/01/2023 11:10:24
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for app1_admin
-- ----------------------------
DROP TABLE IF EXISTS `app1_admin`;
CREATE TABLE `app1_admin`  (
  `adminNo` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `username` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`adminNo`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of app1_admin
-- ----------------------------
INSERT INTO `app1_admin` VALUES ('30000000', 'admin', '123456');

-- ----------------------------
-- Table structure for app1_admin_purview
-- ----------------------------
DROP TABLE IF EXISTS `app1_admin_purview`;
CREATE TABLE `app1_admin_purview`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `adminNo` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `previewId` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of app1_admin_purview
-- ----------------------------

-- ----------------------------
-- Table structure for app1_adminpurview
-- ----------------------------
DROP TABLE IF EXISTS `app1_adminpurview`;
CREATE TABLE `app1_adminpurview`  (
  `previewId` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`previewId`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of app1_adminpurview
-- ----------------------------

-- ----------------------------
-- Table structure for app1_authority
-- ----------------------------
DROP TABLE IF EXISTS `app1_authority`;
CREATE TABLE `app1_authority`  (
  `authNo` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`authNo`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of app1_authority
-- ----------------------------
INSERT INTO `app1_authority` VALUES ('1', '用户管理adm');
INSERT INTO `app1_authority` VALUES ('2', '课程管理tea');
INSERT INTO `app1_authority` VALUES ('3', '删除学生tea');
INSERT INTO `app1_authority` VALUES ('4', '增加学生tea');
INSERT INTO `app1_authority` VALUES ('5', '发布签到tea');
INSERT INTO `app1_authority` VALUES ('6', '把学生加入签到表tea');
INSERT INTO `app1_authority` VALUES ('7', '增选课程stu');

-- ----------------------------
-- Table structure for app1_class
-- ----------------------------
DROP TABLE IF EXISTS `app1_class`;
CREATE TABLE `app1_class`  (
  `classNo` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `course_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `teacher_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`classNo`) USING BTREE,
  INDEX `app1_class_course_id_7a2002c2_fk_app1_course_courseNo`(`course_id`) USING BTREE,
  INDEX `app1_class_teacher_id_2bdb19db_fk_app1_teacher_teacherNo`(`teacher_id`) USING BTREE,
  CONSTRAINT `app1_class_course_id_7a2002c2_fk_app1_course_courseNo` FOREIGN KEY (`course_id`) REFERENCES `app1_course` (`courseNo`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `app1_class_teacher_id_2bdb19db_fk_app1_teacher_teacherNo` FOREIGN KEY (`teacher_id`) REFERENCES `app1_teacher` (`teacherNo`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of app1_class
-- ----------------------------
INSERT INTO `app1_class` VALUES ('1', '100', '10000000');
INSERT INTO `app1_class` VALUES ('2', '101', '10000000');

-- ----------------------------
-- Table structure for app1_class_students
-- ----------------------------
DROP TABLE IF EXISTS `app1_class_students`;
CREATE TABLE `app1_class_students`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `class_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `student_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `app1_class_students_class_id_student_id_77377436_uniq`(`class_id`, `student_id`) USING BTREE,
  INDEX `app1_class_students_student_id_3d0878b1_fk_app1_stud`(`student_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 59 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of app1_class_students
-- ----------------------------
INSERT INTO `app1_class_students` VALUES (58, '1', '1');
INSERT INTO `app1_class_students` VALUES (42, '1', '20000000');
INSERT INTO `app1_class_students` VALUES (46, '1', '20000003');
INSERT INTO `app1_class_students` VALUES (47, '1', '20004567');
INSERT INTO `app1_class_students` VALUES (54, '2', '1');
INSERT INTO `app1_class_students` VALUES (43, '2', '20000000');
INSERT INTO `app1_class_students` VALUES (57, '2', '20000004');

-- ----------------------------
-- Table structure for app1_course
-- ----------------------------
DROP TABLE IF EXISTS `app1_course`;
CREATE TABLE `app1_course`  (
  `courseNo` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `courseName` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `grade` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`courseNo`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of app1_course
-- ----------------------------
INSERT INTO `app1_course` VALUES ('100', '软件文档写作', '3');
INSERT INTO `app1_course` VALUES ('101', '高等数学', '1');
INSERT INTO `app1_course` VALUES ('1234', '234', '234');
INSERT INTO `app1_course` VALUES ('12五456', '12', '12');

-- ----------------------------
-- Table structure for app1_qiandao
-- ----------------------------
DROP TABLE IF EXISTS `app1_qiandao`;
CREATE TABLE `app1_qiandao`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `qianDaoName` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `courseName` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `class1_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `pubtime` datetime(6) NOT NULL,
  `duetime` datetime(6) NOT NULL,
  `teacherNo_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `app1_qiandao_class1_id_af11cb86_fk_app1_class_classNo`(`class1_id`) USING BTREE,
  INDEX `app1_qiandao_teacherNo_id_4d9a6a92_fk_app1_teacher_teacherNo`(`teacherNo_id`) USING BTREE,
  CONSTRAINT `app1_qiandao_teacherNo_id_4d9a6a92_fk_app1_teacher_teacherNo` FOREIGN KEY (`teacherNo_id`) REFERENCES `app1_teacher` (`teacherNo`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 90 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of app1_qiandao
-- ----------------------------
INSERT INTO `app1_qiandao` VALUES (41, '软件文档写作Jan. 11, 2023, 5:13 p.m.', '软件文档写作', '1', '2023-01-11 17:13:31.252240', '2023-01-11 17:18:31.251412', '10000000');
INSERT INTO `app1_qiandao` VALUES (42, '软件文档写作Jan. 11, 2023, 5:16 p.m.', '软件文档写作', '1', '2023-01-11 17:16:35.978114', '2023-01-11 17:21:35.978114', '10000000');
INSERT INTO `app1_qiandao` VALUES (43, '软件文档写作Jan. 11, 2023, 5:18 p.m.', '软件文档写作', '1', '2023-01-11 17:18:47.550559', '2023-01-11 17:23:47.549642', '10000000');
INSERT INTO `app1_qiandao` VALUES (44, '软件文档写作Jan. 11, 2023, 5:23 p.m.', '软件文档写作', '1', '2023-01-11 17:23:54.228444', '2023-01-11 17:28:54.228444', '10000000');
INSERT INTO `app1_qiandao` VALUES (45, '软件文档写作Jan. 11, 2023, 5:27 p.m.', '软件文档写作', '1', '2023-01-11 17:27:02.582285', '2023-01-11 17:32:02.581656', '10000000');
INSERT INTO `app1_qiandao` VALUES (46, '软件文档写作Jan. 11, 2023, 5:33 p.m.', '软件文档写作', '1', '2023-01-11 17:33:23.204709', '2023-01-11 17:38:23.203709', '10000000');
INSERT INTO `app1_qiandao` VALUES (47, '软件文档写作Jan. 11, 2023, 5:55 p.m.', '软件文档写作', '1', '2023-01-11 17:55:22.497653', '2023-01-11 18:57:19.133143', '10000000');
INSERT INTO `app1_qiandao` VALUES (48, '软件文档写作Jan. 12, 2023, 3:44 p.m.', '软件文档写作', '1', '2023-01-12 15:44:23.053699', '2023-01-12 15:47:50.176086', '10000000');
INSERT INTO `app1_qiandao` VALUES (49, '软件文档写作Jan. 12, 2023, 3:55 p.m.', '软件文档写作', '1', '2023-01-12 15:55:16.333353', '2023-01-12 16:05:16.333353', '10000000');
INSERT INTO `app1_qiandao` VALUES (54, '软件文档写作Jan. 12, 2023, 4 p.m.', '软件文档写作', '1', '2023-01-12 16:01:01.324586', '2023-01-12 16:06:01.322847', '10000000');
INSERT INTO `app1_qiandao` VALUES (55, '软件文档写作Jan. 12, 2023, 4:18 p.m.', '软件文档写作', '1', '2023-01-12 16:18:32.216583', '2023-01-12 16:21:26.612093', '10000000');
INSERT INTO `app1_qiandao` VALUES (56, '软件文档写作Jan. 12, 2023, 4:21 p.m.', '软件文档写作', '1', '2023-01-12 16:21:38.573457', '2023-01-12 16:26:09.922073', '10000000');
INSERT INTO `app1_qiandao` VALUES (57, '软件文档写作Jan. 12, 2023, 4:26 p.m.', '软件文档写作', '1', '2023-01-12 16:26:22.225650', '2023-01-12 16:39:04.957294', '10000000');
INSERT INTO `app1_qiandao` VALUES (58, '软件文档写作Jan. 12, 2023, 4:39 p.m.', '软件文档写作', '1', '2023-01-12 16:39:13.309562', '2023-01-12 16:53:21.764178', '10000000');
INSERT INTO `app1_qiandao` VALUES (59, '软件文档写作Jan. 12, 2023, 4:53 p.m.', '软件文档写作', '1', '2023-01-12 16:53:29.486539', '2023-01-12 17:03:29.485541', '10000000');
INSERT INTO `app1_qiandao` VALUES (60, '软件文档写作Jan. 12, 2023, 5:06 p.m.', '软件文档写作', '1', '2023-01-12 17:06:25.723074', '2023-01-12 17:16:25.723074', '10000000');
INSERT INTO `app1_qiandao` VALUES (61, '软件文档写作Jan. 12, 2023, 5:59 p.m.', '软件文档写作', '1', '2023-01-12 17:59:23.478315', '2023-01-12 19:12:02.857610', '10000000');
INSERT INTO `app1_qiandao` VALUES (62, '软件文档写作Jan. 12, 2023, 7:12 p.m.', '软件文档写作', '1', '2023-01-12 19:12:11.116192', '2023-01-12 20:12:11.115706', '10000000');
INSERT INTO `app1_qiandao` VALUES (63, '软件文档写作Jan. 12, 2023, 8:21 p.m.', '软件文档写作', '1', '2023-01-12 20:21:29.838902', '2023-01-12 21:21:29.838902', '10000000');
INSERT INTO `app1_qiandao` VALUES (64, '软件文档写作Jan. 12, 2023, 9:46 p.m.', '软件文档写作', '1', '2023-01-12 21:46:33.702232', '2023-01-12 22:46:33.701269', '10000000');
INSERT INTO `app1_qiandao` VALUES (65, '软件文档写作Jan. 13, 2023, 9:23 a.m.', '软件文档写作', '1', '2023-01-13 09:23:14.368605', '2023-01-13 10:23:14.367606', '10000000');
INSERT INTO `app1_qiandao` VALUES (66, '软件文档写作Jan. 13, 2023, 11:27 a.m.', '软件文档写作', '1', '2023-01-13 11:27:59.571012', '2023-01-13 12:27:59.570021', '10000000');
INSERT INTO `app1_qiandao` VALUES (67, '软件文档写作Jan. 13, 2023, 11:29 a.m.', '软件文档写作', '1', '2023-01-13 11:29:20.031397', '2023-01-13 11:34:20.030405', '10000000');
INSERT INTO `app1_qiandao` VALUES (68, '高等数学Jan. 13, 2023, 1:21 p.m.', '高等数学', '2', '2023-01-13 13:21:07.283618', '2023-01-13 13:22:17.313298', '10000000');
INSERT INTO `app1_qiandao` VALUES (69, '软件文档写作Jan. 13, 2023, 5 p.m.', '软件文档写作', '1', '2023-01-13 17:00:28.917205', '2023-01-13 18:00:28.915206', '10000000');
INSERT INTO `app1_qiandao` VALUES (70, '软件文档写作Jan. 13, 2023, 5:24 p.m.', '软件文档写作', '1', '2023-01-13 17:24:35.115414', '2023-01-13 17:34:35.113406', '10000000');
INSERT INTO `app1_qiandao` VALUES (71, '软件文档写作Jan. 13, 2023, 5:24 p.m.', '软件文档写作', '1', '2023-01-13 17:24:45.530055', '2023-01-13 17:34:45.529684', '10000000');
INSERT INTO `app1_qiandao` VALUES (72, '高等数学Jan. 13, 2023, 5:26 p.m.', '高等数学', '2', '2023-01-13 17:26:10.188702', '2023-01-13 18:26:10.187668', '10000000');
INSERT INTO `app1_qiandao` VALUES (73, '软件文档写作Jan. 13, 2023, 6:30 p.m.', '软件文档写作', '1', '2023-01-13 18:30:15.922389', '2023-01-13 19:30:15.920397', '10000000');
INSERT INTO `app1_qiandao` VALUES (74, '软件文档写作Jan. 13, 2023, 6:30 p.m.', '软件文档写作', '1', '2023-01-13 18:30:23.614693', '2023-01-13 19:30:23.613315', '10000000');
INSERT INTO `app1_qiandao` VALUES (75, '高等数学Jan. 13, 2023, 6:30 p.m.', '高等数学', '2', '2023-01-13 18:30:31.225086', '2023-01-13 18:35:31.223066', '10000000');
INSERT INTO `app1_qiandao` VALUES (76, '软件文档写作Jan. 13, 2023, 6:56 p.m.', '软件文档写作', '1', '2023-01-13 18:57:00.860724', '2023-01-13 19:02:00.860724', '10000000');
INSERT INTO `app1_qiandao` VALUES (77, '软件文档写作Jan. 13, 2023, 6:56 p.m.', '软件文档写作', '1', '2023-01-13 18:59:07.574912', '2023-01-13 19:04:07.574912', '10000000');
INSERT INTO `app1_qiandao` VALUES (78, '软件文档写作Jan. 13, 2023, 7:08 p.m.', '软件文档写作', '1', '2023-01-13 19:08:31.450398', '2023-01-13 19:13:31.450398', '10000000');
INSERT INTO `app1_qiandao` VALUES (79, '软件文档写作Jan. 13, 2023, 7:13 p.m.', '软件文档写作', '1', '2023-01-13 19:13:57.154686', '2023-01-13 19:18:57.153671', '10000000');
INSERT INTO `app1_qiandao` VALUES (80, '软件文档写作Jan. 13, 2023, 7:26 p.m.', '软件文档写作', '1', '2023-01-13 19:26:07.458355', '2023-01-13 19:31:07.458355', '10000000');
INSERT INTO `app1_qiandao` VALUES (81, '软件文档写作Jan. 14, 2023, 10:06 a.m.', '软件文档写作', '1', '2023-01-14 10:07:02.876509', '2023-01-14 10:12:02.874104', '10000000');
INSERT INTO `app1_qiandao` VALUES (82, '软件文档写作Jan. 14, 2023, 10:16 a.m.', '软件文档写作', '1', '2023-01-14 10:16:10.618858', '2023-01-14 10:26:10.616446', '10000000');
INSERT INTO `app1_qiandao` VALUES (83, '软件文档写作Jan. 14, 2023, 10:30 a.m.', '软件文档写作', '1', '2023-01-14 10:30:45.354129', '2023-01-14 10:35:45.352760', '10000000');
INSERT INTO `app1_qiandao` VALUES (84, '软件文档写作Jan. 14, 2023, 10:57 a.m.', '软件文档写作', '1', '2023-01-14 10:57:04.218479', '2023-01-14 11:57:04.216471', '10000000');
INSERT INTO `app1_qiandao` VALUES (85, '软件文档写作Jan. 14, 2023, 7:04 p.m.', '软件文档写作', '1', '2023-01-14 19:04:58.251114', '2023-01-14 19:09:58.251114', '10000000');
INSERT INTO `app1_qiandao` VALUES (86, '软件文档写作Jan. 15, 2023, 8:56 a.m.', '软件文档写作', '1', '2023-01-15 08:56:43.661896', '2023-01-15 09:26:43.657926', '10000000');
INSERT INTO `app1_qiandao` VALUES (87, '软件文档写作Jan. 15, 2023, 9:27 a.m.', '软件文档写作', '1', '2023-01-15 09:28:11.939187', '2023-01-15 09:58:11.937190', '10000000');
INSERT INTO `app1_qiandao` VALUES (88, '高等数学Jan. 15, 2023, 9:31 a.m.', '高等数学', '2', '2023-01-15 09:31:37.375963', '2023-01-15 10:01:37.373986', '10000000');
INSERT INTO `app1_qiandao` VALUES (89, '软件文档写作Jan. 15, 2023, 10:06 a.m.', '软件文档写作', '1', '2023-01-15 10:06:52.412826', '2023-01-15 10:16:52.411829', '10000000');

-- ----------------------------
-- Table structure for app1_qiandaomessage
-- ----------------------------
DROP TABLE IF EXISTS `app1_qiandaomessage`;
CREATE TABLE `app1_qiandaomessage`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` time(6) NOT NULL,
  `student_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `app1_qiandaomessage_student_id_87c2f7b6_fk_app1_stud`(`student_id`) USING BTREE,
  CONSTRAINT `app1_qiandaomessage_student_id_87c2f7b6_fk_app1_stud` FOREIGN KEY (`student_id`) REFERENCES `app1_student` (`studentNo`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of app1_qiandaomessage
-- ----------------------------

-- ----------------------------
-- Table structure for app1_stu_auth
-- ----------------------------
DROP TABLE IF EXISTS `app1_stu_auth`;
CREATE TABLE `app1_stu_auth`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `authNo` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `studentNo` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `authName` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `1`(`authNo`) USING BTREE,
  INDEX `2`(`studentNo`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 18 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of app1_stu_auth
-- ----------------------------
INSERT INTO `app1_stu_auth` VALUES (8, '6', '1', '把学生加入签到表tea');
INSERT INTO `app1_stu_auth` VALUES (9, '7', '1', '增选课程stu');
INSERT INTO `app1_stu_auth` VALUES (10, '2', '123', '课程管理tea');
INSERT INTO `app1_stu_auth` VALUES (11, '1', '1', '用户管理adm');
INSERT INTO `app1_stu_auth` VALUES (13, '7', '1234', '增选课程stu');
INSERT INTO `app1_stu_auth` VALUES (14, '7', '12', '增选课程stu');
INSERT INTO `app1_stu_auth` VALUES (16, '6', '12', '把学生加入签到表tea');
INSERT INTO `app1_stu_auth` VALUES (17, '7', '20000000', '增选课程stu');

-- ----------------------------
-- Table structure for app1_stu_purview
-- ----------------------------
DROP TABLE IF EXISTS `app1_stu_purview`;
CREATE TABLE `app1_stu_purview`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `studentNo` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `previewId` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of app1_stu_purview
-- ----------------------------

-- ----------------------------
-- Table structure for app1_student
-- ----------------------------
DROP TABLE IF EXISTS `app1_student`;
CREATE TABLE `app1_student`  (
  `name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `studentNo` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `photo` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `img_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`studentNo`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of app1_student
-- ----------------------------
INSERT INTO `app1_student` VALUES ('1', '1', 'photos/1640142685693_snoAU7t.jpg', '1', '1640142685693.jpg');
INSERT INTO `app1_student` VALUES ('12', '12', 'photos/1640142685693_GU9GTya.jpg', '12', '1640142685693.jpg');
INSERT INTO `app1_student` VALUES ('123', '123', 'photos/1640142685693_qcH9kHC.jpg', '123', '1640142685693.jpg');
INSERT INTO `app1_student` VALUES ('1234', '1234', 'photos/1640142685693_cvZ3Dsd.jpg', '12345', '1640142685693.jpg');
INSERT INTO `app1_student` VALUES ('2345678', '1234567五456789', 'photos/1650004059073_IqEpy9j.jpg', '234567', '1650004059073.jpg');
INSERT INTO `app1_student` VALUES ('权泽睿', '200', 'photos/IMG_20211221_222940.jpg', '123456', 'IMG_20211221_222940.jpg');
INSERT INTO `app1_student` VALUES ('小敏', '20000000', 'IMG_20211221_222940.jpg', '123456', 'IMG_20211221_222940.jpg');
INSERT INTO `app1_student` VALUES ('小明', '20000001', '03915e0d37rbmKn.jpg', '123456', '03915e0d37rbmKn.jpg');
INSERT INTO `app1_student` VALUES ('小红', '20000002', 'photos/faf2b2119313b07eef0f5ddd05d7912396dd8cb0_lCYIr8J.jfif', '123456', 'faf2b2119313b07eef0f5ddd05d7912396dd8cb0.jfif');
INSERT INTO `app1_student` VALUES ('小刚', '20000003', 'photos/faf2b2119313b07eef0f5ddd05d7912396dd8cb0_yVWIfII.jfif', '123456', 'faf2b2119313b07eef0f5ddd05d7912396dd8cb0.jfif');
INSERT INTO `app1_student` VALUES ('小王', '20000004', 'photos/96c42d1cecca5601c4c969fa6a139c16.jpg', '123456', '96c42d1cecca5601c4c969fa6a139c16.jpg');
INSERT INTO `app1_student` VALUES ('权泽睿', '200001', 'photos/IMG_20211221_222940.jpg', '123456', 'IMG_20211221_222940.jpg');
INSERT INTO `app1_student` VALUES ('张三', '20002222', 'photos/ycy.jpg', '123456', 'ycy.jpg');
INSERT INTO `app1_student` VALUES ('李四', '20004567', 'photos/ycy.jpg', '123456', 'ycy.jpg');
INSERT INTO `app1_student` VALUES ('张三', '20009876', 'photos/ycy_J0n1LpB.jpg', '123456', 'ycy.jpg');
INSERT INTO `app1_student` VALUES ('2345', '234234567890', 'photos/1640142685693_sGnjpAz.jpg', '3456', '1640142685693.jpg');

-- ----------------------------
-- Table structure for app1_studentphoto
-- ----------------------------
DROP TABLE IF EXISTS `app1_studentphoto`;
CREATE TABLE `app1_studentphoto`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `photo` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of app1_studentphoto
-- ----------------------------
INSERT INTO `app1_studentphoto` VALUES (1, 'photos/1650004059073_JMza7nm.jpg');
INSERT INTO `app1_studentphoto` VALUES (2, 'photos/1640142685693.jpg');
INSERT INTO `app1_studentphoto` VALUES (3, 'photos/1650004059073.jpg');
INSERT INTO `app1_studentphoto` VALUES (4, 'photos/28798d4251afe27cab44324f496a5f83.jpg');
INSERT INTO `app1_studentphoto` VALUES (5, 'photos/1640142685693_VPAO0I2.jpg');
INSERT INTO `app1_studentphoto` VALUES (6, 'photos/03915e0d37rbmKn_5Oh3SIH.jpg');
INSERT INTO `app1_studentphoto` VALUES (7, 'photos/IMG_20211221_222940.jpg');

-- ----------------------------
-- Table structure for app1_studentpurview
-- ----------------------------
DROP TABLE IF EXISTS `app1_studentpurview`;
CREATE TABLE `app1_studentpurview`  (
  `previewId` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`previewId`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of app1_studentpurview
-- ----------------------------

-- ----------------------------
-- Table structure for app1_stuqiandao
-- ----------------------------
DROP TABLE IF EXISTS `app1_stuqiandao`;
CREATE TABLE `app1_stuqiandao`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `QianDaoId_id` int(11) NOT NULL,
  `studentNo_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `QTime` datetime(6) NULL DEFAULT NULL,
  `status` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `app1_stuqiandao_studentNo_id_15af6843_fk_app1_student_studentNo`(`studentNo_id`) USING BTREE,
  INDEX `app1_stuqiandao_QianDaoId_id_d524e336_fk`(`QianDaoId_id`) USING BTREE,
  CONSTRAINT `app1_stuqiandao_QianDaoId_id_d524e336_fk` FOREIGN KEY (`QianDaoId_id`) REFERENCES `app1_qiandao` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `app1_stuqiandao_studentNo_id_15af6843_fk_app1_student_studentNo` FOREIGN KEY (`studentNo_id`) REFERENCES `app1_student` (`studentNo`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 109 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of app1_stuqiandao
-- ----------------------------
INSERT INTO `app1_stuqiandao` VALUES (7, 41, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (8, 42, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (9, 43, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (10, 44, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (11, 45, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (12, 46, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (13, 47, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (14, 48, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (15, 54, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (16, 55, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (17, 56, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (18, 57, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (19, 58, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (20, 59, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (21, 60, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (22, 61, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (23, 62, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (24, 63, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (25, 64, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (26, 65, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (27, 65, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (28, 66, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (29, 67, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (30, 68, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (31, 69, '200001', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (34, 69, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (35, 69, '20004567', '2023-01-13 17:41:56.000000', '已签到');
INSERT INTO `app1_stuqiandao` VALUES (38, 75, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (39, 75, '200', '2023-01-14 10:56:21.917548', '已签到');
INSERT INTO `app1_stuqiandao` VALUES (42, 78, '200', '2023-01-14 10:56:21.917548', '已签到');
INSERT INTO `app1_stuqiandao` VALUES (43, 78, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (44, 78, '20000001', '2023-01-13 19:22:09.566074', '已签到');
INSERT INTO `app1_stuqiandao` VALUES (45, 78, '20000002', '2023-01-13 19:21:59.725324', '已签到');
INSERT INTO `app1_stuqiandao` VALUES (46, 78, '20000003', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (47, 78, '20004567', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (48, 79, '200', '2023-01-14 10:56:21.917548', '已签到');
INSERT INTO `app1_stuqiandao` VALUES (49, 79, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (50, 79, '20000001', '2023-01-13 19:22:09.566074', '已签到');
INSERT INTO `app1_stuqiandao` VALUES (51, 79, '20000002', '2023-01-13 19:21:59.725324', '已签到');
INSERT INTO `app1_stuqiandao` VALUES (52, 79, '20000003', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (53, 79, '20004567', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (54, 80, '200', '2023-01-14 10:56:21.917548', '已签到');
INSERT INTO `app1_stuqiandao` VALUES (55, 80, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (56, 80, '20000001', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (57, 80, '20000002', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (58, 80, '20000003', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (59, 80, '20004567', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (60, 81, '200', '2023-01-14 10:56:21.917548', '已签到');
INSERT INTO `app1_stuqiandao` VALUES (61, 81, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (62, 81, '20000001', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (63, 81, '20000002', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (64, 81, '20000003', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (65, 81, '20004567', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (66, 82, '200', '2023-01-14 10:56:21.917548', '已签到');
INSERT INTO `app1_stuqiandao` VALUES (67, 82, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (68, 82, '20000001', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (69, 82, '20000002', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (70, 82, '20000003', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (71, 82, '20004567', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (72, 83, '200', '2023-01-14 10:56:21.917548', '已签到');
INSERT INTO `app1_stuqiandao` VALUES (73, 83, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (74, 83, '20000001', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (75, 83, '20000002', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (76, 83, '20000003', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (77, 83, '20004567', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (78, 84, '200', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (79, 84, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (80, 84, '20000001', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (81, 84, '20000002', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (82, 84, '20000003', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (83, 84, '20004567', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (84, 85, '200', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (85, 85, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (86, 85, '20000001', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (87, 85, '20000002', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (88, 85, '20000003', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (89, 85, '20004567', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (90, 85, '20000000', '2023-01-14 19:05:21.000000', '已签到');
INSERT INTO `app1_stuqiandao` VALUES (91, 86, '1', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (92, 86, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (93, 86, '20000002', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (94, 86, '20000003', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (95, 86, '20004567', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (96, 87, '1', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (97, 87, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (98, 87, '20000002', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (99, 87, '20000003', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (100, 87, '20004567', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (101, 88, '1', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (102, 88, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (103, 88, '20000004', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (104, 89, '1', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (105, 89, '20000000', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (106, 89, '20000003', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (107, 89, '20004567', NULL, '未签到');
INSERT INTO `app1_stuqiandao` VALUES (108, 89, '20000000', '2023-01-15 10:07:09.000000', '已签到');

-- ----------------------------
-- Table structure for app1_tea_auth
-- ----------------------------
DROP TABLE IF EXISTS `app1_tea_auth`;
CREATE TABLE `app1_tea_auth`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `authNo` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `teacherNo` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `authName` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `authNo_id`(`authNo`) USING BTREE,
  INDEX `teacherNo_id`(`teacherNo`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of app1_tea_auth
-- ----------------------------
INSERT INTO `app1_tea_auth` VALUES (1, '1', '10000000', '23');
INSERT INTO `app1_tea_auth` VALUES (2, '2', '10000000', '课程管理tea');
INSERT INTO `app1_tea_auth` VALUES (4, '4', '10000000', '增加学生tea');
INSERT INTO `app1_tea_auth` VALUES (6, '5', '10000000', '发布签到tea');
INSERT INTO `app1_tea_auth` VALUES (7, '6', '10000000', '把学生加入签到表tea');
INSERT INTO `app1_tea_auth` VALUES (8, '3', '10000000', '删除学生tea');

-- ----------------------------
-- Table structure for app1_tea_purview
-- ----------------------------
DROP TABLE IF EXISTS `app1_tea_purview`;
CREATE TABLE `app1_tea_purview`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `teacherNo` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `previewId` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of app1_tea_purview
-- ----------------------------

-- ----------------------------
-- Table structure for app1_teacher
-- ----------------------------
DROP TABLE IF EXISTS `app1_teacher`;
CREATE TABLE `app1_teacher`  (
  `user` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `teacherNo` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`teacherNo`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of app1_teacher
-- ----------------------------
INSERT INTO `app1_teacher` VALUES ('123', '李强', '10000000', '123456');
INSERT INTO `app1_teacher` VALUES ('30000000', '2345', '234523456789', '123456');

-- ----------------------------
-- Table structure for app1_teacherrights
-- ----------------------------
DROP TABLE IF EXISTS `app1_teacherrights`;
CREATE TABLE `app1_teacherrights`  (
  `previewId` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`previewId`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of app1_teacherrights
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id`, `permission_id`) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id`, `codename`) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 97 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` VALUES (13, 'Can add user', 4, 'add_user');
INSERT INTO `auth_permission` VALUES (14, 'Can change user', 4, 'change_user');
INSERT INTO `auth_permission` VALUES (15, 'Can delete user', 4, 'delete_user');
INSERT INTO `auth_permission` VALUES (16, 'Can view user', 4, 'view_user');
INSERT INTO `auth_permission` VALUES (17, 'Can add content type', 5, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (18, 'Can change content type', 5, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (19, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (20, 'Can view content type', 5, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (21, 'Can add session', 6, 'add_session');
INSERT INTO `auth_permission` VALUES (22, 'Can change session', 6, 'change_session');
INSERT INTO `auth_permission` VALUES (23, 'Can delete session', 6, 'delete_session');
INSERT INTO `auth_permission` VALUES (24, 'Can view session', 6, 'view_session');
INSERT INTO `auth_permission` VALUES (25, 'Can add class', 7, 'add_class');
INSERT INTO `auth_permission` VALUES (26, 'Can change class', 7, 'change_class');
INSERT INTO `auth_permission` VALUES (27, 'Can delete class', 7, 'delete_class');
INSERT INTO `auth_permission` VALUES (28, 'Can view class', 7, 'view_class');
INSERT INTO `auth_permission` VALUES (29, 'Can add course', 8, 'add_course');
INSERT INTO `auth_permission` VALUES (30, 'Can change course', 8, 'change_course');
INSERT INTO `auth_permission` VALUES (31, 'Can delete course', 8, 'delete_course');
INSERT INTO `auth_permission` VALUES (32, 'Can view course', 8, 'view_course');
INSERT INTO `auth_permission` VALUES (33, 'Can add student', 9, 'add_student');
INSERT INTO `auth_permission` VALUES (34, 'Can change student', 9, 'change_student');
INSERT INTO `auth_permission` VALUES (35, 'Can delete student', 9, 'delete_student');
INSERT INTO `auth_permission` VALUES (36, 'Can view student', 9, 'view_student');
INSERT INTO `auth_permission` VALUES (37, 'Can add teacher', 10, 'add_teacher');
INSERT INTO `auth_permission` VALUES (38, 'Can change teacher', 10, 'change_teacher');
INSERT INTO `auth_permission` VALUES (39, 'Can delete teacher', 10, 'delete_teacher');
INSERT INTO `auth_permission` VALUES (40, 'Can view teacher', 10, 'view_teacher');
INSERT INTO `auth_permission` VALUES (41, 'Can add qian dao message', 11, 'add_qiandaomessage');
INSERT INTO `auth_permission` VALUES (42, 'Can change qian dao message', 11, 'change_qiandaomessage');
INSERT INTO `auth_permission` VALUES (43, 'Can delete qian dao message', 11, 'delete_qiandaomessage');
INSERT INTO `auth_permission` VALUES (44, 'Can view qian dao message', 11, 'view_qiandaomessage');
INSERT INTO `auth_permission` VALUES (45, 'Can add qian dao', 12, 'add_qiandao');
INSERT INTO `auth_permission` VALUES (46, 'Can change qian dao', 12, 'change_qiandao');
INSERT INTO `auth_permission` VALUES (47, 'Can delete qian dao', 12, 'delete_qiandao');
INSERT INTO `auth_permission` VALUES (48, 'Can view qian dao', 12, 'view_qiandao');
INSERT INTO `auth_permission` VALUES (49, 'Can add admin', 13, 'add_admin');
INSERT INTO `auth_permission` VALUES (50, 'Can change admin', 13, 'change_admin');
INSERT INTO `auth_permission` VALUES (51, 'Can delete admin', 13, 'delete_admin');
INSERT INTO `auth_permission` VALUES (52, 'Can view admin', 13, 'view_admin');
INSERT INTO `auth_permission` VALUES (53, 'Can add authority', 14, 'add_authority');
INSERT INTO `auth_permission` VALUES (54, 'Can change authority', 14, 'change_authority');
INSERT INTO `auth_permission` VALUES (55, 'Can delete authority', 14, 'delete_authority');
INSERT INTO `auth_permission` VALUES (56, 'Can view authority', 14, 'view_authority');
INSERT INTO `auth_permission` VALUES (57, 'Can add tea_ auth', 15, 'add_tea_auth');
INSERT INTO `auth_permission` VALUES (58, 'Can change tea_ auth', 15, 'change_tea_auth');
INSERT INTO `auth_permission` VALUES (59, 'Can delete tea_ auth', 15, 'delete_tea_auth');
INSERT INTO `auth_permission` VALUES (60, 'Can view tea_ auth', 15, 'view_tea_auth');
INSERT INTO `auth_permission` VALUES (61, 'Can add stu_ auth', 16, 'add_stu_auth');
INSERT INTO `auth_permission` VALUES (62, 'Can change stu_ auth', 16, 'change_stu_auth');
INSERT INTO `auth_permission` VALUES (63, 'Can delete stu_ auth', 16, 'delete_stu_auth');
INSERT INTO `auth_permission` VALUES (64, 'Can view stu_ auth', 16, 'view_stu_auth');
INSERT INTO `auth_permission` VALUES (65, 'Can add student photo', 17, 'add_studentphoto');
INSERT INTO `auth_permission` VALUES (66, 'Can change student photo', 17, 'change_studentphoto');
INSERT INTO `auth_permission` VALUES (67, 'Can delete student photo', 17, 'delete_studentphoto');
INSERT INTO `auth_permission` VALUES (68, 'Can view student photo', 17, 'view_studentphoto');
INSERT INTO `auth_permission` VALUES (69, 'Can add stu qian dao', 18, 'add_stuqiandao');
INSERT INTO `auth_permission` VALUES (70, 'Can change stu qian dao', 18, 'change_stuqiandao');
INSERT INTO `auth_permission` VALUES (71, 'Can delete stu qian dao', 18, 'delete_stuqiandao');
INSERT INTO `auth_permission` VALUES (72, 'Can view stu qian dao', 18, 'view_stuqiandao');
INSERT INTO `auth_permission` VALUES (73, 'Can add admin_purview', 19, 'add_admin_purview');
INSERT INTO `auth_permission` VALUES (74, 'Can change admin_purview', 19, 'change_admin_purview');
INSERT INTO `auth_permission` VALUES (75, 'Can delete admin_purview', 19, 'delete_admin_purview');
INSERT INTO `auth_permission` VALUES (76, 'Can view admin_purview', 19, 'view_admin_purview');
INSERT INTO `auth_permission` VALUES (77, 'Can add admin purview', 20, 'add_adminpurview');
INSERT INTO `auth_permission` VALUES (78, 'Can change admin purview', 20, 'change_adminpurview');
INSERT INTO `auth_permission` VALUES (79, 'Can delete admin purview', 20, 'delete_adminpurview');
INSERT INTO `auth_permission` VALUES (80, 'Can view admin purview', 20, 'view_adminpurview');
INSERT INTO `auth_permission` VALUES (81, 'Can add stu_purview', 21, 'add_stu_purview');
INSERT INTO `auth_permission` VALUES (82, 'Can change stu_purview', 21, 'change_stu_purview');
INSERT INTO `auth_permission` VALUES (83, 'Can delete stu_purview', 21, 'delete_stu_purview');
INSERT INTO `auth_permission` VALUES (84, 'Can view stu_purview', 21, 'view_stu_purview');
INSERT INTO `auth_permission` VALUES (85, 'Can add student purview', 22, 'add_studentpurview');
INSERT INTO `auth_permission` VALUES (86, 'Can change student purview', 22, 'change_studentpurview');
INSERT INTO `auth_permission` VALUES (87, 'Can delete student purview', 22, 'delete_studentpurview');
INSERT INTO `auth_permission` VALUES (88, 'Can view student purview', 22, 'view_studentpurview');
INSERT INTO `auth_permission` VALUES (89, 'Can add tea_purview', 23, 'add_tea_purview');
INSERT INTO `auth_permission` VALUES (90, 'Can change tea_purview', 23, 'change_tea_purview');
INSERT INTO `auth_permission` VALUES (91, 'Can delete tea_purview', 23, 'delete_tea_purview');
INSERT INTO `auth_permission` VALUES (92, 'Can view tea_purview', 23, 'view_tea_purview');
INSERT INTO `auth_permission` VALUES (93, 'Can add teacher rights', 24, 'add_teacherrights');
INSERT INTO `auth_permission` VALUES (94, 'Can change teacher rights', 24, 'change_teacherrights');
INSERT INTO `auth_permission` VALUES (95, 'Can delete teacher rights', 24, 'delete_teacherrights');
INSERT INTO `auth_permission` VALUES (96, 'Can view teacher rights', 24, 'view_teacherrights');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq`(`user_id`, `group_id`) USING BTREE,
  INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id`(`group_id`) USING BTREE,
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq`(`user_id`, `permission_id`) USING BTREE,
  INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int(11) NULL DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id`) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk_auth_user_id`(`user_id`) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label`, `model`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 25 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (13, 'app1', 'admin');
INSERT INTO `django_content_type` VALUES (20, 'app1', 'adminpurview');
INSERT INTO `django_content_type` VALUES (19, 'app1', 'admin_purview');
INSERT INTO `django_content_type` VALUES (14, 'app1', 'authority');
INSERT INTO `django_content_type` VALUES (7, 'app1', 'class');
INSERT INTO `django_content_type` VALUES (8, 'app1', 'course');
INSERT INTO `django_content_type` VALUES (12, 'app1', 'qiandao');
INSERT INTO `django_content_type` VALUES (11, 'app1', 'qiandaomessage');
INSERT INTO `django_content_type` VALUES (9, 'app1', 'student');
INSERT INTO `django_content_type` VALUES (17, 'app1', 'studentphoto');
INSERT INTO `django_content_type` VALUES (22, 'app1', 'studentpurview');
INSERT INTO `django_content_type` VALUES (18, 'app1', 'stuqiandao');
INSERT INTO `django_content_type` VALUES (16, 'app1', 'stu_auth');
INSERT INTO `django_content_type` VALUES (21, 'app1', 'stu_purview');
INSERT INTO `django_content_type` VALUES (10, 'app1', 'teacher');
INSERT INTO `django_content_type` VALUES (24, 'app1', 'teacherrights');
INSERT INTO `django_content_type` VALUES (15, 'app1', 'tea_auth');
INSERT INTO `django_content_type` VALUES (23, 'app1', 'tea_purview');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'auth', 'user');
INSERT INTO `django_content_type` VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (6, 'sessions', 'session');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 36 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2022-12-08 12:46:13.216802');
INSERT INTO `django_migrations` VALUES (2, 'auth', '0001_initial', '2022-12-08 12:46:15.177626');
INSERT INTO `django_migrations` VALUES (3, 'admin', '0001_initial', '2022-12-08 12:46:15.809074');
INSERT INTO `django_migrations` VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2022-12-08 12:46:15.847522');
INSERT INTO `django_migrations` VALUES (5, 'admin', '0003_logentry_add_action_flag_choices', '2022-12-08 12:46:15.883022');
INSERT INTO `django_migrations` VALUES (6, 'app1', '0001_initial', '2022-12-08 12:46:17.687671');
INSERT INTO `django_migrations` VALUES (7, 'contenttypes', '0002_remove_content_type_name', '2022-12-08 12:46:18.042332');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0002_alter_permission_name_max_length', '2022-12-08 12:46:18.236438');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0003_alter_user_email_max_length', '2022-12-08 12:46:18.641424');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0004_alter_user_username_opts', '2022-12-08 12:46:18.673446');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0005_alter_user_last_login_null', '2022-12-08 12:46:18.846468');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0006_require_contenttypes_0002', '2022-12-08 12:46:18.870128');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0007_alter_validators_add_error_messages', '2022-12-08 12:46:18.954147');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0008_alter_user_username_max_length', '2022-12-08 12:46:19.066221');
INSERT INTO `django_migrations` VALUES (15, 'auth', '0009_alter_user_last_name_max_length', '2022-12-08 12:46:19.257989');
INSERT INTO `django_migrations` VALUES (16, 'auth', '0010_alter_group_name_max_length', '2022-12-08 12:46:19.359940');
INSERT INTO `django_migrations` VALUES (17, 'auth', '0011_update_proxy_permissions', '2022-12-08 12:46:19.673592');
INSERT INTO `django_migrations` VALUES (18, 'auth', '0012_alter_user_first_name_max_length', '2022-12-08 12:46:19.838722');
INSERT INTO `django_migrations` VALUES (19, 'sessions', '0001_initial', '2022-12-08 12:46:20.255399');
INSERT INTO `django_migrations` VALUES (20, 'app1', '0002_auto_20230105_1336', '2023-01-05 05:37:12.027530');
INSERT INTO `django_migrations` VALUES (21, 'app1', '0003_student_password', '2023-01-05 05:44:32.734479');
INSERT INTO `django_migrations` VALUES (22, 'app1', '0004_alter_qiandao_id_alter_qiandaomessage_id_and_more', '2023-01-06 00:15:28.529450');
INSERT INTO `django_migrations` VALUES (23, 'app1', '0004_student_img_name_alter_qiandao_id_and_more', '2023-01-09 02:43:21.856833');
INSERT INTO `django_migrations` VALUES (24, 'app1', '0005_alter_student_img_name', '2023-01-09 02:48:24.771963');
INSERT INTO `django_migrations` VALUES (25, 'app1', '0006_studentphoto', '2023-01-09 03:21:27.192480');
INSERT INTO `django_migrations` VALUES (26, 'app1', '0007_auto_20230109_1330', '2023-01-09 05:31:45.718613');
INSERT INTO `django_migrations` VALUES (27, 'app1', '0007_auto_20230109_1417', '2023-01-09 06:21:16.735846');
INSERT INTO `django_migrations` VALUES (28, 'app1', '0008_auto_20230110_1111', '2023-01-10 11:11:47.421794');
INSERT INTO `django_migrations` VALUES (29, 'app1', '0009_qiandao_teacherno', '2023-01-10 12:10:57.394617');
INSERT INTO `django_migrations` VALUES (30, 'app1', '0010_merge_20230110_2153', '2023-01-10 21:53:07.022486');
INSERT INTO `django_migrations` VALUES (31, 'app1', '0011_admin_purview_adminpurview_stu_purview_and_more', '2023-01-10 21:53:53.319508');
INSERT INTO `django_migrations` VALUES (32, 'app1', '0010_qiandaomessage_status', '2023-01-11 15:50:38.216162');
INSERT INTO `django_migrations` VALUES (33, 'app1', '0011_auto_20230111_1551', '2023-01-11 15:52:00.162265');
INSERT INTO `django_migrations` VALUES (34, 'app1', '0012_auto_20230111_1654', '2023-01-11 16:54:08.122198');
INSERT INTO `django_migrations` VALUES (35, 'app1', '0013_auto_20230111_1659', '2023-01-11 16:59:35.981985');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO `django_session` VALUES ('dmgqx0ehk3rzofsraars6ia264z1bgue', 'eyJ1c2VybmFtZSI6ImFkbWluIiwiaXNfbG9naW4iOnRydWV9:1pDMYM:a8Y13Vh1wuHEahJcJNAztc1vsi-iDe_c3q8vra18sG4', '2023-01-06 09:28:50.293393');
INSERT INTO `django_session` VALUES ('fvs5nbfvo0ii08b4xb05zahn0rs6sn8a', 'eyJ1c2VybmFtZSI6ImFkbWluIiwiaXNfbG9naW4iOnRydWV9:1pDMX8:akqZL1YwAyKa9832ryg8zTzPsJWr8urLgVasWkWOl1Q', '2023-01-06 09:27:34.645811');
INSERT INTO `django_session` VALUES ('g9i4unhjlmkecjj9wc3errj1kiarp161', 'eyJ1c2VybmFtZSI6ImFkbWluIiwiaXNfbG9naW4iOnRydWV9:1pDMYu:CxzYeU3HBdpGiXv2ymS_8yOgu3e_RDrz3In93JvrGzw', '2023-01-06 09:29:24.292830');
INSERT INTO `django_session` VALUES ('iu0vu00s0zwn1j1opmjgi37ehy365m56', 'eyJ1c2VybmFtZSI6ImFkbWluIiwiaXNfbG9naW4iOnRydWV9:1pDMXf:3IlpF5BM-spEos-n52VEGOwOm3gRtUFsYQ0Og7wnMyA', '2023-01-06 09:28:07.516722');
INSERT INTO `django_session` VALUES ('jblanz7dn8t6ts44hklkzkfy5hd2zvyw', 'eyJ1c2VybmFtZSI6ImFkbWluIiwiaXNfbG9naW4iOnRydWV9:1pDMNZ:scHAmR2VRBkkJMituQcGAmEr-AsL69sVeNvOdiHJ0Hg', '2023-01-06 09:17:41.615735');
INSERT INTO `django_session` VALUES ('qnhawn5ea2973lm29nagr46azh693q1e', 'eyJ1c2VybmFtZSI6ImFkbWluIiwiaXNfbG9naW4iOnRydWV9:1pDMNE:YYI5mA57Q2kpFxfPzwGvpqb8eH_t6U7Aw9MZAK8ywsY', '2023-01-06 09:17:20.400642');
INSERT INTO `django_session` VALUES ('v0ij2sddsqh7pyuaukkxhnryzxz56k20', 'eyJ1c2VybmFtZSI6ImFkbWluIiwiaXNfbG9naW4iOnRydWV9:1pDMLe:WP20tzc1rl-NDNK7BZmlUIWQFdHuHjwVnhT52qA37Vo', '2023-01-19 09:15:42.066509');
INSERT INTO `django_session` VALUES ('xv967prhysybw2e8vuaunbjpyvt57daa', 'eyJ1c2VybmFtZSI6ImFkbWluIiwiaXNfbG9naW4iOnRydWV9:1pDMC1:H3zxQ-PvSyWjry5SUaFx-1rLfkynlhEmPk0bsiP9lPc', '2023-01-19 09:05:45.272295');

SET FOREIGN_KEY_CHECKS = 1;
