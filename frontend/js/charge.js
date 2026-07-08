let chargePage = getPageParams();
let chargeKeyword = "";
let chargeTypeFilter = -1;

const typeMap = { 1: "租金", 2: "押金", 3: "中介费" };

function loadChargeList(page = 1) {
    chargePage.page = page;
    http.get("/charge/list", { 
        params: { page: chargePage.page, size: chargePage.size, keyword: chargeKeyword, charge_type: chargeTypeFilter } 
    }).then(res => {
        chargePage.total = res.data.total;
        const tbody = document.getElementById("chargeTableBody");
        let html = "";
        res.data.list.forEach(item => {
            html += `
            <tr>
                <td>${item.charge_id}</td>
                <td>${item.rent_id}</td>
                <td>${item.province + item.city + item.county + item.address}</td>
                <td>${item.cust_name}</td>
                <td>${typeMap[item.charge_type]}</td>
                <td>${formatMoney(item.charge_money)}</td>
                <td>${formatDate(item.charge_time)}</td>
                <td>${item.remark || "-"}</td>
            </tr>`;
        });
        tbody.innerHTML = html || '<tr><td colspan="8" class="text-center text-muted">暂无数据</td></tr>';
        renderPagination("chargePagination", chargePage, "loadChargeList");
    });
}

function searchCharge() {
    chargeKeyword = document.getElementById("chargeKeyword").value;
    chargeTypeFilter = document.getElementById("chargeType").value;
    loadChargeList(1);
}

function openAddModal() {
    // 加载有效合同下拉
    http.get("/rent/list", { params: { page:1, size:1000, status:0 } }).then(res => {
        let html = '<option value="">请选择租赁合同</option>';
        res.data.list.forEach(item => {
            html += `<option value="${item.rent_id}">合同${item.rent_id} - ${item.province + item.city + item.county + item.address} - ${item.cust_name}</option>`;
        });
        document.getElementById("rentSelect").innerHTML = html;
    });
    document.getElementById("chargeTypeSelect").value = 1;
    document.getElementById("chargeMoney").value = "";
    document.getElementById("chargeRemark").value = "";
    new bootstrap.Modal(document.getElementById("chargeModal")).show();
}

function saveCharge() {
    const data = {
        rent_id: document.getElementById("rentSelect").value,
        charge_type: document.getElementById("chargeTypeSelect").value,
        charge_money: document.getElementById("chargeMoney").value,
        remark: document.getElementById("chargeRemark").value.trim()
    };

    http.post("/charge/add", data).then(res => {
        alert(res.msg);
        bootstrap.Modal.getInstance(document.getElementById("chargeModal")).hide();
        loadChargeList();
    }).catch(() => {});
}