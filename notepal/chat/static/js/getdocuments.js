async function fetchFileNames() {
  try {
    const csrftoken = getCookie('csrftoken'); 
    const headers = {
      'X-CSRFToken': csrftoken,
    };
    
    const response = await fetch('/api/note/all', { headers });
    const fileNames = await response.json();

    // Clear the existing list before adding new items
    fileList.innerHTML = '';

    // Loop through the file names and create list items
    fileNames.forEach(fileName => {
      const listItem = document.createElement('li');
      listItem.innerHTML = `
        <p class="flex items-center gap-x-3 py-2 px-3 text-sm text-slate-700 rounded-md dark:text-slate-400">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" width="16" height="16" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
          </svg>                  
          ${fileName}
        </p>
      `;

      fileList.appendChild(listItem);
    });
  } catch (error) {
    console.error('Error fetching file names:', error);
  }
}
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

fetchFileNames()