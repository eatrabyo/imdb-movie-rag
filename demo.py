from colorama import Fore, Style, init

from src.services.chat_engine import chat_engine

# Initialize colorama
init()


def demo():
    print(Fore.YELLOW + "Loading...\n\n" + Style.RESET_ALL)

    user_id = input("User id: ")
    while True:

        chat = chat_engine(user_id)
        query = input("\nEnter query (s for stop): ")
        if query in ["s", "stop"]:
            break
        print(Fore.YELLOW + f"question: {query}\n" + Style.RESET_ALL)
        response = chat.stream_chat(query)
        for token in response.response_gen:
            print(Fore.YELLOW + token + Style.RESET_ALL, end="", flush=True)

        print(Fore.YELLOW + "\n\n" + Style.RESET_ALL)


if __name__ == "__main__":
    demo()
