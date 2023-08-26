// Assuming you have a logout button or link with an ID "logout-button"
const logoutButton = document.getElementById('logout-button');

logoutButton.addEventListener('click', async () => {
  try {
    const response = await axios.get('/api/logout'); // Change the URL to your logout endpoint
    console.log(response.data); // Assuming the response contains logout success data
    // Redirect the user to the login page or any other appropriate page
    window.location.href = '/login'; // Replace with the correct URL
  } catch (error) {
    console.error(error);
    // Handle error cases here
  }
});