let pageInfo = getPageParams();
let keyword = "";

function loadList(page = 1) {
    pageInfo.page = page;
    http.get("/landlord/list", { params: { page: pageInfo.page, size: pageInfo.size, keyword } }).then(res => {
        pageInfo.total = res.data.total;
        const tbody = document.getElementById("tableBody");
        let html = "";
        res.data.list.forEach(item => {
            html += `
            <tr>
                <td>${item.land_id}</td>
                <td>${item.land_name}</td>
                <td>${item.land_phone}</td>
                <td>${item.land_idcard || "-"}</td>
                <td>${item.land_address || "-"}</td>
                <td>${formatDate(item.create_time)}</td>
                <td>
                    <button class="btn-link" onclick="openEdit(${item.land_id})">编辑</button>
                    <button class="btn-link danger" onclick="deleteItem(${item.land_id})">删除</button>
                </td>
            </tr>`;
        });
        tbody.innerHTML = html || '<tr><td colspan="7" class="text-center text-muted">暂无数据</td></tr>';
        renderPagination("pagination", pageInfo, "loadList");
    });
}

function searchLandlord() {
    keyword = document.getElementById("keyword").value.trim();
    loadList(1);
}

function openAddModal() {
    document.getElementById("modalTitle").textContent = "新增房东";
    document.getElementById("landId").value = "";
    document.getElementById("landName").value = "";
    document.getElementById("landPhone").value = "";
    document.getElementById("landIdcard").value = "";
    document.getElementById("landAddress").value = "";
    new bootstrap.Modal(document.getElementById("landlordModal")).show();
}

function openEdit(id) {
    http.get("/landlord/" + id).then(res => {
        document.getElementById("modalTitle").textContent = "编辑房东";
        document.getElementById("landId").value = res.data.land_id;
        document.getElementById("landName").value = res.data.land_name;
        document.getElementById("landPhone").value = res.data.land_phone;
        document.getElementById("landIdcard").value = res.data.land_idcard || "";
        document.getElementById("landAddress").value = res.data.land_address || "";
        new bootstrap.Modal(document.getElementById("landlordModal")).show();
    });
}

function saveLandlord() {
    const id = document.getElementById("landId").value;
    const data = {
        land_name: document.getElementById("landName").value.trim(),
        land_phone: document.getElementById("landPhone").value.trim(),
        land_idcard: document.getElementById("landIdcard").value.trim(),
        land_address: document.getElementById("landAddress").value.trim()
    };

    const api = id ? http.post("/landlord/update", { ...data, land_id: id }) : http.post("/landlord/add", data);
    api.then(res => {
        alert(res.msg);
        bootstrap.Modal.getInstance(document.getElementById("landlordModal")).hide();
        loadList();
    }).catch(() => {});
}

function deleteItem(id) {
    if (!confirm("确定删除该房东吗？")) return;
    http.delete("/landlord/delete/" + id).then(res => {
        alert(res.msg);
        loadList();
    }).catch(() => {});
}