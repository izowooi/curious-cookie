import 'package:firebase_database/firebase_database.dart';
import 'package:Curious_Cookie/model/script_model.dart';

class ScriptManager {
  // 현재 화풍, 퀴즈 아이디, 언어를 유저 설정 클래스에서 받아와야함.
  // 
  final DatabaseReference _questionRef = FirebaseDatabase.instance.ref('script_db');
  static final ScriptManager _instance = ScriptManager._internal();

  final List<ScriptModel> _scripts = [];
  List<ScriptModel> get scripts => _scripts;

  factory ScriptManager() {
      return _instance;
  }

  ScriptManager._internal();

  Future<void> initialize() async {
    DataSnapshot snapshot = await _questionRef.get();
    if (snapshot.exists) {
      try {
        List<dynamic> data = List<dynamic>.from(snapshot.value as List);
        for (var element in data) {
          if (element == null) {
            continue;
          }
          ScriptModel script = ScriptModel.fromJson(element);
          _scripts.add(script);
        }
        
        print("Parsed _scripts: ${_scripts.length}");
      } catch (e) {
        print("Error parsing data: $e");
      }
    } else {
      print("Snapshot does not exist.");
    }
  }

  List<String> getQuestions() {
    return _scripts.map((e) => e.scriptAR).toList();
  }

  String getIllustraionUrl(int scriptId, String paintStyle) {
    return _scripts.firstWhere((element) => element.id == scriptId).imagePath;

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