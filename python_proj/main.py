from upload_script import FBManger
from generate_scripts import OpenAIChatbot
from generate_illustration import MidjourneyBot
import os
from dotenv import load_dotenv
import time


load_dotenv()

open_ai_api_key = os.getenv('OPEN_AI_API_KEY')
firebase_admin_key = os.getenv('FIREBASE_ADMIN_KEY')
firebase_db_url = os.getenv('FIREBASE_DB_URL')
discord_channel_id = os.getenv('DISCORD_CHANNEL_ID')
discord_user_token = os.getenv('DISCORD_USER_TOKEN')

fb_manager = FBManger(firebase_admin_key, firebase_db_url)
openai_chat_bot = OpenAIChatbot(open_ai_api_key)
midjourney_bot = MidjourneyBot(discord_channel_id, discord_user_token)


def main():
    start_time = gen_script_time = time.time()

    question_dict = fb_manager.get_no_script_from_db()

    for question_id, question_text in question_dict.items():
        print(f'question_id: {question_id}, question_text: {question_text}')
        script_dict, prompt_list, category = openai_chat_bot.generate_script(question_text)
        fb_manager.append_script_list_to_db(question_id, script_dict, prompt_list)
        fb_manager.set_generated_script(question_id)

        gen_script_time = time.time()
    gen_illustration()
    #gen_illustration_url()
    gen_illustration_time = time.time()
    #todo:일러스트 만든 후에 디비에 저장하는 코드 추가

    print(f'gen_script_time: {gen_script_time - start_time}')
    print(f'gen_illustration_time: {gen_illustration_time - gen_script_time}')
    # 6개의 이미지 ( 4개는 업스케일 ) 80초 정도 소요됨, 한 컷을 60초로 가정하면 10컷은 10분.
    # 질문 하나에 10분을 가정하면 1시간에 6개의 질문을 처리할 수 있음.
    # 미드저니 요금제가 200분을 주면 20개 정도 한달에 만들 수 있음. 몇개 못 만드네.


def test_gen_script():
    question_dict = fb_manager.get_unprocessed_questions_from_db()
    for question_id, question_text in question_dict.items():
        script_dict, prompt_list, category = openai_chat_bot.generate_script(question_text)
        fb_manager.append_script_list_to_db(question_id, script_dict, prompt_list)
        fb_manager.set_processed_question(question_id)


def gen_illustration():
    no_illustration_dict = fb_manager.get_no_illustration_from_db()

    for script_id, prompt in no_illustration_dict.items():
        print(f'script_id: {script_id}, prompt_list: {prompt}')
        midjourney_bot.generate_and_save_illustrations(script_id, prompt, 'mommy', ' Early Clean, minimalist design. vector illustration japanese --p om8joos')
        fb_manager.set_processed_script(script_id)


url_dict = {
    160: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291288971313287209/izowooi_A_happy_child_taking_a_deep_breath_on_a_sunny_day_smili_24752fff-fe97-46c4-9ce9-3ed8e27df152.png?ex=66ff8e11&is=66fe3c91&hm=607aacdcc210e73974a36e09dcc91637467e3b3eb00bef29906942053fd732af&',
    161: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291291596863705108/izowooi_A_picture_showing_kids_playing_in_the_summer_heat_with__5f39c3c3-6b6e-4eec-bf79-fb0eec431b81.png?ex=66ff9083&is=66fe3f03&hm=5d922b36eab2482d99890b82cb6729b2332ccfc76046454582a392c0023b4150&',
    162: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291291766485680200/izowooi_A_stunning_sunset_with_vibrant_red_and_orange_hues_in_t_af6c6968-d3c5-4a33-959b-6cc1dbf8f61d.png?ex=66ff90ac&is=66fe3f2c&hm=b42b0af54b8b10ae614df8a4a2eb6ac77d77385ed7fc49aa3ffc550d7fe7ddd9&',
    163: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291291920571695104/izowooi_A_colorful_garden_filled_with_singing_birds_with_the_wi_28d6a9a7-b54a-41c8-a86a-153b6b27af42.png?ex=66ff90d0&is=66fe3f50&hm=0e160909c7881d09c22bc7ee65ac42d98c07c9e845d383bd699bf9c86a543787&',
    164: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291291987558797342/izowooi_A_beautiful_sky_with_moving_white_clouds_and_bright_blu_60a5d9e1-26df-4913-8d9e-2bce972eab3d.png?ex=66ff90e0&is=66fe3f60&hm=72e908cfe13830df7021653fdf432b9222645b7815683510250d3f2766db0896&',
    165: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291292069003792436/izowooi_A_cute_cartoon_character_representing_wind_smiling_and__a2a0f1e5-d5c8-4f57-9831-8f6be27208a7.png?ex=66ff90f4&is=66fe3f74&hm=22dad865bbd1ab2def60f99a61c14854dbee7629ff2470ff1643741832c3f6b2&',
    166: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291292158560702475/izowooi_A_bright_and_cheerful_winter_scene_with_soft_fluffy_sno_955012e3-24f0-4197-99a9-0503e78ecf08.png?ex=66ff9109&is=66fe3f89&hm=e79ac6d0d46899e19639ec713c6872ae31e10887f6c3bf13003c5415d9a43fc1&',
    167: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291292216186372096/izowooi_A_sun_shining_brightly_over_a_snowy_landscape_highlight_3e65cf00-392f-4dcd-8fc6-832f9155f74d.png?ex=66ff9117&is=66fe3f97&hm=2e880854fe4d1a904f6a64d13a3f65c89caee6e0fd52094d443b01a89ed1d5bd&',
    168: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291292314467176539/izowooi_Close-up_of_unique_snowflakes_falling_showing_different_d0f5a86b-ee1e-4afc-889d-812fd41c1ac2.png?ex=66ff912e&is=66fe3fae&hm=0a7f584ecd4d9da4389d0bb1d3b879f01c7886c6274a550094d6e7a4c8bae728&',
    169: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291292368649322496/izowooi_Various_snowflakes_with_different_shapes_resting_on_a_c_40046f87-1c9b-489c-a65b-4c3e813f53ae.png?ex=66ff913b&is=66fe3fbb&hm=1ab5aa4fe7930f578206ddbba0c2e72d032e69a9122b949feb1f944a8141e1a4&',
    170: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291292407970795540/izowooi_A_child_gently_touching_the_snow_with_a_big_smile_on_th_d1380500-40fe-47c1-8424-a5d2e01f6136.png?ex=66ff9145&is=66fe3fc5&hm=10576584c6464b0f2f1c89e5cc344ffe75dfb662fd3bc2794bb04a390c39afd3&',
    171: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291297913430868059/izowooi_Children_playing_joyfully_in_the_snow_making_snowballs__99431f69-3807-4a6f-8eeb-e306484127f3.png?ex=66ff9665&is=66fe44e5&hm=154547a03b1b7f57904bcf700529991ca98a41a7d62df055a4b8ef85a0efa50d&',
    172: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291297975695572992/izowooi_A_winter_scene_showing_a_snowy_park_with_large_piles_of_b5556b59-84de-435a-be19-00fbf237ea95.png?ex=66ff9674&is=66fe44f4&hm=d7edc1e88fabf263384430106a6fd9d472a3d51e5aec1dc6674528c53d7d3e01&',
    173: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291298013360160800/izowooi_A_magical_transformation_showing_a_green_landscape_turn_e23e4cd4-5968-47b3-9a60-65b16ceeec64.png?ex=66ff967d&is=66fe44fd&hm=56d13401cf62c2e8a5783cdd6b67ba47c81da887e3618734e1948889d8f7361f&',
    174: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291298067760283668/izowooi_A_picturesque_scene_of_a_sunset_over_a_snowy_field_pain_619d0e77-db58-4903-a9a2-0b85c3bb9b4e.png?ex=66ff968a&is=66fe450a&hm=79fdf9f74e5ebb24bcd7835d3c7d5ef95f7f8d4bd5b2e9b13289740ea3e6b802&',
    175: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291298094264225833/izowooi_A_bright_blue_sky_with_fluffy_white_clouds_and_a_colorf_16e012e3-cceb-4ab0-9a71-45091a59520f.png?ex=66ff9690&is=66fe4510&hm=10d71a51bc71b5e2a22be1c8232322f5dfd594be765d9ec1ca721649f8be8593&',
    176: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291298152560721950/izowooi_A_close-up_of_an_airplane_wing_with_streams_of_air_flow_559f7e55-dfda-4192-95a5-0d570eb4c37b.png?ex=66ff969e&is=66fe451e&hm=de0888e357dbf5e7c245bb8755526136c6e7d3859e494d8ba475fdf978d96aff&',
    177: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291298236773961738/izowooi_An_airplane_zooming_through_the_sky_leaving_a_colorful__87797d23-f579-48fc-b82e-2f8c5da9f3db.png?ex=66ff96b2&is=66fe4532&hm=7043e010dad326772f37c5d38ccb2e80b9cfdcd4693b921a17ab5eea7398e077&',
    178: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291298284044030013/izowooi_The_airplanes_engines_are_glowing_and_making_noise_with_cb33bbad-ddbc-40a3-8d23-bd7579ffe1cf.png?ex=66ff96be&is=66fe453e&hm=bfdeaebd2a726dfff3f6e62ec5853f66e6086c87357a10351640b7514bdc5f71&',
    179: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291298346576642148/izowooi_A_friendly_airplane_with_big_eyes_and_a_smile_showing_o_4d0fc418-000b-4904-bb84-d439d6a5c2a0.png?ex=66ff96cc&is=66fe454c&hm=fc6de8cffb48c80e3d6fe2d9e7c34f196572a2c05035b16b013d53578fd7fb94&',
    180: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291298418064359495/izowooi_An_airplane_flying_happily_through_fluffy_clouds_with_a_c6d3b018-a219-41a8-847b-bb2326aaa9e0.png?ex=66ff96de&is=66fe455e&hm=10fa9a53be94dd84577b885679a0f3d0fde11f94a21fc2a5a5a13a1a0dd3100a&',
    181: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291298468765110312/izowooi_An_airplane_gently_landing_on_a_bright_runway._There_ar_ffc1d8ce-1b2d-420c-a7b8-f039ebda4194.png?ex=66ff96ea&is=66fe456a&hm=c69440a25a23c6808711237a26811932f453a0bea09ba715a22eb736522d7a05&',
    182: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291298520929665045/izowooi_A_big_airplane_with_open_doors_showing_happy_passengers_eb4d9367-33c8-4f49-8eee-dc60eb2b1e54.png?ex=66ff96f6&is=66fe4576&hm=f3cb8f774ffa054ca002adefcfeb4a7dbe2dd9e227e4e76e6648e3dd116085e2&',
    183: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291298599551897620/izowooi_A_world_map_with_an_airplane_flying_over_it_leaving_a_d_73770548-8018-488a-8367-25f8282564aa.png?ex=66ff9709&is=66fe4589&hm=05e79502d4c8b19ad1d6527b2f5a2519afcaaecac14851c5535a342a4a8367e9&',
    184: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291298642904223754/izowooi_A_cheerful_scene_of_kids_learning_about_airplanes_in_a__286867a3-1a5f-41f0-97a6-ef6b79af1b99.png?ex=66ff9713&is=66fe4593&hm=944eeab0e78ad8398ad67c9dc270241f3c8c90db44f43c21943160d89e98af18&',
    185: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291298691868659742/izowooi_A_bright_and_colorful_underwater_scene_with_various_fri_7114b2e5-857c-4741-b5d6-c07f47bc9fdf.png?ex=66ff971f&is=66fe459f&hm=359ef7af98dd59b507b34e526ac1513d41ac2a0d03fbb6c748ade0200725d36a&',
    186: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291298794687828078/izowooi_An_illustration_showing_a_fish_looking_sad_on_a_dry_sur_aeff4c3c-3d64-48fd-a5cf-f1ad8aa36db3.png?ex=66ff9737&is=66fe45b7&hm=86ed458749bb7cde29074d680c883029f64989d8f6e7e43b83f1b0dd5794b51f&',
    187: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291298798727069767/izowooi_A_close-up_view_of_a_colorful_fish_showing_its_gills_in_c4f3fb09-bd08-4104-9ba2-be831791086d.png?ex=66ff9738&is=66fe45b8&hm=0dd6cdd091f0c5f72259b575af4c2b8003b889fb8e9a24bd3020b4313d5a9e75&',
    188: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291298860521492544/izowooi_A_happy_fish_swimming_around_with_tasty_food_like_seawe_3f861dbc-3528-42f7-849c-e8f4cb49fc97.png?ex=66ff9747&is=66fe45c7&hm=598e2ff1ede2a0427de3b2906f6637010007254688a74da527af59350ded897b&',
    189: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291298946861498368/izowooi_A_joyful_scene_of_multiple_fish_playing_together_with_b_97183106-54b9-4875-a1d1-cfd858fa9a51.png?ex=66ff975c&is=66fe45dc&hm=9c2e11d53f6b325dc8f6cb220792cfabf4901df31a2899165f463c3a62199182&',
    190: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291298951693205575/izowooi_A_dynamic_illustration_of_a_fish_swiftly_swimming_throu_e7209f17-931c-49df-962e-751627f18f4a.png?ex=66ff975d&is=66fe45dd&hm=77bdac4e0b5d48e5f1a35dd3a084a05223ee4a8ba55e2a1390f3a2b9332cbfb8&',
    238: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291314525370585160/izowooi_A_small_green_sprout_breaking_through_the_soil_stretchi_a89f78f2-47b3-4439-9d67-f2af8566ca3b.png?ex=66ffa5de&is=66fe545e&hm=7220d6b5b796728580d38a8e4b223e722b814d722d403b68fb1f5a36d39591a9&',
    239: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291315001264705589/izowooi_The_young_plant_with_two_green_leaves_smiling_up_to_the_a02f78aa-1c05-4bb3-aeb8-0f7e6614e8bc.png?ex=66ffa64f&is=66fe54cf&hm=c1e9c1f4ba464aca6dbcc4a1fe65cd338116d01c5754dd9e80bc7b41ac80da54&',
    240: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291315058063704095/izowooi_The_plant_standing_tall_and_proud_basking_in_the_bright_35f16666-81ca-4d62-942a-225dfcbfed5c.png?ex=66ffa65d&is=66fe54dd&hm=9fdceab553381d3e7c07f68af17bc7ff264b2687774c53b9dfc9fbbdf693e511&',
    288: 'https://cdn.discordapp.com/ephemeral-attachments/1280888589214945280/1291323956162203678/izowooi_A_colorful_illustration_of_a_big_ear_with_musical_notes_93c4705e-6841-4cf2-aaf2-99a2e05c54d0.png?ex=66ffaea6&is=66fe5d26&hm=1ff4ac4e7b99c13f1c4e1b1f0ec7408e759ffe4c737cdd234288db09a2df8208&',
    289: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291324843127734307/izowooi_An_illustration_showing_different_sources_of_sound_like_dfb65a84-77be-4cf8-911c-358b9b7c15f8.png?ex=66ffaf7a&is=66fe5dfa&hm=42670447f9d8cf50f31eb68026181ae89d331852585643c63fe71650f92fa1c2&',
    290: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291324902162563105/izowooi_A_lovely_scene_of_colorful_birds_singing_on_a_tree_bran_c8ff7bed-0cf7-4e77-a49b-a36c38998675.png?ex=66ffaf88&is=66fe5e08&hm=6a4e2237b621d0431e29fe5eabed2218c07d5c4d07b95593c8f03ffccba05140&',
    340: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291335639509372958/izowooi_An_illustration_of_various_nocturnal_animals_making_dif_01782297-a31c-4f3e-b17d-089bb1af3d55.png?ex=66ffb988&is=66fe6808&hm=aebacb10bb15fbe39e0b6b449693156fdf135bc890c521c8d9e3a2ccf71d9bdd&',
    341: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291336089658986567/izowooi_A_relaxed_scene_showing_animals_enjoying_the_quietness__51d2f2b4-7482-48ed-9645-b3fcc06573b5.png?ex=66ffb9f3&is=66fe6873&hm=0370080e59dea50d1c11e626f41ad8fcff2567c99075591de807b2c8b2bed468&',
    390: 'https://cdn.discordapp.com/ephemeral-attachments/1280888589214945280/1291345378414694492/izowooi_A_warm_oven_revealing_a_golden_brown_loaf_of_bread_with_6d09576d-eca5-48dc-b45e-697c80dbe983.png?ex=66ffc29a&is=66fe711a&hm=6535cf5b77622f1fa104f3d6def2e51c0254feb268ca4e780da27ef4de90396e&',
    393: 'https://cdn.discordapp.com/ephemeral-attachments/1280888589214945280/1291346477037391992/izowooi_A_beautiful_image_showcasing_a_cut_piece_of_bread_revea_19862da6-329e-4400-8af9-f255228ba27d.png?ex=66ffc3a0&is=66fe7220&hm=b266c006eab96e5c851d5798a77397971cdd7fa3ed5f172b61633202cc4152ec&',
    394: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291347366917443604/izowooi_A_cheerful_scene_of_children_happily_enjoying_pieces_of_206a3155-496e-4a65-a07b-21d38b5ec2c2.png?ex=66ffc474&is=66fe72f4&hm=c0ad2fb38268ab1c5909de07dc8e1e0b5bd78128b5f9ee238aa857e1d221afa9&',
    395: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291347579778629703/izowooi_A_bright_globe_showing_different_weather_patterns_acros_4b10c522-63a3-47c4-9a03-34e17dfc5cdd.png?ex=66ffc4a7&is=66fe7327&hm=7d273e43acfbdfb2d6af38afa71f3d8a6c549df8499523d3f052408e8214482f&',
    396: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291347637349646427/izowooi_A_friendly_sun_shining_over_half_of_the_Earth_while_the_28fee88c-f087-4ab5-b3d7-dc16e42f8896.png?ex=66ffc4b4&is=66fe7334&hm=439cc895549d84826e116dd98ac8115b03d2bab7ff1417969d67393815ef21f9&',
    434: 'https://cdn.discordapp.com/ephemeral-attachments/1280888589214945280/1291372640765743194/izowooi_A_friendly_scene_showing_a_person_cutting_down_a_tree_i_557177cc-8124-44f3-8321-0974446bf57e.png?ex=66ffdbfe&is=66fe8a7e&hm=b65ca3eeb7faa065c0208dcfc49e2278c07b745130d4d5bc8766a68a384bc334&',
    435: 'https://cdn.discordapp.com/attachments/1280888589214945280/1291373618097291374/izowooi_A_cheerful_scene_with_small_pieces_of_wood_stacked_toge_ef9a8704-0a54-44ba-8087-28c07279fb07.png?ex=66ffdce7&is=66fe8b67&hm=716c95485db5633b1d52cb4f95e04a1f498c61f4fd097407335b48081356b655&'
}


def gen_illustration_url():
    no_illustration_dict = fb_manager.get_no_illustration_from_db()

    for script_id, prompt in no_illustration_dict.items():
        print(f'script_id: {script_id}, prompt_list: {prompt}')
        set_test = {}
        if script_id in url_dict:
            # if script_id > 435:
            #     break
            set_test['mommy'] = [url_dict[script_id]]
            midjourney_bot.save_images(script_id, set_test, 'mommy')
            fb_manager.set_processed_script(script_id)


def test_gen_illustration():
    test_script_id = 997
    test_prompt = 'A cartoonish brain with colorful thought bubbles, creating fun stories while a child sleeps peacefully in a cozy bed.'
    midjourney_bot.generate_and_save_illustrations(test_script_id, test_prompt, 'mommy', ' Early Clean, minimalist design. vector illustration japanese --p om8joos')


main()
#gen_illustration()
#test_gen_script()






