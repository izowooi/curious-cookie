from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

OPEN_AI_API_KEY = os.getenv('OPEN_AI_API_KEY')
print(OPEN_AI_API_KEY)

client = OpenAI(api_key=OPEN_AI_API_KEY)


def run_conversation(single_article):
    # Step 1: send the conversation and available functions to the model

    messages = [{"role": "user", "content": single_article}]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "generate_questions_from_article",
                "description": "You are the parent of a 7-year-old child."
                               "Answer the following questions from your child's perspective in korean."
                               "The answers to the questions are accompanied by illustrations."
                               "You need to write a prompt to create the illustration and a script to accompany it."
                               "The script should be written as if a parent is giving instructions to their child."
                               "The prompt for the illustration should not include any artistic style."
                               "Scenes should be 10-12 shots in total."
                               "Please write the prompts in English and the script in Korean.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "scripts": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "script": {
                                        "type": "string",
                                        "description": "Sentences to explain to your child"
                                    }
                                },
                                "required": ["script"]
                            }
                        },
                        "prompts": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "prompt": {
                                        "type": "string",
                                        "description": "Prompts for illustrations to create each scene"
                                    }
                                },
                                "required": ["prompt"]
                            }
                        },
                        "category": {
                            "type": "string",
                            "description": "Category of question (ex. politics, economy, social, math, ). If there are more than two, separate them with ,"
                        }
                    },
                    "required": [
                        "scripts",
                        "prompts",
                        "category"
                    ]
                },
            },
        }
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )
    response_message = response.choices[0].message
    ret = []
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            if tool_call.function:
                arguments = tool_call.function.arguments
                ret.append(arguments)
                print(arguments)
                #{"scripts":[{"script":"무지개는 빛이 물방울에 들어가서 여러 색으로 나누어질 때 생겨나. 빛이 물방울 안에서 휘어지고 반사되어서 우리가 보는 다양한 색깔들이 나타나지."},{"script":"햇빛이 비추는 날, 비가 오고 난 후에 하늘을 보면 무지개를 볼 수 있어. 이때 물방울과 햇빛이 만나는 상황이 중요해."},{"script":"무지개는 보통 7개의 색으로 나뉘어져 있어. 빨강, 주황, 노루, 초록, 파랑, 남색, 보라 색이 모두 무지개에서 찾아볼 수 있어."},{"script":"무지개는 구름과 비가 있던 하늘에서만 나타나는 특별한 현상이야. 모든 조건이 맞아야만 무지개를 볼 수 있어."},{"script":"무지개를 볼 수 있는 위치와 각도도 중요해. 내가 서 있는 위치에 따라서 무지개의 모양이나 색이 조금씩 달라질 수 있어."}],"prompts":[{"prompt":"A bright sunny day with a rain shower in the background where a rainbow begins to appear in the sky."},{"prompt":"A close-up of sunlight shining through a raindrop, illustrating how light bends and refracts."},{"prompt":"An illustration showing the seven colors of the rainbow, labeled: red, orange, yellow, green, blue, indigo, violet."},{"prompt":"A scenic view of a sky with clouds and rainbows, indicating special weather conditions."},{"prompt":"A child standing at different positions, looking at how the rainbow changes color and shape from various angles."}],"category":"nature, science"}
    return ret


question = "공룡은 왜 멸종했나요?"
print(run_conversation(question))
#['{"scripts":[{"script":"무지개는 빛이 물방울에 들어가서 여러 색으로 나누어질 때 생겨나. 빛이 물방울 안에서 휘어지고 반사되어서 우리가 보는 다양한 색깔들이 나타나지."},{"script":"햇빛이 비추는 날, 비가 오고 난 후에 하늘을 보면 무지개를 볼 수 있어. 이때 물방울과 햇빛이 만나는 상황이 중요해."},{"script":"무지개는 보통 7개의 색으로 나뉘어져 있어. 빨강, 주황, 노루, 초록, 파랑, 남색, 보라 색이 모두 무지개에서 찾아볼 수 있어."},{"script":"무지개는 구름과 비가 있던 하늘에서만 나타나는 특별한 현상이야. 모든 조건이 맞아야만 무지개를 볼 수 있어."},{"script":"무지개를 볼 수 있는 위치와 각도도 중요해. 내가 서 있는 위치에 따라서 무지개의 모양이나 색이 조금씩 달라질 수 있어."}],"prompts":[{"prompt":"A bright sunny day with a rain shower in the background where a rainbow begins to appear in the sky."},{"prompt":"A close-up of sunlight shining through a raindrop, illustrating how light bends and refracts."},{"prompt":"An illustration showing the seven colors of the rainbow, labeled: red, orange, yellow, green, blue, indigo, violet."},{"prompt":"A scenic view of a sky with clouds and rainbows, indicating special weather conditions."},{"prompt":"A child standing at different positions, looking at how the rainbow changes color and shape from various angles."}],"category":"nature, science"}']