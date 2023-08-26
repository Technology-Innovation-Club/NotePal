const loginForm = document.getElementById('login-form');

loginForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  
  const email = document.getElementById('hs-cover-with-gradient-form-email-1').value;
  const password = document.getElementById('hs-cover-with-gradient-form-password-1').value;
  
  const csrftoken = getCookie('csrftoken'); // Replace with your cookie name
  const headers = {
    'X-CSRFToken': csrftoken,
    'Content-Type': 'application/x-www-form-urlencoded',
  };

  const loginData = {
    email,
    password,
  };
  
  try {
    const response = await axios.post('/api/login', loginData, { headers });
    console.log(response.data); // Assuming the response contains login success data
    // You can redirect the user to a success page or perform other actions here
    window.location.href = '/chat';
  } catch (error) {
    console.error(error);

    if (error.response && error.response.data) {
        console.error('Response error:', error.response.data);
    }
    // Handle error cases here
  }
});

// Function to get a cookie by name
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
