import 'package:firebase_database/firebase_database.dart';
import 'package:Curious_Cookie/model/question_model.dart';
import 'package:Curious_Cookie/model/script_model.dart';

class QuestionManager {
  final DatabaseReference _questionRef = FirebaseDatabase.instance.ref('question_db');
  static final QuestionManager _instance = QuestionManager._internal();

  final List<QuestionModel> _questions = [];
  List<QuestionModel> get questions => _questions;

  factory QuestionManager() {
      return _instance;
  }

  QuestionManager._internal();

  Future<void> initialize() async {
    DataSnapshot snapshot = await _questionRef.get();
    if (snapshot.exists) {
      try {
        List<dynamic> data = List<dynamic>.from(snapshot.value as List);
        for (var element in data) {
          if (element == null) {
            continue;
          }
          QuestionModel question = QuestionModel.fromJson(element);
          _questions.add(question);
        }
        
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
      "assets/2d/000000_2d_0.png",
      "assets/2d/000001_2d_0.png",
      "assets/2d/000002_2d_0.png",
      "assets/2d/000003_2d_0.png",
      "assets/2d/000004_2d_0.png",
      "assets/2d/000005_2d_0.png"
    ];
  }
}