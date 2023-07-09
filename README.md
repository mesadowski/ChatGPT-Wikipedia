# ChatGPT-Wikipedia

Use Wikipedia to extend ChatGPT's knowledge base to include current events. It's well-known that ChatGPT knows nothing about events beyond 2021, which was the last time its training data was updated. I based this work on some tutorial code from AWS (https://aws.amazon.com/getting-started/hands-on/create-banking-bot-on-amazon-lex-v2-console/) but made a lot of changes.

This is an AWS Lambda function that can be used in combination with Amazon Lex. You'd need to configure Amazon Lex to handle a chat with a user that has 2 intents: getting the user to provide a subject they want to research on Wikipedia, and then the getting the user to provide a question they want to ask about this suject. At the end of each intent Lex calls the Lamdba code, and the Lambda determines where in the Lex chat workflow we are. It then performs the correct action: either checking for the existence of a relevant Wikipedia page, or using text from that page to ask OpenAI a question about it. The Lambda provides information back to Lex so that it can tell the user the result and react accordingly in the chat workflow, e.g., a Wikipedia page was found, or it wasn't found. 

To use this, you need to put your OpenAI API key in an environment variable in Lambda. 
