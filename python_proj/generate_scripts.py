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
                "You are an assistant that helps create a 10-12 cutscene explanation for young children, ages 5 to 7"
                "Explanations should be written using simple, clear language in Korean, English, Chinese, Arabic and Japanese, just like a parent would talk to their child."
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
                    "description": "Generates a series of 10-12 cutscenes with simple Korean sentences and English illustration prompts for children aged 5 to 7. The sentences should be written as if a parent is explaining a concept to their child, using easy-to-understand language, while the illustration prompts should describe simple and engaging visuals to accompany the sentences. The illustration prompts should be appropriate for Midjourney. The prompt should not contain any picture styles.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "scripts": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "script_kr": {
                                            "type": "string",
                                            "description": "Sentences to explain to your child in Korean"
                                        },
                                        "script_en": {
                                            "type": "string",
                                            "description": "Sentences to explain to your child in English"
                                        },
                                        "script_cn": {
                                            "type": "string",
                                            "description": "Sentences to explain to your child in Chinese"
                                        },
                                        "script_ar": {
                                            "type": "string",
                                            "description": "Sentences to explain to your child in Arabic"
                                        },
                                        "script_jp": {
                                            "type": "string",
                                            "description": "Sentences to explain to your child in Japanese"
                                        },
                                        "prompt": {
                                            "type": "string",
                                            "description": "Midjourney Prompts for illustrations to create each scene"
                                        },
                                    },
                                    "required": ["script_kr", "script_en", "script_cn", "script_ar", "script_jp", "prompt"]
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
        return ret

    def run_conversation_test(self, question):
        print(f"Running conversation test()->{question}");
        #ret = ['{"scripts":[{"script":"무지개는 비와 해가 있을 때 생겨요.","prompt":"A bright scene showing rain falling on one side and sunshine breaking through clouds on the other side."},{"script":"먼저, 빗방울 속에서 빛이 꺾여요.","prompt":"Close-up of raindrops catching sunlight, showing how light bends inside them."},{"script":"그런 다음, 빛은 여러 색으로 나뉘어요.","prompt":"A colorful spectrum, with red, orange, yellow, green, blue, indigo, and violet, coming out of a raindrop."},{"script":"무지개는 이렇게 색깔이 하늘에 나타나요.","prompt":"A bright, arched rainbow in a blue sky with fluffy white clouds."},{"script":"무지개는 장난감처럼 보이기도 해요.","prompt":"Children playing happily under the colorful rainbow, pointing at it."},{"script":"각 색깔은 특별한 의미가 있어요.","prompt":"Happy cartoon characters standing beside each color of the rainbow, each character being a different color."},{"script":"무지개는 우리가 꿈꾸는 것 같아요.","prompt":"A dreamy landscape with children lying on grass, looking up at the rainbow."},{"script":"무지개는 환상적인 모양이에요.","prompt":"A giant rainbow with a friendly sun smiling above it."},{"script":"무지개는 아름다움을 볼 수 있는 신호에요.","prompt":"Happy animals sitting under the rainbow, feeling joyful."},{"script":"우리가 함께 보는 무지개는 더 특별해요.","prompt":"A group of friends holding hands, all looking up at the rainbow together."}],"category":"science"}']
        ret = [
            '{"scripts":[{"script":"무지개는 비와 해가 있을 때 생겨요.","prompt":"A bright scene showing rain falling on one side and sunshine breaking through clouds on the other side."},{"script":"먼저, 빗방울 속에서 빛이 꺾여요.","prompt":"Close-up of raindrops catching sunlight, showing how light bends inside them."}],"category":"science"}']
        return ret

    def generate_script(self, question):
        response = self.run_conversation(question)

        if len(response) > 0:
            response_data = response[0]
            print(response_data)
        else:
            return None, None, None

        # response_data를 파일로 저장
        with open('response_data_3.json', 'w', encoding='utf-8') as file:
            json.dump(response_data, file, ensure_ascii=False, indent=4)

        parsed_data = json.loads(response_data)

        script_kr = [item['script_kr'] for item in parsed_data['scripts']]
        script_en = [item['script_en'] for item in parsed_data['scripts']]
        script_cn = [item['script_cn'] for item in parsed_data['scripts']]
        script_ar = [item['script_ar'] for item in parsed_data['scripts']]
        script_jp = [item['script_jp'] for item in parsed_data['scripts']]

        prompt_list = [item['prompt'] for item in parsed_data['scripts']]
        category = parsed_data['category'].split(', ')

        script_list = {}
        script_list['kr'] = script_kr
        script_list['en'] = script_en
        script_list['cn'] = script_cn
        script_list['ar'] = script_ar
        script_list['jp'] = script_jp

        return script_list, prompt_list, category
