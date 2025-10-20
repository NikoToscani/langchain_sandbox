from auth_key import AUTH_KEY
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_gigachat.chat_models import GigaChat

from pydantic import BaseModel, Field

class PersonData(BaseModel):
    """Class to get structured data from the user request.
    """
    name: str = Field(description="Person's name")
    interest: str = Field(description="Person's interest")

def main():
    schema = {
        "title": "name_and_interest",
        "description": "get all properties: name, interest from user request",
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Person's name",
            },
            "interest":  {
                "type": "string",
                "description": "Person's interest",
            }
        },
        "required": ["name", "interest"],
        # "title": "joke",
        # "description": "Generate all properties: setup, punchline and rating",
        # "type": "object",
        # "properties": {
        #     "setup": {
        #         "type": "string",
        #         "description": "The setup of the joke",
        #     },
        #     "punchline": {
        #         "type": "string",
        #         "description": "The punchline to the joke",
        #     },
        #     "rating": {
        #         "type": "integer",
        #         "description": "How funny the joke is, from 1 to 10",
        #         "default": None,
        #     },
        # },
        # "required": ["setup", "punchline", "rating"],
    }
    # init Chat model with GigaChat LLM
    llm = GigaChat(
                credentials=AUTH_KEY,
                verify_ssl_certs=False,
                )
    # get Chat model with_structured_output
    structured_llm = llm.with_structured_output(PersonData)
    # messages of conversation starts with System prompt
    messages = [
        SystemMessage(
            content="""-"""
        )
    ]
    total_session_tokens = 0
    while(True):
        user_input = input("Пользователь: ")
        if user_input == "пока":
            break
        # # trial
        # res = structured_llm.invoke("I'am Mike and I like to bike")
        # print(res.name)
        # print(res.interest)
        # print(res)

        # can't handle general requests as usual
        # but return any crap perfectly structured
        # sometimes wrongly
        messages.append(HumanMessage(content=user_input))
        res = structured_llm.invoke(messages)
        messages.append(AIMessage(content=str(res)))
        print(f"GigaChat: {res}")
    #     print(f"GigaChat: {res.content}, tokens used: {res.usage_metadata["total_tokens"]}")
    #     total_session_tokens += res.usage_metadata["total_tokens"]
    # print("total session tokens: ", total_session_tokens)

if __name__ == "__main__":
    main()
