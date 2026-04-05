document.addEventListener("DOMContentLoaded", () => {
    const sendBtn = document.getElementById("send-btn");
    const input = document.getElementById("chat-input");
    const messages = document.getElementById("chat-messages");
    const uploadBtn = document.getElementById("upload-btn");
    const fileInput = document.getElementById("pdf-upload");

    // ==========================
    // MOSTRAR MENSAJE
    // ==========================
    function addMessage(text, role) {
        const div = document.createElement("div");
        div.classList.add("message", role);
        div.innerText = text;

        messages.appendChild(div);
        messages.scrollTop = messages.scrollHeight;
    }

    // ==========================
    // ENVIAR PREGUNTA
    // ==========================
    if (sendBtn) {
        sendBtn.addEventListener("click", () => {
            console.log("Send button clicked");
            sendMessage();
        });
    }
    if (input) {
        input.addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                console.log("Enter key pressed");
                sendMessage();
            }
        });
    }

    async function sendMessage() {
        if (!input) return;
        const text = input.value.trim();

        if (!text) {
            console.log("Input is empty");
            return;
        }

        // Mostrar usuario
        addMessage(text, "user");
        input.value = "";

        const userId = localStorage.getItem("user_id");
        if (!userId) {
            addMessage("Error: user_id no encontrado en localStorage", "bot");
            return;
        }

        try {
            addMessage("Enviando pregunta...", "bot");
            const res = await fetch("http://127.0.0.1:8000/ask", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ question: text, user_id: userId })
            });

            const data = await res.json();
            console.log("Response from /ask:", data);

            addMessage(data.answer || "Sin respuesta", "bot");

        } catch (error) {
            addMessage("Error conectando con el servidor", "bot");
            console.error("Error in sendMessage:", error);
        }
    }

    // ==========================
    // SUBIR PDF
    // ==========================
    if (uploadBtn) {
        uploadBtn.addEventListener("click", async () => {
            console.log("Upload button clicked");

            const file = fileInput.files[0];
            if (!file) {
                alert("Selecciona un archivo PDF primero");
                return;
            }

            const user_id = localStorage.getItem("user_id");
            if (!user_id) {
                alert("Debes iniciar sesión primero");
                return;
            }

            const formData = new FormData();
            formData.append("file", file);
            formData.append("user_id", user_id);

            try {
                const res = await fetch("http://127.0.0.1:8000/upload", {
                    method: "POST",
                    body: formData
                });

                const data = await res.json();
                console.log("Response from /upload:", data);

                if (res.ok) {
                    addMessage("Documento subido y procesado correctamente ✅", "bot");
                } else {
                    addMessage(data.detail || "Error al subir el documento", "bot");
                }

            } catch (error) {
                console.error("Error in uploadPDF:", error);
                addMessage("Error conectando con el servidor", "bot");
            }
        });
    }

    // ==========================
    // NUEVO CHAT
    // ==========================
    const newChatBtn = document.getElementById("new-chat-btn");

    if (newChatBtn) {
        newChatBtn.addEventListener("click", () => {
            console.log("New chat button clicked");
            messages.innerHTML = `
                <div class="message bot">
                    Nuevo chat iniciado 🚀
                </div>
            `;
        });
    }

    // ==========================
    // VALIDACIÓN DE USER_ID
    // ==========================
    const user_id = localStorage.getItem("user_id");

    if (!user_id) {
        alert("Debes iniciar sesión");
        window.location.href = "index.html";
        return;
    }

    console.log("USER ID:", user_id);
});