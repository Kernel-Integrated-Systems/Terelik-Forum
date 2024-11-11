document.getElementById("message-form").addEventListener("submit", async function (event) {
    event.preventDefault();

    const formData = new FormData(this);
    const response = await fetch("/messages", {
        method: "POST",
        body: new URLSearchParams(formData),
    });

    if (response.ok) {
        // Reload the chat messages
        location.reload();
    } else {
        console.error("Error sending message");
    }
});
