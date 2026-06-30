-- 数据库初始化：建库+建表+视图+存储过程+触发器+初始数据
CREATE DATABASE IF NOT EXISTS house_rent DEFAULT CHARSET=utf8mb4;
USE house_rent;

-- 1. 角色表
DROP TABLE IF EXISTS sys_role;
CREATE TABLE sys_role(
    role_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '角色ID',
    role_name VARCHAR(20) NOT NULL UNIQUE COMMENT '角色名称：超级管理员/中介员工/只读员工',
    role_desc VARCHAR(100) COMMENT '角色描述'
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='角色表';
INSERT INTO sys_role(role_name,role_desc) VALUES
('超级管理员','全部权限，备份恢复、账号管理'),
('中介员工','房源、租客、租赁、收费操作'),
('只读员工','仅查询数据，无修改删除权限');

-- 2. 系统用户表
DROP TABLE IF EXISTS sys_user;
CREATE TABLE sys_user(
    user_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    username VARCHAR(30) NOT NULL UNIQUE COMMENT '登录账号',
    password VARCHAR(60) NOT NULL COMMENT '密码加密存储',
    real_name VARCHAR(20) NOT NULL COMMENT '员工姓名',
    phone VARCHAR(11) COMMENT '员工手机号',
    role_id INT NOT NULL COMMENT '关联角色',
    create_time DATETIME DEFAULT NOW(),
    FOREIGN KEY (role_id) REFERENCES sys_role(role_id) ON DELETE RESTRICT
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统员工用户表';
CREATE INDEX idx_user_role ON sys_user(role_id);
-- 初始管理员账号：admin/123456（密码：123456）
INSERT INTO sys_user(username,password,real_name,phone,role_id) VALUES
('admin','123456','系统管理员','13800138000',1);

-- 3. 户型表
DROP TABLE IF EXISTS house_type;
CREATE TABLE house_type(
    type_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '户型ID',
    type_name VARCHAR(30) NOT NULL UNIQUE COMMENT '户型名称：一室一厅/两室一厅',
    area_range VARCHAR(50) COMMENT '面积区间',
    remark VARCHAR(100) COMMENT '户型备注'
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='户型分类表';
INSERT INTO house_type(type_name,area_range) VALUES
('一室一厅','30-60㎡'),('两室一厅','60-90㎡'),('三室两厅','90-130㎡'),('四室及以上','130㎡+');

-- 4. 房东表
DROP TABLE IF EXISTS landlord;
CREATE TABLE landlord(
    land_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '房东ID',
    land_name VARCHAR(20) NOT NULL COMMENT '房东姓名',
    land_phone VARCHAR(11) NOT NULL UNIQUE COMMENT '房东电话',
    land_idcard VARCHAR(18) UNIQUE COMMENT '身份证号',
    land_address VARCHAR(200) COMMENT '房东常住地址',
    create_time DATETIME DEFAULT NOW()
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='房东信息表';
CREATE INDEX idx_land_phone ON landlord(land_phone);

-- 5. 房源表
DROP TABLE IF EXISTS house;
CREATE TABLE house(
    house_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '房屋唯一ID',
    house_no VARCHAR(50) NOT NULL UNIQUE COMMENT '房号（唯一标识）',
    type_id INT NOT NULL COMMENT '关联户型',
    land_id INT NOT NULL COMMENT '关联房东',
    address VARCHAR(200) NOT NULL COMMENT '房屋详细地址',
    area DECIMAL(5,1) NOT NULL COMMENT '建筑面积',
    rent_price DECIMAL(10,2) NOT NULL COMMENT '月租金',
    deposit DECIMAL(10,2) NOT NULL COMMENT '押金',
    house_status TINYINT DEFAULT 0 COMMENT '0空置 1已租 2维修 3下架',
    facilities TEXT COMMENT '配套设施',
    create_time DATETIME DEFAULT NOW(),
    FOREIGN KEY (type_id) REFERENCES house_type(type_id) ON DELETE RESTRICT,
    FOREIGN KEY (land_id) REFERENCES landlord(land_id) ON DELETE RESTRICT
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='房源信息表';
CREATE INDEX idx_house_type ON house(type_id);
CREATE INDEX idx_house_land ON house(land_id);
CREATE INDEX idx_house_status ON house(house_status);

-- 6. 租客表
DROP TABLE IF EXISTS customer;
CREATE TABLE customer(
    cust_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '租客ID',
    cust_name VARCHAR(20) NOT NULL COMMENT '租客姓名',
    cust_phone VARCHAR(11) NOT NULL UNIQUE COMMENT '租客手机号',
    cust_idcard VARCHAR(18) UNIQUE COMMENT '租客身份证',
    work_unit VARCHAR(100) COMMENT '工作单位',
    create_time DATETIME DEFAULT NOW()
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='租房客户表';
CREATE INDEX idx_cust_phone ON customer(cust_phone);

-- 7. 租赁合同表
DROP TABLE IF EXISTS rent_contract;
CREATE TABLE rent_contract(
    contract_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '合同编号',
    house_id INT NOT NULL COMMENT '租赁房屋',
    cust_id INT NOT NULL COMMENT '租赁客户',
    start_date DATE NOT NULL COMMENT '起租日期',
    end_date DATE NOT NULL COMMENT '到期日期',
    real_rent DECIMAL(10,2) NOT NULL COMMENT '实际月租',
    contract_status TINYINT DEFAULT 0 COMMENT '0租住中 1已退租',
    return_date DATE NULL COMMENT '归还退租日期',
    operator_id INT NOT NULL COMMENT '办理中介员工ID',
    create_time DATETIME DEFAULT NOW(),
    FOREIGN KEY (house_id) REFERENCES house(house_id) ON DELETE RESTRICT,
    FOREIGN KEY (cust_id) REFERENCES customer(cust_id) ON DELETE RESTRICT,
    FOREIGN KEY (operator_id) REFERENCES sys_user(user_id) ON DELETE RESTRICT
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='房屋租赁合同表';
CREATE INDEX idx_contract_house ON rent_contract(house_id);
CREATE INDEX idx_contract_cust ON rent_contract(cust_id);
CREATE INDEX idx_contract_status ON rent_contract(contract_status);

-- 8. 收费记录表
DROP TABLE IF EXISTS charge_record;
CREATE TABLE charge_record(
    charge_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '缴费ID',
    contract_id INT NOT NULL COMMENT '关联租赁合同',
    charge_type TINYINT NOT NULL COMMENT '1租金 2押金 3中介费',
    charge_money DECIMAL(10,2) NOT NULL COMMENT '缴费金额',
    charge_time DATETIME DEFAULT NOW() COMMENT '缴费时间',
    remark VARCHAR(200) COMMENT '备注',
    FOREIGN KEY (contract_id) REFERENCES rent_contract(contract_id) ON DELETE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='收费记录表';
CREATE INDEX idx_charge_contract ON charge_record(contract_id);

-- 9. 视图：查询房屋完整信息
DROP VIEW IF EXISTS v_house_all_info;
CREATE VIEW v_house_all_info AS
SELECT 
    h.house_no AS 房号,
    l.land_name AS 房东姓名,
    l.land_phone AS 房东电话,
    ht.type_name AS 户型,
    h.address AS 房屋地址,
    CASE h.house_status
        WHEN 0 THEN '空置可租'
        WHEN 1 THEN '已出租'
        WHEN 2 THEN '维修中'
        WHEN 3 THEN '已下架'
    END AS 房屋状态,
    h.rent_price AS 月租金
FROM house h
LEFT JOIN landlord l ON h.land_id = l.land_id
LEFT JOIN house_type ht ON h.type_id = ht.type_id
ORDER BY h.house_id DESC;

-- 10. 存储过程：统计各户型出租数量
DELIMITER //
DROP PROCEDURE IF EXISTS proc_stat_rent_by_type//
CREATE PROCEDURE proc_stat_rent_by_type()
BEGIN
    SELECT 
        ht.type_name AS 户型名称,
        COUNT(DISTINCT h.house_id) AS 总房源数,
        SUM(IF(h.house_status=1,1,0)) AS 已出租数量,
        SUM(IF(h.house_status=0,1,0)) AS 空置数量
    FROM house_type ht
    LEFT JOIN house h ON ht.type_id = h.type_id
    GROUP BY ht.type_id,ht.type_name
    ORDER BY 已出租数量 DESC;
END //
DELIMITER ;

-- 11. 触发器：出租时更新房屋状态为已租
DELIMITER //
DROP TRIGGER IF EXISTS tri_rent_update_house_status//
CREATE TRIGGER tri_rent_update_house_status
AFTER INSERT ON rent_contract
FOR EACH ROW
BEGIN
    IF NEW.contract_status = 0 THEN
        UPDATE house SET house_status=1 WHERE house_id = NEW.house_id;
        -- 自动新增3条收费记录：租金、押金、中介费
        INSERT INTO charge_record(contract_id,charge_type,charge_money,remark)
        VALUES
        (NEW.contract_id, 1, NEW.real_rent, '房屋租金'),
        (NEW.contract_id, 2, NEW.real_rent / 2, '租房押金'),
        (NEW.contract_id, 3, NEW.real_rent / 5, '中介费');
    END IF;
END //

-- 触发器：退租时更新房屋状态为空置
DROP TRIGGER IF EXISTS tri_return_update_house_status//
CREATE TRIGGER tri_return_update_house_status
AFTER UPDATE ON rent_contract
FOR EACH ROW
BEGIN
    IF NEW.contract_status = 1 AND OLD.contract_status = 0 THEN
        UPDATE house SET house_status=0 WHERE house_id = NEW.house_id;
        -- 自动新增押金退还记录
        INSERT INTO charge_record(contract_id,charge_type,charge_money,remark)
        VALUES (NEW.contract_id, 2, -OLD.real_rent / 2, '租房押金退还');
    END IF;
END //
DELIMITER ;

-- ====================== 插入测试房东数据 ======================
INSERT INTO landlord(land_name,land_phone,land_idcard,land_address) VALUES
('张三','13800001111','340101199001011234','合肥市蜀山区翡翠路XX小区1栋'),
('李四','13800002222','340101199202022345','合肥市高新区创新大道花园'),
('王五','13800003333','340101199403033456','合肥市包河区望江路小区'),
('赵六','13800004444','340101199604044567','合肥市庐阳区沿河路公寓');

-- ====================== 插入测试房源数据 ======================
INSERT INTO house(house_no,type_id,land_id,address,area,rent_price,deposit,facilities,house_status) VALUES
('A01-101',1,1,'蜀山区翡翠路幸福小区1栋101',45.5,1200.00,1200.00,'空调、热水器、床、衣柜',0),
('A01-102',2,1,'蜀山区翡翠路幸福小区1栋102',72.0,1800.00,1800.00,'空调、冰箱、洗衣机、燃气',1),
('B02-501',2,2,'高新区创新花园2栋501',85.0,2000.00,2000.00,'全套家电、宽带',0),
('C03-1202',3,3,'包河区望江苑3栋1202',110.0,2600.00,2600.00,'三室两厅、中央空调',1),
('D01-301',4,4,'庐阳沿河公馆1栋301',142.0,3200.00,3200.00,'四室、全屋家具',0);

-- ====================== 插入测试租客数据 ======================
INSERT INTO customer(cust_name,cust_phone,cust_idcard,work_unit) VALUES
('小明','13900001001','340102200001010011','互联网公司'),
('小红','13900001002','340102200102020022','中小学教师'),
('小陈','13900001003','340102200203030033','建筑设计院');

-- ====================== 插入租赁合同（租住中/已退租各一条，触发器自动改房源状态） ======================
-- 操作员都是admin（user_id=1）
INSERT INTO rent_contract(house_id,cust_id,start_date,end_date,real_rent,contract_status,return_date,operator_id) VALUES
(2,1,'2026-01-10','2027-01-09',1800.00,0,NULL,1),  -- A01-102 出租中，触发器自动变为已租
(4,2,'2025-06-01','2026-06-01',2600.00,0,NULL,1);  -- C03-1202 出租中，触发器自动变为已租

UPDATE rent_contract 
SET contract_status = 1, return_date = '2026-06-02'
WHERE contract_id = 2;  -- C03-1202 已退租，更新后房源自动变回空置

-- ====================== 插入收费记录（租金、押金、中介费） ======================
#INSERT INTO charge_record(contract_id,charge_type,charge_money,remark) VALUES
-- 合同1（租住中）缴费
#(1,1,1800.00,'房屋租金'),
#(1,2,900.00,'租房押金'),
#(1,3,360.00,'中介费'),
-- 合同2（已退租）历史缴费
#(2,2,900.00,'租房押金退还')