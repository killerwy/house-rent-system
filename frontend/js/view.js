let viewPage = getPageParams();
let keyword = "";
let viewHouseStatus = "";
let viewTypeName = "";
let viewProvince = "";
let viewCity = "";
let viewCounty = "";

function loadViewList(page = 1) {
    viewPage.page = page;
    const params = {
        page: viewPage.page,
        size: viewPage.size,
        keyword: keyword,
        status: viewHouseStatus,
        type_name: viewTypeName,
        province: viewProvince,
        city: viewCity,
        county: viewCounty
    };
    http.get("/view/houseAll", { params }).then(res => {
        viewPage.total = res.data.total;
        const tbody = document.getElementById("viewTableBody");
        let html = "";
        res.data.list.forEach(item => {
            const statusClass = item.房屋状态 === "空置可租" ? "status-success" : 
                               item.房屋状态 === "已出租" ? "status-warning" : "status-info";
            html += `
            <tr>
                <td>${item.省份 + item.城市 + item.区县 + item.房屋地址}</td>
                <td>${item.房东姓名}</td>
                <td>${item.房东电话}</td>
                <td>${item.户型}</td>
                <td><span class="status-tag ${statusClass}">${item.房屋状态}</span></td>
                <td>${formatMoney(item.月租金)}</td>
            </tr>`;
        });
        tbody.innerHTML = html || '<tr><td colspan="7" class="text-center text-muted">暂无数据</td></tr>';
        renderPagination("viewPagination", viewPage, "loadViewList");
    });
}

// 自动筛选，无需点击搜索按钮
function searchView() {
    const provVal = document.getElementById("provinceSelectView").value;
    const cityVal = document.getElementById("citySelectView").value;

    // 切换省份，清空下级城市、区县并重载城市下拉
    if (provVal !== viewProvince) {
        document.getElementById("citySelectView").value = "";
        document.getElementById("countySelectView").value = "";
        loadCitySelectView(provVal);
    }
    // 切换城市，清空区县并重载区县下拉
    if (cityVal !== viewCity) {
        document.getElementById("countySelectView").value = "";
        loadCountySelectView(provVal, cityVal);
    }

    viewProvince = document.getElementById("provinceSelectView").value
    viewCity = document.getElementById("citySelectView").value;
    viewCounty = document.getElementById("countySelectView").value;
    keyword = document.getElementById("keyword").value.trim();
    viewHouseStatus = document.getElementById("houseStatusView").value;
    viewTypeName = document.getElementById("typeSelectView").value.trim();
    loadViewList(1);
}

// 重置所有筛选条件
function resetViewSearch() {
    document.getElementById("provinceSelectView").value = "";
    document.getElementById("citySelectView").value = "";
    document.getElementById("countySelectView").value = "";
    document.getElementById("keyword").value = "";
    document.getElementById("houseStatusView").value = "";
    document.getElementById("typeSelectView").value = "";

    viewProvince = "";
    viewCity = "";
    viewCounty = "";
    keyword = "";
    viewHouseStatus = "";
    viewTypeName = "";

    // 恢复全部城市、区县下拉选项
    loadProvinceSelectView();
    loadCitySelectView();
    loadCountySelectView();
    loadViewList(1);
}

// 加载省份下拉
function loadProvinceSelectView() {
    http.get("/location/province/list").then(res => {
        let html = '<option value="">全部省份</option>';
        res.data.forEach(item => {
            html += `<option value="${item.name}">${item.name}</option>`;
        });
        document.getElementById("provinceSelectView").innerHTML = html;
    });
}

// 根据省份加载城市
function loadCitySelectView(province = "") {
    let params = {};
    if (province) params.province = province;
    http.get("/location/city/list", { params }).then(res => {
        let html = '<option value="">全部城市</option>';
        res.data.forEach(item => {
            html += `<option value="${item.name}">${item.name}</option>`;
        });
        document.getElementById("citySelectView").innerHTML = html;
    });
}

// 根据省+市加载区县
function loadCountySelectView(province = "", city = "") {
    let params = {};
    if (province) params.province = province;
    if (city) params.city = city;
    http.get("/location/county/list", { params }).then(res => {
        let html = '<option value="">全部区县</option>';
        res.data.forEach(item => {
            html += `<option value="${item.name}">${item.name}</option>`;
        });
        document.getElementById("countySelectView").innerHTML = html;
    });
}

// 加载视图页面户型筛选下拉
function loadTypeSelectView() {
    http.get("/house/type/list").then(res => {
        let html = '<option value="">全部户型</option>';
        res.data.forEach(item => {
            html += `<option value="${item.type_name}">${item.type_name}</option>`;
        });
        document.getElementById("typeSelectView").innerHTML = html;
    });
}