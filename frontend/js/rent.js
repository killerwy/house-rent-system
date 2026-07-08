// 加载空置房源下拉
function loadEmptyHouseList() {
    http.get("/house/list", { params: { page:1, size:1000, status:0 } }).then(res => {
        let html = '<option value="">请选择空置房源</option>';
        res.data.list.forEach(item => {
            html += `<option value="${item.house_id}" data-rent="${item.rent_price}">${item.province + item.city + item.county + item.address} (${formatMoney(item.rent_price)}/月)</option>`;
        });
        document.getElementById("houseSelect").innerHTML = html;
        // 选择房屋自动填充租金
        document.getElementById("houseSelect").onchange = function() {
            const selected = this.options[this.selectedIndex];
            if (selected.value) {
                document.getElementById("realRent").value = selected.dataset.rent;
            }
        };
    });
}

// 加载租客下拉
function loadCustomerList() {
    http.get("/customer/list", { params: { page:1, size:1000 } }).then(res => {
        let html = '<option value="">请选择租客</option>';
        res.data.list.forEach(item => {
            html += `<option value="${item.cust_id}">${item.cust_name} - ${item.cust_phone}</option>`;
        });
        document.getElementById("custSelect").innerHTML = html;
    });
}

// 提交出租登记
function submitRent() {
    const data = {
        house_id: document.getElementById("houseSelect").value,
        cust_id: document.getElementById("custSelect").value,
        start_date: document.getElementById("startDate").value,
        end_date: document.getElementById("endDate").value,
        real_rent: document.getElementById("realRent").value
    };

    if (!confirm("确认提交出租登记吗？提交后房屋状态将自动变更为已出租")) return;

    http.post("/rent/add", data).then(res => {
        alert(res.msg);
        window.location.href = "rent_list.html";
    }).catch(() => {});
}

// ===================== 合同列表 =====================
let rentPage = getPageParams();
let rentKeyword = "";
let rentStatus = -1;

function loadRentList(page = 1) {
    rentPage.page = page;
    http.get("/rent/list", { 
        params: { page: rentPage.page, size: rentPage.size, keyword: rentKeyword, status: rentStatus } 
    }).then(res => {
        rentPage.total = res.data.total;
        const tbody = document.getElementById("rentTableBody");
        let html = "";
        res.data.list.forEach(item => {
            const statusText = item.rent_status === 0 ? "租住中" : "已退租";
            const statusClass = item.rent_status === 0 ? "status-warning" : "status-success";
            html += `
            <tr>
                <td>${item.rent_id}</td>
                <td>${item.province + item.city + item.county + item.address}</td>
                <td>${item.cust_name}</td>
                <td>${formatDate(item.start_date)}</td>
                <td>${formatDate(item.end_date)}</td>
                <td>${formatMoney(item.real_rent)}</td>
                <td><span class="status-tag ${statusClass}">${statusText}</span></td>
                <td>${item.operator_name}</td>
                <td>${formatDate(item.create_time)}</td>
                <td>
                    <button class="btn-link" onclick="viewRent(${item.rent_id})">详情</button>
                    ${item.rent_status === 0 ? `<button class="btn-link" onclick="openReturnModal(${item.rent_id})">办理退租</button>` : ""}
                </td>
            </tr>`;
        });
        tbody.innerHTML = html || '<tr><td colspan="9" class="text-center text-muted">暂无数据</td></tr>';
        renderPagination("rentPagination", rentPage, "loadRentList");
    });
}

function searchRent() {
    rentKeyword = document.getElementById("rentKeyword").value.trim();
    rentStatus = document.getElementById("rentStatus").value;
    loadRentList(1);
}

// 打开退租弹窗
function openReturnModal(rentId) {
    document.getElementById("returnRentId").value = rentId;
    document.getElementById("returnDate").valueAsDate = new Date();
    new bootstrap.Modal(document.getElementById("returnModal")).show();
}

// 提交退租
function submitReturn() {
    const rentId = document.getElementById("returnRentId").value;
    const returnDate = document.getElementById("returnDate").value;
    
    if (!confirm("确认办理退租吗？退租后房屋状态将自动变更为空置")) return;

    http.post("/rent/return", { rent_id: rentId, return_date: returnDate }).then(res => {
        alert(res.msg);
        bootstrap.Modal.getInstance(document.getElementById("returnModal")).hide();
        loadRentList();
    }).catch(() => {});
}

function viewRent(id) {
    http.get("/rent/" + id).then(res => {
        alert(`合同详情：\n合同号：${res.data.rent_id}\n地址：${res.data.province + res.data.city + res.data.county + res.data.address}\n租客：${res.data.cust_name}\n起租：${formatDate(res.data.start_date)}\n到期：${formatDate(res.data.end_date)}\n月租金：${formatMoney(res.data.real_rent)}\n状态：${res.data.rent_status===0?"租住中":"已退租"}`);
    });
}