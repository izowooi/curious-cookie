import 'package:Curious_Cookie/controller/script_manager.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:Curious_Cookie/controller/question_manager.dart';
import 'package:Curious_Cookie/main.dart';

class HomeWidget extends ConsumerWidget {
  final questionManager = QuestionManager();
  final scriptManager = ScriptManager();

  HomeWidget({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final questions = questionManager.getQuestions();
    final imageUrls = questionManager.getImageUrls();
    print(
        'questions length: ${questions.length}, imageUrls length: ${imageUrls.length}');
    return Scaffold(
      appBar: AppBar(
        title: const Text('무엇이든 물어봐요'),
      ),
      body: FutureBuilder(
        future: initializeFirebase(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.done) {
            return _buildListView(ref);
          } else {
            return const Center(
              child: CircularProgressIndicator(),
            );
          }
        },
      ),
    );
  }

  Future<void> initializeFirebase() async {
    await questionManager.initialize();
    await scriptManager.initialize();
  }
  Widget _buildListView(WidgetRef ref) {
    final questions = questionManager.getQuestions();
    final questionIds = questionManager.getQuestionsIds();
    final imageUrls = questionManager.getImageUrls();
    print(
        '_buildListView questions length: ${questions.length}, imageUrls length: ${imageUrls.length}');

    return ListView.builder(
      itemCount: questions.length,
      itemBuilder: (context, index) {
        return Padding(
          padding: const EdgeInsets.symmetric(vertical: 4.0),
          child: Container(
            child: ListTile(
              // leading: Image.asset(
              //   imageUrls[index],
              //   fit: BoxFit.cover,
              // ),
              leading: Icon(Icons.star_border),
              title: Text(questions[index]),
              trailing: IconButton(
                icon: const Icon(Icons.arrow_forward),
                onPressed: () {
                  ref.read(navigationIndexProvider.notifier).state = 1;
                  ref.read(storyIndexProvider.notifier).state = 0;
                  ref.read(userSettingsProvider.notifier).updateQuestionId(questionIds[index]);
                },
              ),
            ),
          ),
        );
      },
    );
  }
}
