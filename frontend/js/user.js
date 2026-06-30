let userPage = getPageParams();
let keyword = "";

function loadUserList(page = 1) {
    userPage.page = page;
    http.get("/user/list", { params: { page: userPage.page, size: userPage.size, keyword } }).then(res => {
        userPage.total = res.total;
        const tbody = document.getElementById("userTableBody");
        let html = "";
        res.list.forEach(item => {
            html += `
            <tr>
                <td>${item.user_id}</td>
                <td>${item.username}</td>
                <td>${item.real_name}</td>
                <td>${item.phone || "-"}</td>
                <td>${item.role_name}</td>
                <td>${formatDate(item.create_time)}</td>
                <td>
                    <button class="btn-link" onclick="openEdit(${item.user_id})">编辑</button>
                    <button class="btn-link" onclick="openPwdModal(${item.user_id})">改密码</button>
                    <button class="btn-link danger" onclick="deleteUser(${item.user_id})">删除</button>
                </td>
            </tr>`;
        });
        tbody.innerHTML = html || '<tr><td colspan="7" class="text-center text-muted">暂无数据</td></tr>';
        renderPagination("userPagination", userPage, "loadUserList");
    });
}

function searchUser() {
    keyword = document.getElementById("keyword").value.trim();
    loadUserList(1);
}

function openAddModal() {
    document.getElementById("userModalTitle").textContent = "新增员工";
    document.getElementById("userId").value = "";
    document.getElementById("username").value = "";
    document.getElementById("password").value = "";
    document.getElementById("realName").value = "";
    document.getElementById("phone").value = "";
    document.getElementById("roleId").value = 2;
    document.getElementById("pwdGroup").style.display = "block";
    new bootstrap.Modal(document.getElementById("userModal")).show();
}

function openEdit(id) {
    http.get("/user/" + id).then(res => {
        document.getElementById("userModalTitle").textContent = "编辑员工";
        document.getElementById("userId").value = res.user_id;
        document.getElementById("username").value = res.username;
        document.getElementById("realName").value = res.real_name;
        document.getElementById("phone").value = res.phone || "";
        document.getElementById("roleId").value = res.role_id;
        document.getElementById("pwdGroup").style.display = "none"; // 编辑不修改密码
        new bootstrap.Modal(document.getElementById("userModal")).show();
    });
}

function saveUser() {
    const id = document.getElementById("userId").value;
    const data = {
        username: document.getElementById("username").value.trim(),
        real_name: document.getElementById("realName").value.trim(),
        phone: document.getElementById("phone").value.trim(),
        role_id: document.getElementById("roleId").value
    };

    if (!data.username || !data.real_name || !data.role_id) {
        alert("必填项不能为空");
        return;
    }

    let api;
    if (id) {
        api = http.post("/user/update", { ...data, user_id: id });
    } else {
        const pwd = document.getElementById("password").value.trim();
        if (!pwd) {
            alert("请设置初始密码");
            return;
        }
        api = http.post("/user/add", { ...data, password: pwd });
    }

    api.then(() => {
        alert("保存成功");
        bootstrap.Modal.getInstance(document.getElementById("userModal")).hide();
        loadUserList();
    }).catch(() => {});
}

function openPwdModal(id) {
    document.getElementById("pwdUserId").value = id;
    document.getElementById("newPassword").value = "";
    new bootstrap.Modal(document.getElementById("pwdModal")).show();
}

function submitPwd() {
    const id = document.getElementById("pwdUserId").value;
    const newPwd = document.getElementById("newPassword").value.trim();
    if (!newPwd) {
        alert("请输入新密码");
        return;
    }
    http.post("/user/updatePwd", { user_id: id, new_password: newPwd }).then(() => {
        alert("密码修改成功");
        bootstrap.Modal.getInstance(document.getElementById("pwdModal")).hide();
    }).catch(() => {});
}

function deleteUser(id) {
    if (!confirm("确定删除该员工账号吗？")) return;
    http.delete("/user/delete/" + id).then(() => {
        alert("删除成功");
        loadUserList();
    }).catch(() => {});
}