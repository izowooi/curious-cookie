# -*- coding: utf-8 -*-
from openai import OpenAI
import json


class OpenAIChatbot:
    MODEL_NAME = 'gpt-4o-mini'

    def __init__(self, openai_api_key):
        self.client = OpenAI(api_key=openai_api_key)

    def run_conversation(self, single_article):
        system_message = {
            "role": "system",
            "content": (
                "You are an assistant that helps create a 10-12 cutscene explanation for young children, ages 5 to 7. "
                "The explanations should be written in Korean as if a parent is talking to their child, using simple and clear language "
                "that is easy for a young child to understand. Each cutscene should contain a brief sentence or two that describes "
                "what is happening, using short and easy-to-understand words. "
                "The illustration prompts should be written in English and describe simple and friendly images that help support the explanations. "
                "Illustrations should be engaging but not complex, focusing on bright colors and clear shapes."
            )
        }

        user_message = {
            "role": "user",
            "content": single_article
        }

        # Combine messages
        messages = [system_message, user_message]

        #messages = [{"role": "user", "content": single_article}]
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "generate_scripts_with_illustrations_for_children",
                    "description": "Generates a series of 10-12 cutscenes with simple Korean sentences and English illustration prompts for children aged 5 to 7. The sentences should be written as if a parent is explaining a concept to their child, using easy-to-understand language, while the illustration prompts should describe simple and engaging visuals to accompany the sentences.",
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
                                        },
                                        "prompt": {
                                            "type": "string",
                                            "description": "Prompts for illustrations to create each scene"
                                        },
                                    },
                                    "required": ["script"]
                                }
                            },
                            "category": {
                                "type": "string",
                                "description": "Category of question (ex. politics, economy, social, math, ). If there are more than two, separate them with ,"
                            }
                        },
                        "required": [
                            "scripts",
                            "category"
                        ]
                    },
                },
            }
        ]
        response = self.client.chat.completions.create(
            model=self.MODEL_NAME,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )
        response_message = response.choices[0].message
        ret = []
        if response_message.tool_calls:
            for tool_call in response_message.tool_calls:
                if tool_call.function:
                    arguments = tool_call.function.arguments
                    ret.append(arguments)
                    #print(arguments)
                    #{"scripts":[{"script":"무지개는 빛이 물방울에 들어가서 여러 색으로 나누어질 때 생겨나. 빛이 물방울 안에서 휘어지고 반사되어서 우리가 보는 다양한 색깔들이 나타나지."},{"script":"햇빛이 비추는 날, 비가 오고 난 후에 하늘을 보면 무지개를 볼 수 있어. 이때 물방울과 햇빛이 만나는 상황이 중요해."},{"script":"무지개는 보통 7개의 색으로 나뉘어져 있어. 빨강, 주황, 노루, 초록, 파랑, 남색, 보라 색이 모두 무지개에서 찾아볼 수 있어."},{"script":"무지개는 구름과 비가 있던 하늘에서만 나타나는 특별한 현상이야. 모든 조건이 맞아야만 무지개를 볼 수 있어."},{"script":"무지개를 볼 수 있는 위치와 각도도 중요해. 내가 서 있는 위치에 따라서 무지개의 모양이나 색이 조금씩 달라질 수 있어."}],"prompts":[{"prompt":"A bright sunny day with a rain shower in the background where a rainbow begins to appear in the sky."},{"prompt":"A close-up of sunlight shining through a raindrop, illustrating how light bends and refracts."},{"prompt":"An illustration showing the seven colors of the rainbow, labeled: red, orange, yellow, green, blue, indigo, violet."},{"prompt":"A scenic view of a sky with clouds and rainbows, indicating special weather conditions."},{"prompt":"A child standing at different positions, looking at how the rainbow changes color and shape from various angles."}],"category":"nature, science"}
                    #{"scripts":[{"script":"한때 지구에는 공룡이 살았어요. 공룡은 매우 크고 무서운 동물들이었어요.","prompt":"A friendly dinosaur in a bright green landscape with colorful trees and flowers."},{"script":"하지만 아주 오랜 시간이 지나서, 큰 사건이 있었어요. 하늘에서 큰 돌이 떨어졌지요.","prompt":"A bright, cartoonish meteor streaking through a blue sky towards Earth."},{"script":"이 큰 돌이 땅에 떨어지자, 큰 폭발이 일어났어요. 불과 연기가 가득했어요.","prompt":"A colorful explosion with bright flames and colorful smoke in the sky."},{"script":"그 이후에 하늘이 어두워지고, 햇빛이 잘 들어오지 않았어요.","prompt":"A dark sky with clouds blocking out the sunlight and a sad-looking dinosaur beneath."},{"script":"식물들이 잘 자라지 못해서, 공룡들은 먹을 것이 없어졌어요.","prompt":"A dry landscape with wilted plants and a hungry dinosaur looking sad."},{"script":"공룡들은 점점 약해지고, 결국 더 이상 살아남지 못했어요.","prompt":"A sad dinosaur sitting down with a few other small dinosaurs around."},{"script":"과학자들은 이것을 멸종이라고 불러요. 많은 공룡들이 없어졌지요.","prompt":"A friendly scientist looking through a magnifying glass at a dinosaur fossil."},{"script":"하지만 공룡의 냄새는 아직도 남아 있어요! 새들이 공룡의 후손이에요.","prompt":"A happy colorful bird sitting on a branch with a bright background."},{"script":"우리 주위에서도 공룡의 흔적을 볼 수 있어요. 재미있지요?","prompt":"A playful child looking at dinosaur footprints in the mud."},{"script":"공룡에 대한 이야기들은 언제나 흥미로워요! 다음에 또 이야기해 볼까요?","prompt":"A family gathered around reading a dinosaur book with bright illustrations."}],"category":"natural history"}
                    #{"scripts":[{"script":"꿈은 우리의 생각과 기억이 모여서 생기는 것이야. 잠을 자면서 꿈을 꾸게 돼.","prompt":"A playful bedroom scene with a child sleeping in a colorful bed, surrounded by stars and dream clouds."},{"script":"꿈은 우리가 하고 싶은 것들을 보여줘. 내가 좋아하는 것들을 꿈에서 만날 수 있어.","prompt":"A bright dream world with a child flying with balloons, meeting friendly animals, and playing with toys."},{"script":"때로는 꿈이 조금 이상할 수도 있어. 이상한 꿈은 상상력이 풍부하다는 뜻이야.","prompt":"A fun and whimsical scene with strange, colorful creatures and unusual landscapes."},{"script":"꿈은 우리에게 이야기를 들려주기도 해. 마치 영화를 보는 것처럼 느낄 수 있어.","prompt":"A magical movie theater scene with a child watching a big screen showing animated adventures."},{"script":"모두들 다르게 꿈을 꿔. 친구의 꿈은 나와 다를 수 있어.","prompt":"A scene with diverse children lying down, each with unique dream bubbles showing different themes."},{"script":"좋은 꿈을 꾸면 기분이 좋아져. 나쁜 꿈은 피하고 싶지.","prompt":"A cheerful sun shining over a child smiling, with a dark cloud representing a bad dream far away."},{"script":"꿈은 우리의 마음속 깊은 곳에서 나오는 거야. 꿈을 꿀 때 기분이 어떤지 느껴봐.","prompt":"A serene landscape with a child sitting peacefully, surrounded by soft colors reflecting different emotions."},{"script":"우리가 꿈을 꾸는 동안 우리의 뇌가 열심히 일해. 여러 가지 생각을 정리하고 있어.","prompt":"An animated brain character working, surrounded by ideas and memories floating around."},{"script":"꿈은 때로는 우리가 겪은 일이나 느낀 것을 바꿔놓기도 해. 마법처럼 변할 수 있어.","prompt":"A magical transformation scene where everyday objects change into fantastical elements."},{"script":"그래서 다음에 꿈을 꿀 때, 무엇이 나올지 기대해봐! 새로운 모험이 기다리고 있어.","prompt":"A child opening a big door with light shining through, hinting at a new adventure ahead."}],"category":"imagination, dreams"}
        return ret

    def run_conversation_test(self, question):
        print(f"Running conversation test()->{question}");
        ret = ['{"scripts":[{"script":"무지개는 구름과 비가 있던 하늘에서만 나타나는 특별한 현상이야. 모든 조건이 맞아야만 무지개를 볼 수 있어."},{"script":"무지개를 볼 수 있는 위치와 각도도 중요해. 내가 서 있는 위치에 따라서 무지개의 모양이나 색이 조금씩 달라질 수 있어."}],"prompts":[{"prompt":"A scenic view of a sky with clouds and rainbows, indicating special weather conditions."},{"prompt":"A child standing at different positions, looking at how the rainbow changes color and shape from various angles."}],"category":"nature, science"}']
        return ret

    def generate_script(self, question):
        response = self.run_conversation_test(question)

        if len(response) > 0:
            response_data = response[0]
            print(response_data)
        else:
            return None, None, None

        parsed_data = json.loads(response_data)

        script_list = [item['script'] for item in parsed_data['scripts']]
        prompt_list = [item['prompt'] for item in parsed_data['prompts']]
        category = parsed_data['category'].split(', ')

        return script_list, prompt_list, category
