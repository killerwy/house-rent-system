function loadStatData() {
    http.get("/stat/rentByType").then(res => {
        // 渲染表格
        const tbody = document.getElementById("statTableBody");
        let html = "";
        const xData = [];
        const rentData = [];
        const emptyData = [];

        res.data.forEach(item => {
            const rate = item.总房源数 > 0 ? ((item.已出租数量 / item.总房源数) * 100).toFixed(1) + "%" : "-";
            html += `
            <tr>
                <td>${item.户型名称}</td>
                <td>${item.总房源数}</td>
                <td>${item.已出租数量}</td>
                <td>${item.空置数量}</td>
                <td>${rate}</td>
            </tr>`;
            xData.push(item.户型名称);
            rentData.push(item.已出租数量);
            emptyData.push(item.空置数量);
        });
        tbody.innerHTML = html;

        // 渲染柱状图
        const chart = echarts.init(document.getElementById("statChart"));
        const option = {
            title: { text: "各户型出租情况对比", left: "center" },
            tooltip: { trigger: "axis" },
            legend: { data: ["已出租", "空置"], bottom: 0 },
            xAxis: { type: "category", data: xData },
            yAxis: { type: "value", minInterval: 1 },
            series: [
                { name: "已出租", type: "bar", data: rentData, itemStyle: { color: "#e6a23c" } },
                { name: "空置", type: "bar", data: emptyData, itemStyle: { color: "#67c23a" } }
            ]
        };
        chart.setOption(option);
        window.addEventListener("resize", () => chart.resize());
    });
}