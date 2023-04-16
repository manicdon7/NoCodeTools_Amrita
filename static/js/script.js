import bot from './assets/bot.svg'
import user from './assets/user.svg'

const form = document.querySelector('form')
const chatContainer = document.querySelector('#chat_container')

let loadInterval

const loader = (element) => {
  element.textContent = ''

  loadInterval = setInterval(() => {
    element.textContent += '.'

    if (element.textContent === '....') {
      element.textContent = ''
    }
  }, 300)
}

const typeText = (element, text) => {
  element.innerHTML = ''
  let index = 0

  console.log(text.length)
  console.log(index)

  let interval = setInterval(() => {
    if (index < text.length) {
      // still typing
      element.innerHTML += text.charAt(index)
      // text.chartAt gets the caracter under a specific index in the text that AI is going to return
      index++
    } else {
      clearInterval(interval)
    }
  }, 20)
}

const generateUniqueId = () => {
  const timestamp = Date.now()
  const randomNumber = Math.random()
  console.log(randomNumber)
  const hexadecimalString = randomNumber.toString(16)
  console.log(hexadecimalString)

  return `id-${timestamp}-${hexadecimalString}`
}

const chatStripe = (isAi, value, uniqueId) => {
  return `
      <div class="wrapper ${isAi && 'ai'}">
        <div class="chat">
          <div class="profile">
            <img 
              src="${isAi ? bot : user}"
              alt="${isAi ? 'bot' : 'user'}"
            />
          </div>
          <div class="message" id=${uniqueId}>${value}</div>
        </div>
      </div>
    `
}

async function handleSubmit(e) {
  e.preventDefault()

  const data = new FormData(form)

  // user's chat stripe
  chatContainer.innerHTML += chatStripe(false, data.get('prompt'))

  form.reset()

  // bot's chat stripe
  const uniqueId = generateUniqueId()
  chatContainer.innerHTML += chatStripe(true, ' ', uniqueId)

  // this is going to put the new message in view
  // scrollTop is how much it's currently scrolled
  // scrollHeight is the total height and it is surely hgiher than scrollTop, so if I put in srollTop a value of scrollHeight i'm sure that it will scroll at the bottom
  chatContainer.scrollTop = chatContainer.scrollHeight

  const messageBotDiv = document.getElementById(uniqueId)

  loader(messageBotDiv)

  // fetch data from server -> bot's response
  const response = await fetch('/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': '{{ csrf_token }}'
    },
    body: JSON.stringify({
      prompt: data.get('prompt'),
    }),
  })

  clearInterval(loadInterval)

  if(response.ok) {
    const data = await response.json()
    const parsedData = data.bot.trim() //trim removes whitespaces

    typeText(messageBotDiv, parsedData)
  } else {
    const err = await response.text()

    messageBotDiv.innnerHTML = "Something went wrong"

    alert(err)
  }
}

form.addEventListener('submit', handleSubmit)
form.addEventListener('keyup', (e) => {
  if (e.keyCode === 13) {
    handleSubmit(e)
  }
})
