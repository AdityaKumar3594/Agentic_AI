from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel


# 1. Prompt Template
prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple words"
)

# 2. Model
model = ChatMistralAI(model="mistral-small-2506")

# 3. Output Parser
parser = StrOutputParser()

short_prompt= ChatPromptTemplate.from_template(
    "Explain {topic} in simple words in less than 50 words"
)

long_prompt= ChatPromptTemplate.from_template(
    "Explain {topic} in simple words in more than 200 words"
)


chain = RunnableParallel({
    "short": RunnableLambda(lambda x: x['short']) | short_prompt | model | parser,
    "long": RunnableLambda(lambda x: x['long']) | long_prompt | model | parser
})

result = chain.invoke({"short": {"topic": "AI & ML"}, "long": {"topic": "NLP"}})
print(result["short"])
print("=="*100)
print(result["long"])
