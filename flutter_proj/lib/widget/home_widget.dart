import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:Curious_Cookie/controller/question_manager.dart';
import 'package:Curious_Cookie/main.dart';

class HomeWidget extends ConsumerWidget {

  final questionManager = QuestionManager();

  HomeWidget({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final questions = questionManager.getQuestions();
    final imageUrls = questionManager.getImageUrls();

    return Scaffold(
      appBar: AppBar(
        title: const Text('무엇이든 물어봐요'),
      ),
      body: ListView.builder(
        itemCount: questions.length,
        itemBuilder: (context, index) {
            return Padding(
            padding: const EdgeInsets.symmetric(vertical: 4.0),
            child: Container(
              child: ListTile(
              leading: Image.asset(
                imageUrls[index],
                fit: BoxFit.cover,
              ),
              title: Text(questions[index]),
              trailing: IconButton(
                icon: Icon(Icons.arrow_forward),
                onPressed: () {
                ref.read(navigationIndexProvider.notifier).state = 1;
                },
              ),
              ),
            ),
          );
        },
      ),
    );    
  }
}