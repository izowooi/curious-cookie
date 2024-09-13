import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class StoryWidget extends ConsumerWidget {
  final String imageUrl = 'assets/000011_mommy_1.png';
  final String description = "설명을 추가하세요. 설명을 추가하세요. 설명을 추가하세요. 설명을 추가하세요. 설명을 추가하세요. 설명을 추가하세요. ";
  
  StoryWidget({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    ButtonStyle buttonStyle = ElevatedButton.styleFrom(
      minimumSize: Size(50, 50),
      shape: CircleBorder(), // 버튼을 원형으로 설정
      padding: EdgeInsets.all(12), // 버튼 크기 조정
      //foregroundColor: Colors.white,
      backgroundColor: Colors.transparent,
      shadowColor: Colors.transparent,
    );
    return Stack(
      children: [
        // 배경 이미지
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
              
            },
            style: buttonStyle,
            child: Icon(Icons.arrow_back, size: 40.0, color: Colors.black54), // 아이콘 설정
          ),
        ),        // 하단 텍스트
        Positioned(
          top: 16.0,
          right: 16.0,
          child: ElevatedButton(
            onPressed: () {
            },
            style: buttonStyle,
            child: Icon(Icons.arrow_forward, size: 40.0, color: Colors.black54), // 아이콘 설정
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
              style: TextStyle(
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