// 后端接口基础地址
const BASE_URL = "http://localhost:5000";

// 封装axios实例
const http = axios.create({
    baseURL: BASE_URL + "/api",
    timeout: 10000
});

// 请求拦截器：添加token
http.interceptors.request.use(
    config => {
        const token = localStorage.getItem("access_token");
        if (token) {
            config.headers.Authorization = "Bearer " + token;
        }
        return config;
    },
    error => Promise.reject(error)
);

// 响应拦截器：统一处理错误
http.interceptors.response.use(
    response => {
        const res = response.data;
        if (res.code !== 200) {
            alert(res.msg || "请求失败");
            // 401未授权，跳登录
            if (res.code === 401) {
                logout();
            }
            return Promise.reject(res);
        }
        return res.data;
    },
    error => {
        if (error.response && error.response.status === 401) {
            alert("登录已过期，请重新登录");
            logout();
        } else {
            alert("网络请求失败：" + (error.message || "未知错误"));
        }
        return Promise.reject(error);
    }
);

// 登录相关
function login(username, password) {
    return http.post("/auth/login", { username, password });
}

function getUserInfo() {
    return http.get("/auth/info");
}

function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_info");
    // 跳登录页
    if (window.top !== window.self) {
        window.top.location.href = "index.html";
    } else {
        window.location.href = "index.html";
    }
}

// 获取当前登录用户信息
function getCurrentUser() {
    const userStr = localStorage.getItem("user_info");
    return userStr ? JSON.parse(userStr) : null;
}

// 权限校验
function hasPermission(perm) {
    const user = getCurrentUser();
    if (!user) return false;
    // 超级管理员全部权限
    if (user.role_id === 1) return true;
    // 中介员工权限
    const rolePerms = {
        2: ["house", "landlord", "customer", "rent", "charge", "stat", "view"],
        3: ["view", "stat"]
    };
    return (rolePerms[user.role_id] || []).includes(perm);
}

// 检查登录状态（子页面调用）
function checkLogin() {
    const token = localStorage.getItem("access_token");
    if (!token) {
        logout();
        return false;
    }
    return true;
}

// 通用分页参数
function getPageParams() {
    return {
        page: 1,
        size: 10,
        total: 0
    };
}

// 渲染分页
function renderPagination(containerId, pageInfo, loadFunc) {
    const container = document.getElementById(containerId);
    const totalPage = Math.ceil(pageInfo.total / pageInfo.size) || 1;
    
    let html = `<span class="page-total">共 ${pageInfo.total} 条</span>`;
    html += `<button onclick="${loadFunc}(${pageInfo.page - 1})" ${pageInfo.page <= 1 ? "disabled" : ""}>上一页</button>`;
    
    // 简化页码，最多显示7页
    let start = Math.max(1, pageInfo.page - 3);
    let end = Math.min(totalPage, start + 6);
    if (end - start < 6) start = Math.max(1, end - 6);
    
    for (let i = start; i <= end; i++) {
        html += `<button class="${i === pageInfo.page ? 'active' : ''}" onclick="${loadFunc}(${i})">${i}</button>`;
    }
    
    html += `<button onclick="${loadFunc}(${pageInfo.page + 1})" ${pageInfo.page >= totalPage ? "disabled" : ""}>下一页</button>`;
    container.innerHTML = html;
}

// 格式化日期
function formatDate(dateStr) {
    if (!dateStr) return "-";
    return new Date(dateStr).toLocaleDateString("zh-CN");
}

// 格式化金额
function formatMoney(money) {
    return "¥" + Number(money).toFixed(2);
}