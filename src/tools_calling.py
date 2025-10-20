from auth_key import AUTH_KEY
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_gigachat.chat_models import GigaChat
from langchain_core.tools import tool

@tool
def my_tool_func(tool_input: str) -> str:
    """Return some string with str argument

    Args:
        tool_input: first str
    """
    return "Hello from my_tool_func with arg: " + tool_input

@tool
def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

# print(multiply)
# multiply.invoke({"a": 2, "b": 3})

# print(multiply.name) # multiply
# print(multiply.description) # Multiply two numbers.
# print(multiply.args_schema.model_json_schema())
# print(multiply.args)

def main():
    # init Chat model with GigaChat LLM
    llm = GigaChat(
                credentials=AUTH_KEY
                verify_ssl_certs=False,
                )
    llm_with_tools = llm.bind_tools([my_tool_func, multiply])
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
        messages.append(HumanMessage(content=user_input))
        res = llm_with_tools.invoke(messages)
        messages.append(res)
        if res.tool_calls:
            print("Tool_calling condition")
            # print(f"GigaChat: {res.tool_calls}, tokens used: {res.usage_metadata["total_tokens"]}")
            for tool_call in res.tool_calls:
                # Выбираем и вызываем tool
                if tool_call['name'] == 'multiply':
                    tool_res = multiply.invoke(tool_call['args'])
                elif tool_call['name'] == 'my_tool_func':
                    tool_res = my_tool_func.invoke(tool_call['args'])
                
                # Добавляем результат выполнения инструмента в историю
                tool_message = ToolMessage(
                    content=tool_res,
                    tool_call_id=tool_call["id"]
                    )
                messages.append(tool_message)
            
            print(f"GigaChat: {tool_message.content}, tokens used: {res.usage_metadata["total_tokens"]}")
        else:
            print("No tool_calling condition")
            print(f"GigaChat: {res.content}, tokens used: {res.usage_metadata["total_tokens"]}")

        total_session_tokens += res.usage_metadata["total_tokens"]
    print("total session tokens: ", total_session_tokens)
    
    # print(my_tool_func(tool_input="some_tool_arg"))        
    # print(my_tool_func.invoke({"tool_input": "some_tool_arg"}))
    # print(my_tool_func.name)
    # print(my_tool_func.description)
    # print(my_tool_func.args)
    # print(my_tool_func.args_schema.model_json_schema())

if __name__ == "__main__":
    main()
