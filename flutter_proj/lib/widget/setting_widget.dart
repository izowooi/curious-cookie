import 'package:flutter/material.dart';

class SettingWidget extends StatefulWidget {
  @override
  _SettingWidgetState createState() => _SettingWidgetState();
}

class _SettingWidgetState extends State<SettingWidget> {
  String _selectedStyle = '2d';
  double _fontSize = 32.0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('설정'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 화풍 선택
            Row(
              children: [
                Text('화풍 선택', style: TextStyle(fontSize: 18)),
                Expanded(
                  child: RadioListTile<String>(
                    title: Text('2D'),
                    value: '2d',
                    groupValue: _selectedStyle,
                    onChanged: (value) {
                      setState(() {
                        _selectedStyle = value!;
                      });
                    },
                  ),
                ),
                Expanded(
                  child: RadioListTile<String>(
                    title: Text('3D'),
                    value: '3d',
                    groupValue: _selectedStyle,
                    onChanged: (value) {
                      setState(() {
                        _selectedStyle = value!;
                      });
                    },
                  ),
                ),
                Expanded(
                  child: RadioListTile<String>(
                    title: Text('엄마'),
                    value: '엄마',
                    groupValue: _selectedStyle,
                    onChanged: (value) {
                      setState(() {
                        _selectedStyle = value!;
                      });
                    },
                  ),
                ),
              ],
            ),
            SizedBox(height: 16),
            Row(
              children: [
                Text('폰트 크기', style: TextStyle(fontSize: 18)),
                  Expanded(
                    child: Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 38),
                      child: Slider(
                        value: _fontSize,
                        min: 32,
                        max: 128,
                        divisions: 20,
                        label: _fontSize.round().toString(),
                        onChanged: (value) {
                          setState(() {
                            _fontSize = value;
                          });
                        },
                      ),
                    ),
                  ),
                  Text(_fontSize.round().toString(), style: const TextStyle(fontSize: 18)
                ),
              ],
            ),            
            SizedBox(height: 16),

          ],
        ),
      ),
    );
  }
}