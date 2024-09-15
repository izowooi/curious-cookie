import 'package:firebase_database/firebase_database.dart';
import 'package:Curious_Cookie/model/question_model.dart';
import 'package:Curious_Cookie/model/script_model.dart';

class QuestionManager {
  final DatabaseReference _questionRef = FirebaseDatabase.instance.ref('question_db');
  static final QuestionManager _instance = QuestionManager._internal();

  final List<QuestionModel> _questions = [];
  List<QuestionModel> get questions => _questions;

  final List<ScriptModel> _scripts = [];
  List<ScriptModel> get scripts => _scripts;

  factory QuestionManager() {
      return _instance;
  }

  QuestionManager._internal();

  Future<void> initialize() async {
    DataSnapshot snapshot = await _questionRef.get();
    if (snapshot.exists) {
      try {
        List<dynamic> data = List<dynamic>.from(snapshot.value as List);
        data.forEach((element) {
          if (element == null) {
            return;
          }
          QuestionModel question = QuestionModel.fromJson(element);
          _questions.add(question);
        });
        
        print("Parsed _questions: ${_questions.length}");
      } catch (e) {
        print("Error parsing data: $e");
      }
    } else {
      print("Snapshot does not exist.");
    }
  }

  List<String> getQuestions() {
    return _questions.map((e) => e.question).toList();
  }

  List<String> getImageUrls() {
    return [
      "assets/000011_mommy_1.png",
      "assets/000012_mommy_1.png",
      "assets/000013_mommy_1.png",
      "assets/000014_mommy_1.png",
      "assets/000015_mommy_1.png"
    ];
  }
}