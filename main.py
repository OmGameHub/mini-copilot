from dotenv import load_dotenv
from openai import OpenAI
import json
from pathlib import Path

from tools import available_tools
from my_system_prompts import get_system_prompt

load_dotenv()

def main():
    client = OpenAI()

    assistant_prompt = "Hello, I'm Akash, your coding agent! How can I assist you today?"
    system_prompt = get_system_prompt()
    messages = [
        { "role": "system", "content": system_prompt },
        { "role": "assistant", "content": assistant_prompt }
    ]

    print(assistant_prompt)
    while True:
        user_query = input('> ')
        messages.append({ "role": "user", "content": user_query })

        while True:
            response = client.chat.completions.create(
                model="gpt-4o",
                response_format={"type": "json_object"},
                messages=messages
            )

            parsed_output = json.loads(response.choices[0].message.content)
            messages.append({ "role": "assistant", "content": json.dumps(parsed_output) })

            if parsed_output.get("step") == "plan":
                print(f"🧠: {parsed_output.get('content')}")
                continue

            if parsed_output.get("step") == "action":
                tool_name = parsed_output.get("function")
                tool_input = parsed_output.get("input")

                if available_tools.get(tool_name, False) != False:
                    output = available_tools[tool_name].get("fn")(tool_input)
                    messages.append({ "role": "assistant", "content": json.dumps({ "step": "observe", "output":  output}) })
                    continue

            if parsed_output.get("step") == "output":
                print(f"🤖: {parsed_output.get('content')}")
                break



if __name__ == "__main__":
    main()
