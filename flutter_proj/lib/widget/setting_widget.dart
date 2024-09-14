import 'package:flutter/material.dart';

class SettingWidget extends StatefulWidget {
  @override
  _SettingWidgetState createState() => _SettingWidgetState();
}

class _SettingWidgetState extends State<SettingWidget> {
  String _selectedStyle = '2d';
  String _selectedLanguage = 'ko';
  double _fontSize = 32.0;

  @override
  Widget build(BuildContext context) {
    var textStyle = TextStyle(fontSize: 18);
    return Scaffold(
      appBar: AppBar(
        title: Text('설정'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Divider(
              color: Colors.grey, // 선 색상
              thickness: 1, // 선 두께
              indent: 0, // 왼쪽 여백
              endIndent: 0, // 오른쪽 여백
            ),
            // 화풍 선택
            Text('화풍 선택', style: textStyle),
            Row(
              children: [
                
                ...['2d', '3d', '엄마'].map((style) {
                  return Expanded(
                    child: RadioListTile<String>(
                      title: Text(style.toUpperCase()),
                      value: style,
                      groupValue: _selectedStyle,
                      onChanged: (value) {
                        setState(() {
                          _selectedStyle = value!;
                        });
                      },
                    ),
                  );
                }).toList(),
              ],
            ),
            SizedBox(height: 8),
            Text('언어 선택', style: textStyle),
            Row(
              children: [
                ...['kr', 'en', 'ar'].map((style) {
                  return Expanded(
                    child: RadioListTile<String>(
                      title: Text(style.toUpperCase(),),
                      value: style,
                      groupValue: _selectedLanguage,
                      onChanged: (value) {
                        setState(() {
                          _selectedLanguage = value!;
                        });
                      },
                    ),
                  );
                }).toList(),
              ],
            ),
            Row(
              children: [
                ...['jp', 'cn'].map((style) {
                  return Expanded(
                    child: RadioListTile<String>(
                      title: Text(style.toUpperCase(),),
                      value: style,
                      groupValue: _selectedLanguage,
                      onChanged: (value) {
                        setState(() {
                          _selectedLanguage = value!;
                        });
                      },
                    ),
                  );
                }).toList(),
              ],
            ),
            SizedBox(height: 8),
            Text('폰트 크기 (${_fontSize.round().toString()})', style: TextStyle(fontSize: 18)),
            Row(
              children: [
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 0),
                    child: Slider(
                      value: _fontSize,
                      min: 32,
                      max: 128,
                      label: _fontSize.round().toString(),
                      onChanged: (value) {
                        setState(() {
                          _fontSize = value;
                        });
                      },
                    ),
                  ),
                ),
              ],
            ),            
          ],
        ),
      ),
    );
  }
}