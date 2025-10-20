from auth_key import AUTH_KEY
# option 1
from gigachat import GigaChat
from gigachat.models import Chat
from gigachat.models.messages import Messages, MessagesRole

system_str = """Ты — чат-бот, отвечающий на запросы, как консультант компании. Запросы не всегда являются
                осмысленными или структурированными. Ответ должен быть не более 20 слов. Для ответа используй данные ниже:
                Компания "Рога и копыта" занимается разработкой инновационного программного обеспечения и искусственного интеллекта.
                Номер телефона: +7 (495) 777-77-77. Email для связи: info@rogakopyta.com. Мы работаем в Москве, 
                наш адрес: ул. Простая, д. 12. Компания предлагает корпоративные решения, AI-приложения, аналитическое ПО.
                Способы покупки: через сайт rogakopyta.com, по телефону и через менеджеров компании. Возврат: возврат возможен в течение 14 дней
                после покупки при сохранении целостности товара. Акции: сезонные скидки и акции для постоянных клиентов.
                Жалобы и предложения: отправляйте на почту feedback@rogakopyta.com, мы оперативно рассмотрим.
                На приветствие отвечай: «Чем я могу помочь? Готов ответить на ваши вопросы о компании "Рога и копыта"».
                На любые другие запросы, в том числе не являющиеся осмысленными или структурированными,
                не касающиеся перечисленных данных выше, отвечай: «Извините, я консультирую только по вопросам компании "Рога и копыта"»."""

def main():
    llm = GigaChat(
        credentials=AUTH_KEY,
        verify_ssl_certs=False,
    )
    # print("option 1: import from gigachat")
    all_messages = [Messages(role=MessagesRole.SYSTEM, content=system_str)]
    total_session_tokens = 0
    while (True):
        user_message = input("Пользователь: ")
        if (user_message == "пока"):
            break
        all_messages.append(Messages(role=MessagesRole.USER, content=user_message))
        chat = Chat(messages=all_messages)
        res = llm.chat(chat)
        ai_reply = res.choices[0].message.content
        tokens_used = res.usage.total_tokens
        all_messages.append(Messages(role=MessagesRole.ASSISTANT, content=ai_reply))
        print(f"GigaChat: {ai_reply}, tokens used: {tokens_used}")
        # print(" ")
        # print(res)
        # print(" ")
        # print(" ")
    total_session_tokens += tokens_used
    print("total session tokens: ", total_session_tokens)

if __name__ == "__main__":
    main()


# # option 2
# from langchain_gigachat.chat_models import GigaChat

# def main():
#     llm = GigaChat(
#         credentials=AUTH_KEY,
#         verify_ssl_certs=False,
#     )
#     print("option 2: import from langchain_gigachat.chat_models")
#     print(llm.invoke("Tell about yourself briefly"))

# if __name__ == "__main__":
#     main()
