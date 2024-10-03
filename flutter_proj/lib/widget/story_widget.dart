import 'package:Curious_Cookie/controller/script_manager.dart';
import 'package:Curious_Cookie/main.dart';
import 'package:Curious_Cookie/model/user_settings.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:Curious_Cookie/controller/user_settings_notifier.dart';
import 'package:intl/intl.dart';

class StoryWidget extends ConsumerWidget {
  
  const StoryWidget({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    var storyIndex = ref.watch(storyIndexProvider);
    final questionId = ref.watch(userSettingsProvider).questionId;
    final scripts = ScriptManager().getScripts(questionId);
    var descriptId = scripts[storyIndex].id;
    var storyMaxIndex = scripts.length - 1;
    final paintStyle = ref.watch(userSettingsProvider).style;

    var description = '';
    final language = ref.watch(userSettingsProvider).language;
    switch (language) {
      case 'kr':
        description = scripts[storyIndex].scriptKR;
        break;
      case 'en':
        description = scripts[storyIndex].scriptEN;
        break;
      case 'jp':
        description = scripts[storyIndex].scriptJP;
        break;
      case 'cn':
        description = scripts[storyIndex].scriptCN;
        break;
      case 'ar':
        description = scripts[storyIndex].scriptAR;
        break;
      default:
        description = scripts[storyIndex].scriptKR;
        break;
    }

    var formattedDescriptId = NumberFormat('000000').format(descriptId);

    var imageUrl = 'assets/$paintStyle/${formattedDescriptId}_${paintStyle}_0.jpg';
    final userSettings = ref.watch(userSettingsProvider);

    print('hello');
    
    print('Sytle: ${userSettings.style}, questionId: ${userSettings.questionId}, Language: ${userSettings.language}');

    ButtonStyle buttonStyle = ElevatedButton.styleFrom(
      minimumSize: const Size(50, 50),
      shape: const CircleBorder(), // 버튼을 원형으로 설정
      padding: const EdgeInsets.all(12), // 버튼 크기 조정
      backgroundColor: Colors.transparent,
      shadowColor: Colors.transparent,
    );

    return Stack(
      children: [
        Positioned.fill(
          child: Image.asset(
            imageUrl,
            fit: BoxFit.cover, // 이미지를 꽉 채우도록 설정
          ),
        ),
        Positioned(
          top: 16.0,
          left: 16.0,
          child: ElevatedButton(
            onPressed: () {
              storyIndex = storyIndex - 1;
              if (storyIndex < 0) {
                storyIndex = 0;
              }
              ref.read(storyIndexProvider.notifier).state = storyIndex;
            },
            style: buttonStyle,
            child: const Icon(Icons.arrow_back, size: 40.0, color: Colors.black54), // 아이콘 설정
          ),
        ),        // 하단 텍스트
        Positioned(
          top: 16.0,
          right: 16.0,
          child: ElevatedButton(
            onPressed: () {
              storyIndex = storyIndex + 1;
              if (storyIndex > storyMaxIndex) {
                storyIndex = storyMaxIndex;
              }
              ref.read(storyIndexProvider.notifier).state = storyIndex;

            },
            style: buttonStyle,
            child: const Icon(Icons.arrow_forward, size: 40.0, color: Colors.black54), // 아이콘 설정
          ),
        ),        // 하단 텍스트
        Positioned(
          bottom: 64.0, // 아래에서 위로 16.0 패딩
          left: 0,
          right: 0,
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 128.0),
            child: Text(
              description,
              style: const TextStyle(
                color: Colors.white,
                fontSize: 32.0,
                backgroundColor: Colors.black54, // 텍스트 배경을 반투명 검정색으로 설정
              ),
              textAlign: TextAlign.center,
            ),
          ),
        ),
      ],
    );
  }
}