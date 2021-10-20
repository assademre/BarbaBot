## What is BarbaBot

BarbaBot is a basic chatbot that uses feed-forward model. It answers questions which are associated with the patterns inside the intents.

## How to use
First of all user should have fill decent amount of intents in a json file or one can also use the provided one.

BarbaBot can already inform you about weather reports and exchange rates in some currencies as: EUR, USD, GBP, CAD, JPY, CNY, PLN, SEK, TRY, CZK. However, one should get the necessary credentials for both of these features from below websites, and then
store them in a file which is named *credentials.env*.

https://weather.visualcrossing.com (For weather reports) 

https://www.currencyconverterapi.com/ (For exchange rates).

## How it works

### Intents File
Intents file is the file which contains the database of the possible answers.The format of the file is JSON, and it is formed by three part:

•tag

•patterns

•responses

Tag  is  for  tagging  pattern  and  response  duo,  pattern  is  for  sentences,phrases, or some keywords to catch sensible words from input, and responsesis for response sentences which are used in output.  Below, you can see one of the examples of the intents.

`{
  "intents": [
    {
      "tag": "greetings",
      "patterns": [
        "hey",
        "hello",
        "hi"
      ],
      "responses": [
        "Hello!",
        "Hi!",
        "Hey!",
        "Hello there!"
      ]
    }
]}
`

### Training Model

After importing essential packages, first lemmatizer is called from NLTK (WordNetLemmatizer). Therefore, a list is created for ignored letters. Any question mark, exclamation mark, and
so on to the list are removed for not to confuse the model. Then tokenizer and lemmatizer on the intents set is used to create word sets. Next, pickle was used to create classes and words file. These files were created by using dump command. For the training part, firstly activation function and learning rate are used. For the loss function, categorical crossentropy is used. Later on, the categorical crossentropy helped system to detect accuracy and the loss. As a final step, model fit is implemented and then it is saved under the name of chatbot_model.

