// Get the necessary DOM elements
const questionTextarea = document.querySelector('#question-area');
const chatList = document.querySelector('#chat-list');
const sendButton = document.querySelector('#send-button');
const loadingSpinner = document.querySelector('#send-loading');

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
            <article class="prose prose-xl prose-invert">
      
            ${convertMarkdown(data)}
          </article>
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
                  <svg class="h-3.5 w-3.5" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1v-1z"/>
                    <!-- ...other paths -->
                  </svg>
                  Copy
                </button>
                <button type="button" class="py-2 px-3 inline-flex justify-center items-center gap-x-2 rounded-full border border-transparent text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2 transition-all text-sm dark:hover:bg-slate-800 dark:hover:text-gray-400 dark:hover:border-gray-900 dark:focus:ring-gray-900 dark:focus:ring-offset-gray-800">
                  <svg class="h-3.5 w-3.5" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M13.5 1a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3zM11 2.5a2.5 2.5 0 1 1 .603 1.628l-6.718 3.12a2.499 2.499 0 0 1 0 1.504l6.718 3.12a2.5 2.5 0 1 1-.488.876l-6.718-3.12a2.5 2.5 0 1 1 0-3.256l6.718-3.12A2.5 2.5 0 0 1 11 2.5zm-8.5 4a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3zm11 5.5a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3z"/>
                  </svg>
                  Share
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
    chatList.scrollTop = chatList.scrollHeight;

    // Create and display the loading spinner
    chatList.scrollTop = chatList.scrollHeight;

    try {
      await sendQuestion(question);

      // Remove the loading spinner (it should already be displayed)
      loadingSpinner.classList.add('hidden');

      // Scroll to the latest question-answer pair
      chatList.scrollTop = chatList.scrollHeight;
    } catch (error) {
      console.error('Error sending question:', error);
      // Handle the error here, e.g., by displaying an error message to the user.
    }
  }
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
