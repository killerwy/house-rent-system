let typeModal;
window.onload = function() {
    typeModal = new bootstrap.Modal(document.getElementById("typeModal"));
};

// 加载户型列表
function loadTypeList() {
    http.get("/house/type/list").then(res => {
        const tbody = document.getElementById("tableBody");
        let html = "";
        res.forEach(item => {
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
        document.getElementById("typeId").value = res.type_id;
        document.getElementById("typeName").value = res.type_name;
        document.getElementById("remark").value = res.remark || "";
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

    if (!data.type_name) {
        alert("户型名称不能为空");
        return;
    }

    const api = id ? http.post("/house/type/update", { ...data, type_id: id }) : http.post("/house/type/add", data);
    api.then(() => {
        alert("保存成功");
        typeModal.hide();
        loadTypeList();
    }).catch(() => {});
}

// 删除户型
function deleteType(id) {
    if (!confirm("确定要删除该户型吗？")) return;
    http.delete("/house/type/delete/" + id).then(() => {
        alert("删除成功");
        loadTypeList();
    }).catch(() => {});
}

// ===================== 房源管理 =====================
let housePage = getPageParams();
let houseKeyword = "";
let houseStatus = -1;

function loadHouseList(page = 1) {
    housePage.page = page;
    const params = {
        page: housePage.page,
        size: housePage.size,
        keyword: houseKeyword,
        status: houseStatus
    };

    http.get("/house/list", { params }).then(res => {
        housePage.total = res.total;
        const tbody = document.getElementById("houseTableBody");
        let html = "";
        res.list.forEach(item => {
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

function searchHouse() {
    houseKeyword = document.getElementById("houseKeyword").value.trim();
    houseStatus = document.getElementById("houseStatus").value;
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
        document.getElementById("houseId").value = res.house_id;
        document.getElementById("province").value = res.province;
        document.getElementById("city").value = res.city;
        document.getElementById("county").value = res.county;        
        document.getElementById("address").value = res.address;
        document.getElementById("typeId").value = res.type_id;
        document.getElementById("landId").value = res.land_id;
        document.getElementById("area").value = res.area;
        document.getElementById("rentPrice").value = res.rent_price;
        document.getElementById("facilities").value = res.facilities || "";
        document.getElementById("houseStatusSelect").value = res.house_status;
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

    if (!data.type_id || !data.land_id || !data.province || !data.city || !data.county || !data.address) {
        alert("必填项不能为空");
        return;
    }

    const area = Number(document.getElementById("area").value);
    const rent = Number(document.getElementById("rentPrice").value);
    if (isNaN(area) || area < 0) {
        alert("建筑面积不能为负数");
        return;
    }
    if (isNaN(rent) || rent < 0) {
        alert("月租金不能为负数");
        return;
    }

    const api = id ? http.post("/house/update", { ...data, house_id: id }) : http.post("/house/add", data);
    api.then(() => {
        alert("保存成功");
        bootstrap.Modal.getInstance(document.getElementById("houseModal")).hide();
        loadHouseList();
    }).catch(() => {});
}

function deleteHouse(id) {
    if (!confirm("确定删除该房源吗？")) return;
    http.delete("/house/delete/" + id).then(() => {
        alert("删除成功");
        loadHouseList();
    }).catch(() => {});
}

// 加载户型下拉
function loadTypeSelect() {
    http.get("/house/type/list").then(res => {
        let html = '<option value="">请选择户型</option>';
        res.forEach(item => {
            html += `<option value="${item.type_id}">${item.type_name}</option>`;
        });
        document.getElementById("typeId").innerHTML = html;
    });
}

// 加载房东下拉
function loadLandlordSelect() {
    http.get("/landlord/list", { params: { page: 1, size: 1000 } }).then(res => {
        let html = '<option value="">请选择房东</option>';
        res.list.forEach(item => {
            html += `<option value="${item.land_id}">${item.land_name} - ${item.land_phone}</option>`;
        });
        document.getElementById("landId").innerHTML = html;
    });
}