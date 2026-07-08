let pageInfo = getPageParams();
let keyword = "";

function loadList(page = 1) {
    pageInfo.page = page;
    http.get("/customer/list", { params: { page: pageInfo.page, size: pageInfo.size, keyword } }).then(res => {
        pageInfo.total = res.total;
        const tbody = document.getElementById("tableBody");
        let html = "";
        res.list.forEach(item => {
            html += `
            <tr>
                <td>${item.cust_id}</td>
                <td>${item.cust_name}</td>
                <td>${item.cust_phone}</td>
                <td>${item.cust_idcard || "-"}</td>
                <td>${item.work_unit || "-"}</td>
                <td>${formatDate(item.create_time)}</td>
                <td>
                    <button class="btn-link" onclick="openEdit(${item.cust_id})">编辑</button>
                    <button class="btn-link danger" onclick="deleteItem(${item.cust_id})">删除</button>
                </td>
            </tr>`;
        });
        tbody.innerHTML = html || '<tr><td colspan="7" class="text-center text-muted">暂无数据</td></tr>';
        renderPagination("pagination", pageInfo, "loadList");
    });
}

function searchCustomer() {
    keyword = document.getElementById("keyword").value.trim();
    loadList(1);
}

function openAddModal() {
    document.getElementById("modalTitle").textContent = "新增租客";
    document.getElementById("custId").value = "";
    document.getElementById("custName").value = "";
    document.getElementById("custPhone").value = "";
    document.getElementById("custIdcard").value = "";
    document.getElementById("workUnit").value = "";
    new bootstrap.Modal(document.getElementById("customerModal")).show();
}

function openEdit(id) {
    http.get("/customer/" + id).then(res => {
        document.getElementById("modalTitle").textContent = "编辑租客";
        document.getElementById("custId").value = res.cust_id;
        document.getElementById("custName").value = res.cust_name;
        document.getElementById("custPhone").value = res.cust_phone;
        document.getElementById("custIdcard").value = res.cust_idcard || "";
        document.getElementById("workUnit").value = res.work_unit || "";
        new bootstrap.Modal(document.getElementById("customerModal")).show();
    });
}

function saveCustomer() {
    const id = document.getElementById("custId").value;
    const data = {
        cust_name: document.getElementById("custName").value.trim(),
        cust_phone: document.getElementById("custPhone").value.trim(),
        cust_idcard: document.getElementById("custIdcard").value.trim(),
        work_unit: document.getElementById("workUnit").value.trim()
    };

    if (!data.cust_name || !data.cust_phone) {
        alert("姓名和手机号不能为空");
        return;
    }

    const phoneReg = /(^\d{8}$)|(^\d{11}$)/;
    if (!phoneReg.test(data.cust_phone)) {
        alert("手机号必须为8或11位数字");
        return;
    }

    const idCardReg = /(^\d{15}$)|(^\d{17}[\dX]$)/;
    if (!idCardReg.test(data.cust_idcard)) {
        alert("身份证号必须为15位数字或18位数字(末位可为X)");
        return;
    }


    const api = id ? http.post("/customer/update", { ...data, cust_id: id }) : http.post("/customer/add", data);
    api.then(() => {
        alert("保存成功");
        bootstrap.Modal.getInstance(document.getElementById("customerModal")).hide();
        loadList();
    }).catch(() => {});
}

function deleteItem(id) {
    if (!confirm("确定删除该租客吗？")) return;
    http.delete("/customer/delete/" + id).then(() => {
        alert("删除成功");
        loadList();
    }).catch(() => {});
}