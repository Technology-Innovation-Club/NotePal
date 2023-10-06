const questionTextarea = document.querySelector('#question-area');
var chatList = document.querySelector('#chat-list');
const sendButton = document.querySelector('#send-button');
const loadingSpinner = document.querySelector('#send-loading');
const uploadButton = document.getElementById('upload-button');
const spinningElement = document.querySelector('.animate-spin');
const alertWrongFile = document.getElementById('alertWrongFile');
const alertExistingFile = document.getElementById('alertExistingFile');

// CHAT HANDLING

function convertMarkdown(content) {
  var converter = new showdown.Converter();
  var html = converter.makeHtml(content);
  console.log(html);
  
  return html;
}





// Function to send a question and update the chat list
async function sendQuestion(query) {
  const csrftoken = getCookie('csrftoken'); 
  const headers = {
    'X-CSRFToken': csrftoken,
    'Content-Type': 'application/x-www-form-urlencoded',
  };
  const queryData = {
    query,
  };
  try {
    const response = await axios.post('/api/chat/query', queryData, { headers });
    const data = response.data;

    // Create chat bubble for answer
    const answerBubble = document.createElement('li');
    answerBubble.innerHTML = `
      <!-- Chat Bubble -->
      <li class="max-w-4xl py-2 px-4 sm:px-6 lg:px-8 mx-auto flex gap-x-2 sm:gap-x-4">
        <svg class="flex-shrink-0 w-[2.375rem] h-[2.375rem] rounded-full" width="38" height="38" viewBox="0 0 38 38" fill="none" xmlns="http://www.w3.org/2000/svg">
          <!-- SVG paths for the chat bubble -->
        </svg>
        <div class="grow max-w-[90%] md:max-w-2xl w-full space-y-3">
          <!-- Card -->
          <div class="space-y-3">
            <!-- Use the Typography classes here -->
            <article class="prose sm:prose-base md:prose-lg lg:prose-xl prose-code:bg-black prose-em:font-semibold prose-slate dark:prose-invert prose-a:text-blue-600 prose-img:rounded-xl">${convertMarkdown(data)}</article>
            <div class="space-y-1.5">
              <!-- Other content if needed -->
            </div>
          </div>
          <!-- End Card -->
          <!-- Button Group -->
          <div>
            <div class="sm:flex sm:justify-between">
              <div>
                <button type="button" class="py-2 px-3 inline-flex justify-center items-center gap-x-2 rounded-full border border-transparent text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2 transition-all text-sm dark:hover:bg-slate-800 dark:hover:text-gray-400 dark:hover:border-gray-900 dark:focus:ring-gray-900 dark:focus:ring-offset-gray-800">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.666 3.888A2.25 2.25 0 0013.5 2.25h-3c-1.03 0-1.9.693-2.166 1.638m7.332 0c.055.194.084.4.084.612v0a.75.75 0 01-.75.75H9a.75.75 0 01-.75-.75v0c0-.212.03-.418.084-.612m7.332 0c.646.049 1.288.11 1.927.184 1.1.128 1.907 1.077 1.907 2.185V19.5a2.25 2.25 0 01-2.25 2.25H6.75A2.25 2.25 0 014.5 19.5V6.257c0-1.108.806-2.057 1.907-2.185a48.208 48.208 0 011.927-.184" />
              </svg>              
                  Copy
                </button>
              </div>
            </div>
          </div>
          <!-- End Button Group -->
        </div>
      </li>
      <!-- End Chat Bubble -->
    `;

    chatList.appendChild(answerBubble);
  } catch (error) {
    console.error('Error sending question:', error);
  }
}


// Add an event listener for the Enter key and the button click
questionTextarea.addEventListener('keydown', async (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    await submitQuestion();
  }
});

sendButton.addEventListener('click', async () => {
  await submitQuestion();
});

// Function to submit the question
async function submitQuestion() {
  const question = document.getElementById('question-area').value;
  console.log('the question is: '+question)
  if (question) {
    questionTextarea.value = '';
    loadingSpinner.classList.remove('hidden');
    // Create chat bubble for question and display it immediately
    const questionBubble = document.createElement('li');
    questionBubble.innerHTML = `
      <!-- Chat Bubble -->
      <div class="max-w-4xl px-4 sm:px-6 lg:px-8 mx-auto">
        <div class="max-w-2xl flex gap-x-2 sm:gap-x-4">
          <span class="flex-shrink-0 inline-flex items-center justify-center h-[2.375rem] w-[2.375rem] rounded-full bg-gray-600">
            <span class="text-sm font-medium text-white leading-none">Q</span>
          </span>

          <div class="grow mt-2 space-y-3">
            <p class="text-gray-800 dark:text-gray-200">${question}</p>
          </div>
        </div>
      </div>
      <!-- End Chat Bubble -->
    `;
    chatList.appendChild(questionBubble);
    // Scroll to the latest question-answer pair
    // chatList.scrollTop = chatList.scrollHeight;

    // Create and display the loading spinner
    // chatList.scrollTop = chatList.scrollHeight;

    try {
      await sendQuestion(question);

      // Remove the loading spinner (it should already be displayed)
      loadingSpinner.classList.add('hidden');

      // Scroll to the latest question-answer pair
      // chatList.scrollTop = chatList.scrollHeight;
    } catch (error) {
      console.error('Error sending question:', error);
      // Handle the error here, e.g., by displaying an error message to the user.
    }
  }
}

// FILE UPLOAD HANDLING
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

    // Create a chat bubble for the uploaded file
    const uploadedFileBubble = createUploadedFileBubble(file);

    // Append the chat bubble to the chat list
    chatList.appendChild(uploadedFileBubble);
    
    // Refresh the page when upload is successful
    // window.location.reload();
    const closeButton = document.querySelector('.hs-dropdown-toggle'); // Select the button using its class
    // Trigger the click event on the button
    if (closeButton) {
      closeButton.click();
    }
  } catch (error) {
    console.error(error);
    console.log("this is the error status: "+error.response.status);

    if (error.response && error.response.status === 401) {
        console.error('User not authenticated');
        // Redirect the user to the login page
        window.location.href = '/login'; 
    } else if (error.response && error.response.status === 400) {
        alertWrongFile.classList.remove('hidden');
    }else if (error.response && error.response.status === 409) {
      console.log('Displaying existing file alert');
        alertExistingFile.classList.remove('hidden');
        }
    }
    // Handle other error cases here
  }
);

function createUploadedFileBubble(file) {
  const uploadedFileBubble = document.createElement('li');
  uploadedFileBubble.innerHTML = `
    <!-- Chat Bubble -->
    <div class="max-w-4xl px-4 sm:px-6 lg:px-8 mx-auto">
      <div class="max-w-2xl flex gap-x-2 sm:gap-x-4">
        <span class="flex-shrink-0 inline-flex items-center justify-center h-[2.375rem] w-[2.375rem] rounded-full bg-gray-600">
          <span class="text-sm font-medium text-white leading-none">AZ</span>
        </span>

        <div class="grow mt-2 space-y-3">
          <p class="text-gray-800 dark:text-gray-200">${removeFileExtension(file.name)} uploaded</p>
          <ul class="flex flex-col justify-end text-start -space-y-px">
                <li class="flex items-center gap-x-2 p-3 text-sm bg-white border text-gray-800 first:rounded-t-lg first:mt-0 last:rounded-b-lg dark:bg-slate-900 dark:border-gray-700 dark:text-gray-200">
                  <div class="w-full flex justify-between truncate">
                    <span class="mr-3 flex-1 w-0 truncate">
                      ${file.name}
                    </span>
                  </div>
                </li>
              </ul>
        </div>
      </div>
    </div>
    <!-- End Chat Bubble -->
  `;
  return uploadedFileBubble;
}

function removeFileExtension(fileName) {
  // Split the file name by dot (.)
  const parts = fileName.split('.');

  // Check if there's more than one part (i.e., there's an extension)
  if (parts.length > 1) {
    // Remove the last part (the extension) and join the remaining parts
    return parts.slice(0, -1).join('.');
  }

  // If there's no extension, return the original name
  return fileName;
}


// Function to get a cookie by name
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
