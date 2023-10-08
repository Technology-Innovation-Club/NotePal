const submitButton = document.querySelector("#submit-api-key");
const errorDiv = document.querySelector("#api-key-error");

submitButton.addEventListener("click", async () => {
  const api_key = document.querySelector("#api-key").value;
  const csrftoken = getCookie("csrftoken");
  const headers = {
    "X-CSRFToken": csrftoken,
    "Content-Type": "application/x-www-form-urlencoded",
  };
  const APIKeyDetails = {
    api_key,
  };
  try {
    const response = await axios.post("/api/note/add-api-key", APIKeyDetails, {
      headers,
    });
    const data = response.data;

    window.location.href = "/chat";
  } catch (error) {
    if (error.response && error.response.status === 400) {
      errorDiv.classList.remove("hidden");
    } else {
      console.error("Error sending question:", error);
    }
  }
});

document.querySelector("#api-key").addEventListener("input", () => {
  errorDiv.classList.add("hidden");
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
