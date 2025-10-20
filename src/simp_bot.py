# import getpass
# import os

# try:
#     # load environment variables from .env file (requires `python-dotenv`)
#     from dotenv import load_dotenv

#     load_dotenv()
# except ImportError:
#     pass

# os.environ["LANGSMITH_TRACING"] = "true"
# if "LANGSMITH_API_KEY" not in os.environ:
#     os.environ["LANGSMITH_API_KEY"] = getpass.getpass(
#         prompt="Enter your LangSmith API key (optional): "
#     )
# if "LANGSMITH_PROJECT" not in os.environ:
#     os.environ["LANGSMITH_PROJECT"] = getpass.getpass(
#         prompt='Enter your LangSmith Project Name (default = "default"): '
#     )
#     if not os.environ.get("LANGSMITH_PROJECT"):
#         os.environ["LANGSMITH_PROJECT"] = "default"

from auth_key import AUTH_KEY
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat

def main():
    # init Chat model where LLM is GigaChat
    llm = GigaChat(
                credentials=AUTH_KEY,
                verify_ssl_certs=False,
                )
    # messages of conversation starts with System prompt
    messages = [
        SystemMessage(
            content="""Ты — чат-бот, отвечающий на запросы, как консультант компании. Запросы не всегда являются
            осмысленными или структурированными. Ответ должен быть не более 20 слов. Для ответа используй данные ниже:
            Компания "Рога и копыта" занимается разработкой инновационного программного обеспечения и искусственного интеллекта.
            Номер телефона: +7 (495) 777-77-77. Email для связи: info@rogakopyta.com. Мы работаем в Москве, 
            наш адрес: ул. Технологическая, д. 12. Компания предлагает корпоративные решения, AI-приложения, аналитическое ПО.
            Способы покупки: через сайт rogakopyta.com, по телефону и через менеджеров компании. Возврат: возврат возможен в течение 14 дней
            после покупки при сохранении целостности товара. Акции: сезонные скидки и акции для постоянных клиентов.
            Жалобы и предложения: отправляйте на почту feedback@rogakopyta.com, мы оперативно рассмотрим.
            На приветствие отвечай: «Чем я могу помочь? Готов ответить на ваши вопросы о компании "Рога и копыта"».
            На любые другие запросы, в том числе не являющиеся осмысленными или структурированными,
            не касающиеся перечисленных данных выше, отвечай: «Извините, я консультирую только по вопросам компании "Рога и копыта"»."""
        )
    ]
    total_session_tokens = 0
    while(True):
        user_input = input("Пользователь: ")
        if user_input == "пока":
            break
        messages.append(HumanMessage(content=user_input))
        res = llm.invoke(messages)
        messages.append(res)
        print(f"GigaChat: {res.content}, tokens used: {res.usage_metadata["total_tokens"]}")
        # print(" ")
        # print(messages)
        # print(" ")
        # print(" ")
        total_session_tokens += res.usage_metadata["total_tokens"]
    print("total session tokens: ", total_session_tokens)
    # Попытка вывести вывод по токенам
        # for token in llm.stream(messages):
        #     print(token.content, end="|")
        

if __name__ == "__main__":
    main()
