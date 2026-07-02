import os
from anthropic import Anthropic

client = Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=100,
    messages=[
        {"role": "user", "content": "Dime hola en una frase corta"}
    ]
)

print(message.content[0].text)
