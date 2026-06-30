// 加载空置房源下拉
function loadEmptyHouseList() {
    http.get("/house/list", { params: { page:1, size:1000, status:0 } }).then(res => {
        let html = '<option value="">请选择空置房源</option>';
        res.list.forEach(item => {
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
        res.list.forEach(item => {
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

    if (!data.house_id || !data.cust_id || !data.start_date || !data.end_date || !data.real_rent) {
        alert("请填写完整信息");
        return;
    }

    if (!confirm("确认提交出租登记吗？提交后房屋状态将自动变更为已出租")) return;

    http.post("/rent/add", data).then(() => {
        alert("出租登记成功！");
        window.location.href = "rent_list.html";
    }).catch(() => {});
}

// ===================== 合同列表 =====================
let contractPage = getPageParams();
let contractKeyword = "";
let contractStatus = -1;

function loadContractList(page = 1) {
    contractPage.page = page;
    http.get("/rent/list", { 
        params: { page: contractPage.page, size: contractPage.size, keyword: contractKeyword, status: contractStatus } 
    }).then(res => {
        contractPage.total = res.total;
        const tbody = document.getElementById("contractTableBody");
        let html = "";
        res.list.forEach(item => {
            const statusText = item.contract_status === 0 ? "租住中" : "已退租";
            const statusClass = item.contract_status === 0 ? "status-warning" : "status-success";
            html += `
            <tr>
                <td>${item.contract_id}</td>
                <td>${item.province + item.city + item.county + item.address}</td>
                <td>${item.cust_name}</td>
                <td>${formatDate(item.start_date)}</td>
                <td>${formatDate(item.end_date)}</td>
                <td>${formatMoney(item.real_rent)}</td>
                <td><span class="status-tag ${statusClass}">${statusText}</span></td>
                <td>${item.operator_name}</td>
                <td>${formatDate(item.create_time)}</td>
                <td>
                    <button class="btn-link" onclick="viewContract(${item.contract_id})">详情</button>
                    ${item.contract_status === 0 ? `<button class="btn-link" onclick="openReturnModal(${item.contract_id})">办理退租</button>` : ""}
                </td>
            </tr>`;
        });
        tbody.innerHTML = html || '<tr><td colspan="9" class="text-center text-muted">暂无数据</td></tr>';
        renderPagination("contractPagination", contractPage, "loadContractList");
    });
}

function searchContract() {
    contractKeyword = document.getElementById("contractKeyword").value.trim();
    contractStatus = document.getElementById("contractStatus").value;
    loadContractList(1);
}

// 打开退租弹窗
function openReturnModal(contractId) {
    document.getElementById("returnContractId").value = contractId;
    document.getElementById("returnDate").valueAsDate = new Date();
    new bootstrap.Modal(document.getElementById("returnModal")).show();
}

// 提交退租
function submitReturn() {
    const contractId = document.getElementById("returnContractId").value;
    const returnDate = document.getElementById("returnDate").value;
    
    if (!returnDate) {
        alert("请选择归还日期");
        return;
    }
    if (!confirm("确认办理退租吗？退租后房屋状态将自动变更为空置")) return;

    http.post("/rent/return", { contract_id: contractId, return_date: returnDate }).then(() => {
        alert("退租办理成功！");
        bootstrap.Modal.getInstance(document.getElementById("returnModal")).hide();
        loadContractList();
    }).catch(() => {});
}

function viewContract(id) {
    http.get("/rent/" + id).then(res => {
        alert(`合同详情：\n合同号：${res.contract_id}\n地址：${res.province + res.city + res.county + res.address}\n租客：${res.cust_name}\n起租：${formatDate(res.start_date)}\n到期：${formatDate(res.end_date)}\n月租金：${formatMoney(res.real_rent)}\n状态：${res.contract_status===0?"租住中":"已退租"}`);
    });
}