import openai

kay_settings = {
    "OPENAI_API_KEY": "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",
    "gpt_model": "gpt-3-turbo",
    # "temperature": {""}
}

dalle_settings = {
    "size": {"s": '256x256', "m": '512x512', "l": '1024x1024'},
    
}

def set_API_KEY(input):
    openai.api_key = input

def askGPT(input_prompt):
    # target  = str(input("What do you want to draw?: "))
    user_content = "Write only one sentence which is richly described and using the appropriate word to draw a picture of " + input_prompt
    
    message = [
            {'role': 'system', 'content': 'You are an expressive writer'},
            {'role': 'user', 'content': 'Write only one sentence which is richly described and using the appropriate word to draw a picture of dog'},
            {'role': 'assistant', 'content': 'The majestic German Shepherd stood tall and regal, its sleek and noble form exuding an aura of strength and loyalty, while its intelligent eyes sparkled with a deep wisdom that seemed to pierce the very essence of one\'s soul'},
            {'role': 'user', 'content': user_content},
    ]
    
    response = openai.ChatCompletion.create(
        model = kay_settings['gpt_model'],
        messages = message,
        temperature = 1.2,
    )

    reply = response['choices'][0]['message']['content']
    
    return reply

def askDALL_E(input):
    
    img_resp = openai.Image.create(
        prompt = input,
        n = 1,
        size = dalle_settings['size']['s']
    )
    
    img_url = img_resp["data"][0]["url"]
    
    return img_url