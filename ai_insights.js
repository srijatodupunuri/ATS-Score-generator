async function askATSAI() {
  const input = document.getElementById("chatQuestion");

  const question = input.value.trim();

  if (!question) {
    return;
  }

  const messages = document.getElementById("chatMessages");

  messages.innerHTML += `

        <div class="user-message">

            ${question}

        </div>

    `;

  const response = await fetch("/api/ats-chat", {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      question,
    }),
  });

  const result = await response.json();

  messages.innerHTML += `

        <div class="ai-message">

            ${result.response.replace(/\n/g, "<br>")}

        </div>

    `;

  input.value = "";

  messages.scrollTop = messages.scrollHeight;
}
