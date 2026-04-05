// ==========================
// 🔐 VERIFICAR LOGIN
// ==========================
document.addEventListener("DOMContentLoaded", () => {

    const token = localStorage.getItem("access_token");

    const currentPage = window.location.pathname;

    // Si está en chat y NO está logueado → lo mando a login
    if (currentPage.includes("chat.html") && !token) {
        window.location.href = "index.html";
    }

    // Si está logueado y entra a login/register → lo mando al chat
    if ((currentPage.includes("index.html") || currentPage.includes("register.html")) && token) {
        window.location.href = "chat.html";
    }

});


// ==========================
// 🚪 LOGOUT
// ==========================
function logout() {
    localStorage.removeItem("access_token");
    window.location.href = "index.html";
}