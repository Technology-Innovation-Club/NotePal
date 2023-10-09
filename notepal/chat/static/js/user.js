
const csrftoken = getCookie("csrftoken");
const headers = {
  "X-CSRFToken": csrftoken,
};
window.addEventListener('beforeunload', function (event) {
    // Send an AJAX request to a Django view that deletes the user
    const xhr = new XMLHttpRequest();
    xhr.open('DELETE', '/chat/delete-user/', true);  // Replace with the actual URL
    xhr.send();

    if (navigator.sendBeacon) {
        const formData = new FormData();
        formData.append('delete_user', true);
    
        // Send a Beacon request to ensure the request is sent
        navigator.sendBeacon('/chat/delete-user/', formData);
      }
  });


// Function to get a cookie by name
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