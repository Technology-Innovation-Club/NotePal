const uploadButton = document.getElementById('upload-button');
const spinningElement = document.querySelector('.animate-spin');
const alertWrongFile = document.getElementById('alertWrongFile');
const alertExistingFile = document.getElementById('alertExistingFile');

uploadButton.addEventListener('click', async () => {
  // Get the selected file from the file input
  const fileInput = document.getElementById('file-input');
  const file = fileInput.files[0];
  
  const formData = new FormData();
  formData.append('file', file);
  
  const csrftoken = getCookie('csrftoken'); 
  const headers = {
    'X-CSRFToken': csrftoken,
  };

  try {
    // Show the spinning element while uploading
    spinningElement.classList.remove('hidden');
    
    const response = await axios.post('/api/note/upload', formData, { headers });
    console.log(response.data); // Handle success here

    // Hide the spinning element after upload is complete
    spinningElement.classList.add('hidden');
    
    const closeButton = document.querySelector('.hs-dropdown-toggle'); // Select the button using its class
    // Trigger the click event on the button
    if (closeButton) {
      closeButton.click();
    }
  } catch (error) {
    console.error(error);

    if (error.response && error.response.status === 401) {
        console.error('User not authenticated');
        // Redirect the user to the login page
        window.location.href = '/login'; 
    } else if (error.response && error.response.status === 400) {
        console.log('Displaying wrong file type alert');
        alertWrongFile.classList.remove('hidden');
    }else if (error.response && error.response.status === 409) {
      console.log('Displaying existing file alert');
        alertExistingFile.classList.remove('hidden');
        }
    }
    // Handle other error cases here
  }
);

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
