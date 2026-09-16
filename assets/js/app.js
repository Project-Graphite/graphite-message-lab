const form = document.querySelector("#message-form");
const list = document.querySelector("#message-list");
const template = document.querySelector("#message-template");
const bodyInput = document.querySelector("#message-body");
const characterCount = document.querySelector("#character-count");
const formStatus = document.querySelector("#form-status");
const submitButton = document.querySelector("#submit-button");

const renderMessages = (messages) => {
  list.replaceChildren();

  if (messages.length === 0) {
    const empty = document.createElement("p");
    empty.className = "rounded-2xl border border-dashed border-white/10 p-6 text-center text-sm text-slate-500";
    empty.textContent = "No messages yet. Be the first to test the stack.";
    list.append(empty);
    return;
  }

  messages.forEach((message) => {
    const card = template.content.cloneNode(true);
    card.querySelector(".message-author").textContent = message.display_name;
    card.querySelector(".message-body").textContent = message.body;

    const status = card.querySelector(".message-status");
    status.textContent = message.status;
    status.className += message.status === "processed"
      ? " bg-emerald-400/10 text-emerald-300"
      : " bg-amber-400/10 text-amber-300";

    const createdAt = new Date(message.created_at).toLocaleString();
    const details = message.word_count === null
      ? createdAt
      : `${createdAt} · ${message.word_count} word${message.word_count === 1 ? "" : "s"}`;
    card.querySelector(".message-meta").textContent = details;
    list.append(card);
  });
};

const loadMessages = async () => {
  try {
    const response = await fetch("/api/messages/", { headers: { Accept: "application/json" } });
    if (!response.ok) throw new Error("Unable to load messages");
    const data = await response.json();
    renderMessages(data.messages);
  } catch (error) {
    list.textContent = error.message;
  }
};

if (bodyInput) {
  bodyInput.addEventListener("input", () => {
    characterCount.textContent = `${bodyInput.value.length} / 500`;
  });
}

if (form) {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    submitButton.disabled = true;
    formStatus.textContent = "Sending…";

    try {
      const response = await fetch("/api/messages/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": form.querySelector("[name=csrfmiddlewaretoken]").value,
        },
        body: JSON.stringify({
          display_name: form.elements.display_name.value,
          body: form.elements.body.value,
        }),
      });
      const data = await response.json();
      if (!response.ok) {
        const firstError = Object.values(data.errors || {}).flat()[0];
        throw new Error(firstError || "The message could not be sent.");
      }

      form.reset();
      characterCount.textContent = "0 / 500";
      formStatus.textContent = "Message stored. The worker will process it shortly.";
      await loadMessages();
    } catch (error) {
      formStatus.textContent = error.message;
    } finally {
      submitButton.disabled = false;
    }
  });

  loadMessages();
  window.setInterval(loadMessages, 5000);
}
