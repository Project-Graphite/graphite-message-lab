const form = document.querySelector("#message-form");
const list = document.querySelector("#message-list");
const template = document.querySelector("#message-template");
const bodyInput = document.querySelector("#message-body");
const characterCount = document.querySelector("#character-count");
const formStatus = document.querySelector("#form-status");
const submitButton = document.querySelector("#submit-button");

const renderNotice = (text) => {
  const notice = document.createElement("p");
  notice.className = "rounded-xl border border-dashed border-line p-6 text-center text-sm text-faint";
  notice.textContent = text;
  list.replaceChildren(notice);
};

const renderMessages = (messages) => {
  list.replaceChildren();

  if (messages.length === 0) {
    renderNotice("No approved messages yet.");
    return;
  }

  messages.forEach((message) => {
    const card = template.content.cloneNode(true);
    card.querySelector(".message-author").textContent = message.display_name;
    card.querySelector(".message-body").textContent = message.body;

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
    if (!response.ok) throw new Error(response.statusText);
    const data = await response.json();
    renderMessages(data.messages);
  } catch {
    if (!list.querySelector("article")) renderNotice("Unable to load approved messages.");
  }
};

const updateSubmitLabel = () => {
  const visibility = form.elements.requested_visibility.value;
  submitButton.textContent = visibility === "public" ? "Request publication" : "Send privately";
};

bodyInput.addEventListener("input", () => {
  characterCount.textContent = `${bodyInput.value.length} / 500`;
});

form.elements.requested_visibility.forEach((input) => {
  input.addEventListener("change", updateSubmitLabel);
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  submitButton.disabled = true;
  formStatus.textContent = "Sending...";

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
        requested_visibility: form.elements.requested_visibility.value,
      }),
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      const firstError = Object.values(data.errors || {}).flat()[0];
      throw new Error(firstError || "The message could not be sent.");
    }

    form.reset();
    characterCount.textContent = "0 / 500";
    updateSubmitLabel();
    if (data.message.moderation_flagged) {
      formStatus.textContent = "Message received and kept private by the content filter.";
    } else if (data.message.publication_requested) {
      formStatus.textContent = "Message received privately and queued for publication review.";
    } else {
      formStatus.textContent = "Private message received.";
    }
  } catch (error) {
    formStatus.textContent = error.message;
  } finally {
    submitButton.disabled = false;
  }
});

loadMessages();
window.setInterval(loadMessages, 15000);
