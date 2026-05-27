from rag import run_chat

print("Rag Ready")
while True:
    user_input = input("Enter query or press c to stop\n")
    sid = input("Get Session Id\n")
    if user_input.lower() == 'c':
        break
    else :
        prompt = f"""Question is: {user_input}. You are a helpful 
        and friendly company representative for answer user queries. 
        Answer exclusively from the supplied context.
        Do not use external knowledge."""

        response, chat = run_chat(str(user_input), sid, False)

        print(response)