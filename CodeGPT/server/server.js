import express from 'express'
import * as dotenv from 'dotenv'
import cors from 'cors'
import { Configuration, OpenAIApi } from 'openai'

dotenv.config()

const configuration = new Configuration({
  apiKey: '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',
})

const openai = new OpenAIApi(configuration)

const app = express()
app.use(cors())
app.use(express.json())

app.get('/', async (req, res) => {
  res.status(200).send({
    message: 'Hello',
  })
})

app.post('/', async (req, res) => {
  try {
    console.log(req.body)
    const prompt = req.body.prompt

    const response = await openai.createCompletion({
      model: 'text-davinci-003',
      prompt: `${prompt}`,
      temperature: 0,
      max_tokens: 40, //lunghezza della risposta
      top_p: 1,
      frequency_penalty: 0.5, // 0 risponde alla stessa maniera ad una simile domanda
      presence_penalty: 0,
    })

    res.status(200).json({
      bot: response.data.choices[0].text
    })
  } catch (error) {
    console.log(error);
    res.status(500).send({ error })
  }
})


app.listen(5000, () => console.log('Server us running on port http://localhost:5000'))
