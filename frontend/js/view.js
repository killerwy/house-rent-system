let viewPage = getPageParams();
let keyword = "";

function loadViewList(page = 1) {
    viewPage.page = page;
    http.get("/view/houseAll", { params: { page: viewPage.page, size: viewPage.size, keyword } }).then(res => {
        viewPage.total = res.total;
        const tbody = document.getElementById("viewTableBody");
        let html = "";
        res.list.forEach(item => {
            const statusClass = item.房屋状态 === "空置可租" ? "status-success" : 
                               item.房屋状态 === "已出租" ? "status-warning" : "status-info";
            html += `
            <tr>
                <td>${item.房屋地址}</td>
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

function searchView() {
    keyword = document.getElementById("keyword").value.trim();
    loadViewList(1);
}