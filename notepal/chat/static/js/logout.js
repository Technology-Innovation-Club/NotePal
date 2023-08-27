// Assuming you have a logout link with an ID "logout-link"
const logoutLink = document.getElementById('logout-link');

logoutLink.addEventListener('click', async (event) => {
  event.preventDefault(); // Prevent the default link behavior

  try {
    const response = await axios.get('/api/logout'); // Change the URL to your logout endpoint
    // Redirect the user to the login page or any other appropriate page
    window.location.href = '/login'; // Replace with the correct URL
  } catch (error) {
    console.error(error);
    // Handle error cases here
  }
});
