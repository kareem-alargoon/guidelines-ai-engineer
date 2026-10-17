from llm_client import chat, Role, LLMError

context = []

try:
    while True:
        inp = input("Enter your message>> ").strip()
        if inp == "/reset":
            context = []
            print("context is reset")
            continue
        elif inp == "":
            print("This is empty input")
            continue
        elif inp == "/history":
            print("context is: ", context)
            continue
        elif inp == "/exit":
            break
        else:
            context.append({"role": Role.USER.value, "content": inp})
            try:
                chat_result = chat(context)
            except LLMError as e:
                print(e)
                context.pop()
                continue
            print("response is: ", chat_result.text)
            print(f"in: {chat_result.input_tokens} tokens | out: {chat_result.output_tokens} tokens | {chat_result.duration_seconds:.2f} s")
            context.append({"role": Role.ASSISTANT.value, "content": chat_result.text})
except KeyboardInterrupt:
    print("\nExit Chat. Goodbye!")
