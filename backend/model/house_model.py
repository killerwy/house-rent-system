"""房源模型"""
from db.mysql_conn import MySQLConnection
from util.page_util import build_page_sql, get_total_count
from model.location_model import LocationModel

class HouseModel:
    @staticmethod
    def get_house_list(offset, size, keyword="", status=-1, province="", city="", county="", type_id=-1):
        """分页查询房源（支持地址搜索、状态筛选）"""
        # 构建查询条件
        where_conditions = []
        params = []
        # 搜索关键词
        if keyword:
            where_conditions.append("(loc.province LIKE %s OR loc.city LIKE %s OR loc.county LIKE %s OR h.address LIKE %s OR l.land_name LIKE %s)")
            like_keyword = f"%{keyword}%"
            params.extend([like_keyword, like_keyword, like_keyword, like_keyword, like_keyword])
        # 省精确筛选
        if province:
            where_conditions.append("loc.province = %s")
            params.append(province)
        # 市精确筛选
        if city:
            where_conditions.append("loc.city = %s")
            params.append(city)
        # 区县精确筛选
        if county:
            where_conditions.append("loc.county = %s")
            params.append(county)
        # 户型筛选
        if type_id != -1:
            where_conditions.append("h.type_id = %s")
            params.append(type_id)
        # 状态筛选
        if status != -1:
            where_conditions.append("house_status = %s")
            params.append(status)
        # 拼接WHERE子句
        where_sql = " WHERE " + " AND ".join(where_conditions) if where_conditions else ""
        
        # 基础SQL
        base_sql = f"""
        SELECT h.*, loc.province, loc.city, loc.county, ht.type_name, l.land_name, l.land_phone 
        FROM house h
        LEFT JOIN location loc ON h.loc_id = loc.loc_id
        LEFT JOIN house_type ht ON h.type_id = ht.type_id
        LEFT JOIN landlord l ON h.land_id = l.land_id
        {where_sql}
        ORDER BY h.house_id DESC
        """
        # 计数SQL
        count_sql = f"""
        SELECT COUNT(*) as total FROM house h
        LEFT JOIN location loc ON h.loc_id = loc.loc_id
        LEFT JOIN landlord l ON h.land_id = l.land_id
        {where_sql}
        """
        
        # 分页查询
        page_sql = build_page_sql(base_sql, offset, size)
        list_data = MySQLConnection.execute_sql(page_sql, params, fetch_type="all")
        # 总条数
        total = get_total_count(count_sql, params)
        
        return total, list_data

    @staticmethod
    def add_house(province, city, county, address, type_id, land_id, area, rent_price, facilities="", house_status=0):
        """新增房源"""
        # 自动获取/创建区域ID
        loc_id = LocationModel.get_or_create(province, city, county)

        sql = """
        INSERT INTO house(loc_id, address, type_id, land_id, area, rent_price, facilities, house_status) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        return MySQLConnection.execute_sql(sql, (loc_id, address, type_id, land_id, area, rent_price, facilities, house_status))

    @staticmethod
    def update_house(house_id, province, city, county, address, type_id, land_id, area, rent_price, facilities="", house_status=0):
        """修改房源"""
        # 查询原房源信息，获取旧区域ID
        old_house = HouseModel.get_house_by_id(house_id)
        if not old_house:
            return 0
        old_loc_id = old_house["loc_id"]
        
        # 获取新区域ID
        new_loc_id = LocationModel.get_or_create(province, city, county)

        sql = """
        UPDATE house 
        SET loc_id=%s, address=%s, type_id=%s, land_id=%s, area=%s, rent_price=%s, facilities=%s, house_status=%s 
        WHERE house_id=%s
        """
        result = MySQLConnection.execute_sql(sql, (new_loc_id, address, type_id, land_id, area, rent_price, facilities, house_status, house_id))
        
        # 若区域发生变更，检查旧区域是否还有房源引用，无则删除
        if result > 0 and new_loc_id != old_loc_id:
            house_count = LocationModel.count_house_by_loc(old_loc_id)
            if house_count == 0:
                LocationModel.delete_location(old_loc_id)
        
        return result

    @staticmethod
    def delete_house(house_id):
        """删除房源（检查关联合同）"""
        house_info = HouseModel.get_house_by_id(house_id)
        if not house_info:
            return 0
        loc_id = house_info["loc_id"]

        # 检查关联合同
        check_sql = "SELECT COUNT(*) as total FROM rent WHERE house_id = %s"
        check_result = MySQLConnection.execute_sql(check_sql, (house_id,), fetch_type="one")
        if check_result["total"] > 0:
            return -1
        # 执行删除
        sql = "DELETE FROM house WHERE house_id = %s"
        result = MySQLConnection.execute_sql(sql, (house_id,))

        # 删除成功后，检查该区域是否还有其他房源，无则删除区域
        if result > 0:
            house_count = LocationModel.count_house_by_loc(loc_id)
            if house_count == 0:
                LocationModel.delete_location(loc_id)
        
        return result

    @staticmethod
    def get_house_by_id(house_id):
        """根据ID查询房源"""
        sql = """
        SELECT h.*, loc.province, loc.city, loc.county, ht.type_name, l.land_name, l.land_phone 
        FROM house h
        LEFT JOIN location loc ON h.loc_id = loc.loc_id
        LEFT JOIN house_type ht ON h.type_id = ht.type_id
        LEFT JOIN landlord l ON h.land_id = l.land_id
        WHERE h.house_id = %s
        """
        return MySQLConnection.execute_sql(sql, (house_id,), fetch_type="one")
    
    @staticmethod
    def get_house_by_address(province, city, county, address):
        """根据房屋地址查询房源"""
        sql = """
        SELECT h.*, loc.province, loc.city, loc.county
        FROM house h
        LEFT JOIN location loc ON h.loc_id = loc.loc_id
        WHERE loc.province = %s AND loc.city = %s AND loc.county = %s AND h.address = %s
        """
        return MySQLConnection.execute_sql(sql, (province, city, county, address), fetch_type="one")
    
    @staticmethod
    def update_house_status(house_id, status):
        """更新房源状态"""
        sql = "UPDATE house SET house_status = %s WHERE house_id = %s"
        return MySQLConnection.execute_sql(sql, (status, house_id))
    
    @staticmethod
    def get_type_by_id(type_id):
        """根据ID查询户型"""
        sql = "SELECT * FROM house_type WHERE type_id = %s"
        return MySQLConnection.execute_sql(sql, (type_id,), fetch_type="one")