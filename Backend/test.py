from google import genai

client = genai.Client(api_key="AIzaSyCYo0UruSnc61216c0h_JsNuSPpd99050w")

for model in client.models.list():
    print(f"Model Name: {model.display_name}")
    print(f"Model Code: {model.name}")
    print(f"Input token limit: {model.input_token_limit}")
    print(f"Output token limit: {model.output_token_limit}\n")
