const signupForm = document.getElementById('signup-form');

signupForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  
  const email = document.getElementById('hs-cover-with-gradient-form-email-1').value;
  console.log("email: "+email);
  const password = document.getElementById('hs-cover-with-gradient-form-password-1').value;
  console.log("password: "+password);
  const repeat_password = document.getElementById('hs-cover-with-gradient-form-confirm-password-1').value;
  
  // Check if passwords match
  if (password !== repeat_password) {
    alert('Passwords do not match');
    return;
  }
  
  const csrftoken = getCookie('csrftoken'); // Replace with your cookie name
  const headers = {
    'X-CSRFToken': csrftoken,
    'Content-Type': 'application/x-www-form-urlencoded',
  };

  const signupData = {
    email,
    password,
    repeat_password,
  };
  
  try {
    const response = await axios.post('/api/signup', signupData, { headers });
    console.log(response.data); // Assuming the response contains the user data
    // You can redirect the user to a success page or perform other actions here
    window.location.href = '/chat'; // Replace with the correct URL of the chat page
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