function loadBackupList() {
    http.get("/backup/list").then(res => {
        const tbody = document.getElementById("backupTableBody");
        let html = "";
        res.data.forEach(item => {
            html += `
            <tr>
                <td>${item.file_name}</td>
                <td>${item.create_time}</td>
                <td>
                    <button class="btn-link" onclick="doRestore('${item.file_name}')">恢复此备份</button>
                </td>
            </tr>`;
        });
        tbody.innerHTML = html || '<tr><td colspan="3" class="text-center text-muted">暂无备份文件</td></tr>';
    });
}

function doBackup() {
    if (!confirm("确认执行数据库备份吗？")) return;
    http.post("/backup/doBackup").then(res => {
        alert(res.msg);
        loadBackupList();
    }).catch(() => {});
}

function doRestore(fileName) {
    if (!confirm("警告：恢复操作将覆盖当前所有数据，确定要恢复吗？")) return;
    if (!confirm("再次确认：恢复后数据无法撤销，确定继续？")) return;

    http.post("/backup/doRestore", { file_name: fileName }).then(res => {
        alert(res.msg);
        loadBackupList();
    }).catch(() => {});
}