let typeModal;
window.onload = function() {
    typeModal = new bootstrap.Modal(document.getElementById("typeModal"));
};

// 加载户型列表
function loadTypeList() {
    http.get("/house/type/list").then(res => {
        const tbody = document.getElementById("tableBody");
        let html = "";
        res.data.forEach(item => {
            html += `
            <tr>
                <td>${item.type_id}</td>
                <td>${item.type_name}</td>
                <td>${item.remark || "-"}</td>
                <td>
                    <button class="btn-link" onclick="openEditModal(${item.type_id})">编辑</button>
                    <button class="btn-link danger" onclick="deleteType(${item.type_id})">删除</button>
                </td>
            </tr>`;
        });
        tbody.innerHTML = html || '<tr><td colspan="5" class="text-center text-muted">暂无数据</td></tr>';
    });
}

// 打开新增弹窗
function openAddModal() {
    document.getElementById("modalTitle").textContent = "新增户型";
    document.getElementById("typeId").value = "";
    document.getElementById("typeName").value = "";
    document.getElementById("remark").value = "";
    typeModal.show();
}

// 打开编辑弹窗
function openEditModal(id) {
    http.get("/house/type/" + id).then(res => {
        document.getElementById("modalTitle").textContent = "编辑户型";
        document.getElementById("typeId").value = res.data.type_id;
        document.getElementById("typeName").value = res.data.type_name;
        document.getElementById("remark").value = res.data.remark || "";
        typeModal.show();
    });
}

// 保存户型
function saveType() {
    const id = document.getElementById("typeId").value;
    const data = {
        type_name: document.getElementById("typeName").value.trim(),
        remark: document.getElementById("remark").value.trim()
    };

    const api = id ? http.post("/house/type/update", { ...data, type_id: id }) : http.post("/house/type/add", data);
    api.then(res => {
        alert(res.msg);
        typeModal.hide();
        loadTypeList();
    }).catch(() => {});
}

// 删除户型
function deleteType(id) {
    if (!confirm("确定要删除该户型吗？")) return;
    http.delete("/house/type/delete/" + id).then(res => {
        alert(res.msg);
        loadTypeList();
    }).catch(() => {});
}

// ===================== 房源管理 =====================
let housePage = getPageParams();
let houseKeyword = "";
let houseStatus = -1;
let selectTypeId = -1;
let selectProvince = "";
let selectCity = "";
let selectCounty = "";

function loadHouseList(page = 1) {
    housePage.page = page;
    const params = {
        page: housePage.page,
        size: housePage.size,
        keyword: houseKeyword,
        status: houseStatus,
        type_id: selectTypeId,
        province: selectProvince,
        city: selectCity,
        county: selectCounty
    };

    http.get("/house/list", { params }).then(res => {
        housePage.total = res.data.total;
        const tbody = document.getElementById("houseTableBody");
        let html = "";
        res.data.list.forEach(item => {
            const statusText = ["空置可租","已出租","维修中","已下架"][item.house_status];
            const statusClass = ["status-success","status-warning","status-info","status-danger"][item.house_status];
            html += `
            <tr>
                <td>${item.house_id}</td>
                <td>${item.province + item.city + item.county + item.address}</td>
                <td>${item.type_name}</td>
                <td>${item.land_name}</td>
                <td>${item.area}㎡</td>
                <td>${formatMoney(item.rent_price)}</td>
                <td><span class="status-tag ${statusClass}">${statusText}</span></td>
                <td>
                    <button class="btn-link" onclick="openHouseEdit(${item.house_id})">编辑</button>
                    <button class="btn-link danger" onclick="deleteHouse(${item.house_id})">删除</button>
                </td>
            </tr>`;
        });
        tbody.innerHTML = html || '<tr><td colspan="8" class="text-center text-muted">暂无数据</td></tr>';
        renderPagination("housePagination", housePage, "loadHouseList");
    });
}

// 自动搜索函数（联动清空下级下拉）
function searchHouse() {
    const provVal = document.getElementById("provinceSelect").value;
    const cityVal = document.getElementById("citySelect").value;

    // 省份切换，重置城市、区县
    if (provVal !== selectProvince) {
        document.getElementById("citySelect").value = "";
        document.getElementById("countySelect").value = "";
        loadCitySelect(provVal);
    }
    // 城市切换，重置区县
    if (cityVal !== selectCity) {
        document.getElementById("countySelect").value = "";
        loadCountySelect(provVal, cityVal);
    }

    selectProvince = document.getElementById("provinceSelect").value.trim();
    selectCity = document.getElementById("citySelect").value.trim();
    selectCounty = document.getElementById("countySelect").value.trim();
    houseKeyword = document.getElementById("houseKeyword").value.trim();
    houseStatus = document.getElementById("houseStatus").value;
    selectTypeId = parseInt(document.getElementById("typeSelect").value);
    loadHouseList(1);
}

function resetSearch() {
    document.getElementById("provinceSelect").value = "";
    document.getElementById("citySelect").value = "";
    document.getElementById("countySelect").value = "";
    document.getElementById("typeSelect").value = "-1";
    document.getElementById("houseKeyword").value = "";
    document.getElementById("houseStatus").value = "-1";
    selectProvince = "";
    selectCity = "";
    selectCounty = "";
    houseKeyword = "";
    houseStatus = -1;
    selectTypeId = -1;
    loadProvinceSelect();
    loadCitySelect();
    loadCountySelect();
    loadHouseList(1);
}

function openHouseAdd() {
    // 加载户型和房东下拉选项
    loadTypeSelect();
    loadLandlordSelect();
    document.getElementById("houseModalTitle").textContent = "新增房源";
    document.getElementById("houseForm").reset();
    document.getElementById("houseId").value = "";
    new bootstrap.Modal(document.getElementById("houseModal")).show();
}

function openHouseEdit(id) {
    loadTypeSelect();
    loadLandlordSelect();
    http.get("/house/" + id).then(res => {
        document.getElementById("houseModalTitle").textContent = "编辑房源";
        document.getElementById("houseId").value = res.data.house_id;
        document.getElementById("province").value = res.data.province;
        document.getElementById("city").value = res.data.city;
        document.getElementById("county").value = res.data.county;        
        document.getElementById("address").value = res.data.address;
        document.getElementById("typeId").value = res.data.type_id;
        document.getElementById("landId").value = res.data.land_id;
        document.getElementById("area").value = res.data.area;
        document.getElementById("rentPrice").value = res.data.rent_price;
        document.getElementById("facilities").value = res.data.facilities || "";
        document.getElementById("houseStatusSelect").value = res.data.house_status;
        new bootstrap.Modal(document.getElementById("houseModal")).show();
    });
}

function saveHouse() {
    const id = document.getElementById("houseId").value;
    const data = {
        province: document.getElementById("province").value.trim(),
        city: document.getElementById("city").value.trim(),
        county: document.getElementById("county").value.trim(),
        address: document.getElementById("address").value.trim(),
        type_id: document.getElementById("typeId").value,
        land_id: document.getElementById("landId").value,
        area: document.getElementById("area").value,
        rent_price: document.getElementById("rentPrice").value,
        facilities: document.getElementById("facilities").value.trim(),
        status: document.getElementById("houseStatusSelect").value
    };

    const api = id ? http.post("/house/update", { ...data, house_id: id }) : http.post("/house/add", data);
    api.then(res => {
        alert(res.msg);
        bootstrap.Modal.getInstance(document.getElementById("houseModal")).hide();
        loadProvinceSelect();
        loadCitySelect();
        loadCountySelect();
        loadHouseList();
    }).catch(() => {});
}

function deleteHouse(id) {
    if (!confirm("确定删除该房源吗？")) return;
    http.delete("/house/delete/" + id).then(res => {
        alert(res.msg);
        loadProvinceSelect();
        loadCitySelect();
        loadCountySelect();
        loadHouseList();
    }).catch(() => {});
}

// 加载户型下拉
function loadTypeSelect() {
    http.get("/house/type/list").then(res => {
        let html = '<option value="">请选择户型</option>';
        res.data.forEach(item => {
            html += `<option value="${item.type_id}">${item.type_name}</option>`;
        });
        document.getElementById("typeId").innerHTML = html;
    });
}

// 加载房东下拉
function loadLandlordSelect() {
    http.get("/landlord/list", { params: { page: 1, size: 1000 } }).then(res => {
        let html = '<option value="">请选择房东</option>';
        res.data.list.forEach(item => {
            html += `<option value="${item.land_id}">${item.land_name} - ${item.land_phone}</option>`;
        });
        document.getElementById("landId").innerHTML = html;
    });
}

// 加载户型筛选框下拉
function loadTypeFilterSelect() {
    http.get("/house/type/list").then(res => {
        let html = '<option value="-1">全部户型</option>';
        res.data.forEach(item => {
            html += `<option value="${item.type_id}">${item.type_name}</option>`;
        });
        document.getElementById("typeSelect").innerHTML = html;
    });
}

// 加载省份下拉
function loadProvinceSelect() {
    http.get("/location/province/list").then(res => {
        let html = '<option value="">全部省份</option>';
        res.data.forEach(item => {
            html += `<option value="${item.name}">${item.name}</option>`;
        });
        document.getElementById("provinceSelect").innerHTML = html;
    });
}

// 根据省份加载城市
function loadCitySelect(province = "") {
    let params = {};
    if (province) params.province = province;
    http.get("/location/city/list", { params }).then(res => {
        let html = '<option value="">全部城市</option>';
        res.data.forEach(item => {
            html += `<option value="${item.name}">${item.name}</option>`;
        });
        document.getElementById("citySelect").innerHTML = html;
    });
}

// 根据省+市加载区县
function loadCountySelect(province = "", city = "") {
    let params = {};
    if (province) params.province = province;
    if (city) params.city = city;
    http.get("/location/county/list", { params }).then(res => {
        let html = '<option value="">全部区县</option>';
        res.data.forEach(item => {
            html += `<option value="${item.name}">${item.name}</option>`;
        });
        document.getElementById("countySelect").innerHTML = html;
    });
}
