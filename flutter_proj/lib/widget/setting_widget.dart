import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:Curious_Cookie/main.dart';

class SettingWidget extends ConsumerWidget {
  SettingWidget({super.key});

  double _fontSize = 32.0;

  String _LocalizeStyle(String style) {
    switch (style) {
      case '2d':
        return '2D';
      case '3d':
        return '3D';
      case 'mommy':
        return '엄마';
      default:
        return 'Unknown';
    }
  }
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final userSettings = ref.watch(userSettingsProvider);

    print(
        'SettingWidget()->Sytle: ${userSettings.style}, questionId: ${userSettings.questionId}, Language: ${userSettings.language}, FontSize: ${userSettings.fontSize}');

    var textStyle = const TextStyle(fontSize: 18);
    return Scaffold(
      appBar: AppBar(
        title: const Text('설정'),
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Divider(
                color: Colors.grey, // 선 색상
                thickness: 1, // 선 두께
                indent: 0, // 왼쪽 여백
                endIndent: 0, // 오른쪽 여백
              ),
              const SizedBox(height: 32),
              // 화풍 선택
              Text('화풍 선택', style: textStyle),
              Row(
                children: [
                  ...['2d', '3d', 'mommy'].map((style) {
                    return Expanded(
                      child: RadioListTile<String>(
                        title: Text(_LocalizeStyle(style)),
                        value: style,
                        groupValue: userSettings.style,
                        onChanged: (value) {
                          ref
                              .read(userSettingsProvider.notifier)
                              .updateStyle(value!);
                        },
                      ),
                    );
                  }),
                ],
              ),
              const SizedBox(height: 32),
              Text('언어 선택', style: textStyle),
              Row(
                children: [
                  ...['kr', 'en', 'ar'].map((style) {
                    return Expanded(
                      child: RadioListTile<String>(
                        title: Text(
                          style.toUpperCase(),
                        ),
                        value: style,
                        groupValue: userSettings.language,
                        onChanged: (value) {
                          ref
                              .read(userSettingsProvider.notifier)
                              .updateLanguage(value!);
                        },
                      ),
                    );
                  }),
                ],
              ),
              Row(
                children: [
                  ...['jp', 'cn'].map((style) {
                    return Expanded(
                      child: RadioListTile<String>(
                        title: Text(
                          style.toUpperCase(),
                        ),
                        value: style,
                        groupValue: userSettings.language,
                        onChanged: (value) {
                          ref
                              .read(userSettingsProvider.notifier)
                              .updateLanguage(value!);
                        },
                      ),
                    );
                  }),
                ],
              ),
              const SizedBox(height: 32),
              Text('폰트 크기 (${userSettings.fontSize.round().toString()})',
                  style: const TextStyle(fontSize: 18)),
              Row(
                children: [
                  Expanded(
                    child: Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 0),
                      child: Slider(
                        value: userSettings.fontSize,
                        min: 32,
                        max: 128,
                        label: userSettings.fontSize.round().toString(),
                        onChanged: (value) {
                          ref
                              .read(userSettingsProvider.notifier)
                              .updateFontSize(value);
                        },
                      ),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
