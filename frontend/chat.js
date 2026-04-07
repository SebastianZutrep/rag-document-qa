document.addEventListener("DOMContentLoaded", () => {
    const sendBtn = document.getElementById("send-btn");
    const input = document.getElementById("chat-input");
    const messages = document.getElementById("chat-messages");
    const uploadBtn = document.getElementById("upload-btn");
    const fileInput = document.getElementById("pdf-upload");
    const fileNameDiv = document.getElementById("file-name");
 
    // VALIDACIÓN DE USER_ID
    const user_id = localStorage.getItem("user_id");
    if (!user_id) {
        alert("Debes iniciar sesión");
        window.location.href = "index.html";
        return;
    }
 
    // Mostrar nombre del archivo al seleccionarlo
    fileInput.addEventListener("change", () => {
        const file = fileInput.files[0];
        if (file) {
            fileNameDiv.textContent = file.name;
        } else {
            fileNameDiv.textContent = "";
        }
    });
 
    // MOSTRAR MENSAJE
    function addMessage(text, role) {
        const div = document.createElement("div");
        div.classList.add("message", role);
        div.innerText = text;
        messages.appendChild(div);
        messages.scrollTop = messages.scrollHeight;
    }
 
    // ENVIAR PREGUNTA
    if (sendBtn) {
        sendBtn.addEventListener("click", () => sendMessage());
    }
    if (input) {
        input.addEventListener("keypress", (e) => {
            if (e.key === "Enter") sendMessage();
        });
    }
 
    async function sendMessage() {
        if (!input) return;
        const text = input.value.trim();
        if (!text) return;
 
        addMessage(text, "user");
        input.value = "";
 
        const userId = localStorage.getItem("user_id");
        if (!userId) {
            addMessage("Error: user_id no encontrado", "bot");
            return;
        }
 
        try {
            addMessage("Pensando...", "bot");
            const res = await fetch("http://127.0.0.1:8000/ask", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question: text, user_id: userId })
            });
 
            const data = await res.json();
 
            // Reemplazar el mensaje "Pensando..." con la respuesta
            const allMessages = messages.querySelectorAll(".message.bot");
            const last = allMessages[allMessages.length - 1];
            if (last && last.innerText === "Pensando...") {
                last.innerText = data.answer || "Sin respuesta";
            } else {
                addMessage(data.answer || "Sin respuesta", "bot");
            }
 
        } catch (error) {
            addMessage("Error conectando con el servidor", "bot");
            console.error("Error in sendMessage:", error);
        }
    }
 
    // SUBIR ARCHIVO
    if (uploadBtn) {
        uploadBtn.addEventListener("click", async () => {
            const file = fileInput.files[0];
            if (!file) {
                alert("Selecciona un archivo primero");
                return;
            }
 
            const userId = localStorage.getItem("user_id");
            if (!userId) {
                alert("Debes iniciar sesión primero");
                return;
            }
 
            // Validar extensión en el frontend también
            const allowedExtensions = [".pdf", ".docx", ".doc", ".xlsx", ".xls", ".csv",
                                        ".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".webp"];
            const ext = "." + file.name.split(".").pop().toLowerCase();
            if (!allowedExtensions.includes(ext)) {
                addMessage(`Formato '${ext}' no soportado. Formatos aceptados: ${allowedExtensions.join(", ")}`, "bot");
                return;
            }
 
            addMessage(`Subiendo ${file.name}...`, "bot");
 
            const formData = new FormData();
            formData.append("file", file);
            formData.append("user_id", userId);
 
            try {
                const res = await fetch("http://127.0.0.1:8000/upload", {
                    method: "POST",
                    body: formData
                });
 
                const data = await res.json();
 
                if (res.ok) {
                    addMessage(`"${file.name}" subido y procesado. ¡Ya puedes hacer preguntas!`, "bot");
                    fileNameDiv.textContent = "";
                    fileInput.value = "";
                } else {
                    addMessage(`${data.detail || "Error al subir el archivo"}`, "bot");
                }
 
            } catch (error) {
                console.error("Error in upload:", error);
                addMessage("Error conectando con el servidor", "bot");
            }
        });
    }
 
    // NUEVO CHAT
    const newChatBtn = document.getElementById("new-chat-btn");
    if (newChatBtn) {
        newChatBtn.addEventListener("click", () => {
            messages.innerHTML = `
                <div class="message bot">
                    Hola 👋 Soy tu asistente RAG. Sube un archivo y hazme preguntas.
                </div>
            `;
        });
    }
});
