// JSON data (Replace with your actual data)
const jsonData = {
    "questions": [
        {
            "question": "What is the value of the arithmetic expression 5 * (2 + 3)?",
            "type_of_question": "theory",
            "the_answer": "25"
        },
        {
            "question": "Which arithmetic operator is used for multiplication?",
            "type_of_question": "objective",
            "options": ["+", "-", "*", "/"],
            "the_answer": "*"
        }
    ]
};
let currentQuestionIndex = 0;
const questionsDataObject = {};

// Function to generate a theory question card
function createTheoryQuestionCard(questionData) {
    const card = document.createElement('div');
    card.className = 'space-y-3';
    card.innerHTML = `
    <div>
            <p class="text-sm text-gray-800 dark:text-white">${questionData.question}</p>
            <p id="correct-answer" class="text-green-500 hidden">The correct answer should be here</p>
            <span id="correct-badge" class=" hidden inline-flex items-center gap-1.5 py-1.5 px-3 rounded-full text-xs font-medium bg-green-500 text-white">Correct</span>
            <span id="wrong-badge" class=" inline-flex hidden items-center gap-1.5 py-1.5 px-3 rounded-full text-xs font-medium bg-red-500 text-white">Wrong</span><p class="text-green-500 hidden">${questionData.the_answer}</p>
            <div class="space-y-1.5">
                <input type="text" class="answer-input py-3 px-4 block w-full border-gray-200 rounded-md text-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400 sm:p-5" placeholder="Type your answer">
            </div>
            </div>
        `;

    return card;
}

// Function to generate an objective question card
function createObjectiveQuestionCard(questionData) {
    const card = document.createElement('div');
    card.className = 'space-y-3';
    
    const options = questionData.options.map((option) => `
            <label class="max-w-xs flex p-3 block w-full bg-white border border-gray-200 rounded-md text-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400">
                <input type="radio" name="answer" class="answer-radio shrink-0 mt-0.5 border-gray-200 rounded-full text-blue-600 pointer-events-none focus:ring-blue-500 dark:bg-gray-800 dark:border-gray-700 dark:checked:bg-blue-500 dark:checked:border-blue-500 dark:focus:ring-offset-gray-800">
                <span class="text-sm text-gray-500 ml-3 dark:text-gray-400">${option}</span>
            </label>
        `).join('');
        card.innerHTML = `
            <p class="text-sm text-gray-800 dark:text-white">${questionData.question}</p>
            <span id="correct-badge" class=" hidden inline-flex items-center gap-1.5 py-1.5 px-3 rounded-full text-xs font-medium bg-green-500 text-white">Correct</span>
            <span id="wrong-badge" class=" inline-flex hidden items-center gap-1.5 py-1.5 px-3 rounded-full text-xs font-medium bg-red-500 text-white">Wrong</span><p id="correct-answer" class="text-green-500 hidden">${questionData.the_answer}</p>
            <div class="space-y-1.5">
                <div class="grid space-y-2 options">
                    ${options}
                </div>
            </div>
        `;

    return card;
}



// Function to handle question submission
async function submitQuestion(questionCard, correctAnswer, questionType) {
    const userInput = questionCard.querySelector('.answer-input') || null;
    const userAnswer = userInput ? userInput.value.trim() : '';
    let isCorrect = false;

    if (questionType === 'theory') {
        // Check similarity for theory questions
        isCorrect = await checkSentenceSimilarity(userAnswer, correctAnswer);
    } else if (questionType === 'objective') {
        // Check user's answer against the correct answer for objective questions
        if (userAnswer === correctAnswer) {
            isCorrect = true;
        }
    }

    const correctBadge = questionCard.querySelector('#correct-badge');
    const wrongBadge = questionCard.querySelector('#wrong-badge');

    if (isCorrect) {
        correctBadge.classList.remove('hidden');
        wrongBadge.classList.add('hidden');
    } else {
        wrongBadge.classList.remove('hidden');
        correct-answer.classList.remove('hidden');
    }
}



function showQuestion(index) {
    const questionData = questionsDataObject[index];

    // Check if the questionData is defined
    if (!questionData) {
        console.error(`Question with index ${index} not found.`);
        return;
    }

    // Create and display the question card based on questionData
    let questionCard;

    if (questionData.type_of_question === 'theory') {
        questionCard = createTheoryQuestionCard(questionData);
    } else if (questionData.type_of_question === 'objective') {
        questionCard = createObjectiveQuestionCard(questionData);
    }

    const midCard = document.createElement('div');
    midCard.className = 'grow max-w-[90%] md:max-w-2xl w-full space-y-3';
    midCard.innerHTML=`
    <div>
    <!-- Card -->
    ${questionCard}
    <!-- End Card -->
    <!-- Button Group -->
          <div>
            <div class="sm:flex sm:justify-between">
              <div>
                <button type="button" class="py-2 px-3 inline-flex justify-center items-center gap-2 rounded-md border border-transparent font-semibold bg-blue-500 text-white hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all text-sm dark:focus:ring-offset-gray-800">
                  Submit
                </button>
                
              </div>

              <div class="mt-1 sm:mt-0">
                <a id="previous-button" class="text-gray-400 hover:text-blue-600 p-4 inline-flex items-center gap-2 rounded-md pointer-events-none" href="#">
                  <span aria-hidden="true">«</span>
                  <span>Previous</span>
                </a>
                <a id="next-button" class="text-gray-500 hover:text-blue-600 p-4 inline-flex items-center gap-2 rounded-md" href="#">
                  <span>Next</span>
                  <span aria-hidden="true">»</span>
                </a>
              </div>
            </div>
          </div>
          <!-- End Button Group -->
    </div>
    `
}

function initQuiz(questionsData) {

    // Convert the questionsData array into an object with indexes as keys
    questionsData.forEach((questionData, index) => {
        questionsDataObject[index] = questionData;
    });

    const totalQuestions = Object.keys(questionsDataObject).length;
    let currentQuestionIndex = 0;

    showQuestion(currentQuestionIndex);

    // Handle "Next" button click
    const nextButton = document.getElementById('next-button');
    nextButton.addEventListener('click', () => {
        if (currentQuestionIndex < totalQuestions - 1) {
            currentQuestionIndex++;
            showQuestion(currentQuestionIndex);
        }
    });

    // Handle "Previous" button click
    const previousButton = document.getElementById('previous-button');
    previousButton.addEventListener('click', () => {
        if (currentQuestionIndex > 0) {
            currentQuestionIndex--;
            showQuestion(currentQuestionIndex);
        }
    });
}

async function checkSentenceSimilarity(sentence1, sentence2) {
    // Load the Universal Sentence Encoder model.
    const model = await use.load();
  
    // Encode the input sentences.
    const embeddings = await model.embed([sentence1, sentence2]);
  
    // Calculate the cosine similarity between the embeddings.
    const similarity = tf.metrics.cosineDistance(embeddings[0], embeddings[1]).dataSync();
  
    // You can set a threshold value to determine if they are similar.
    const threshold = 0.8; // Adjust this threshold as needed.
  
    if (similarity < threshold) {
      return true;
    } else {
      return false;
    }
  }
  


// Initialize the quiz
// initQuiz(jsonData.questions);