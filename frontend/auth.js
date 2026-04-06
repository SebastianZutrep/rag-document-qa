// ==========================
// LOGIN
// ==========================
const loginBtn = document.getElementById("login-btn");

if (loginBtn) {
    loginBtn.addEventListener("click", async () => {

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        if (!email || !password) {
            alert("Completa todos los campos");
            return;
        }

        try {
            const res = await fetch("http://127.0.0.1:8000/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email, password })
            });

            const data = await res.json();

            if (res.ok) {
                console.log("Login response:", data);

                // Guardar token y user_id
                localStorage.setItem("access_token", data.access_token);
                localStorage.setItem("user_id", data.user_id);

                // Redirigir
                window.location.href = "chat.html";
            } else {
                alert(data.detail || "Error al iniciar sesión");
            }

        } catch (error) {
            console.error(error);
            alert("Error de conexión");
        }
    });
}


// ==========================
// REGISTER
// ==========================
const registerBtn = document.getElementById("register-btn");

if (registerBtn) {
    registerBtn.addEventListener("click", async () => {
        const name = document.getElementById("name").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirm-password").value;

        if (!name || !email || !password || !confirmPassword) {
            alert("Completa todos los campos");
            return;
        }

        if (password !== confirmPassword) {
            alert("Las contraseñas no coinciden");
            return;
        }

        try {
            const res = await fetch("http://127.0.0.1:8000/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ name, email, password })
            });

            const data = await res.json();

            if (res.ok) {
                alert("Registro exitoso. Ahora puedes iniciar sesión.");
                window.location.href = "index.html";
            } else {
                alert(data.detail || "Error al registrarse");
            }

        } catch (error) {
            console.error(error);
            alert("Error de conexión");
        }
    });
}
