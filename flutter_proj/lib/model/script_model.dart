class ScriptModel {
  final int id;
  final int questionId;
  final String imageGenerated;
  final String imagePath;
  final String prompt;
  final String scriptKR;
  final String scriptEN;
  final String scriptJP;
  final String scriptCN;
  final String scriptAR;

  ScriptModel({
    required this.id,
    required this.questionId,
    required this.imageGenerated,
    required this.imagePath,
    required this.prompt,
    required this.scriptKR,
    required this.scriptEN,
    required this.scriptJP,
    required this.scriptCN,
    required this.scriptAR
  });

  factory ScriptModel.fromJson(Map<dynamic, dynamic> json) {
    return ScriptModel(
      id: json['id'],
      questionId: json['question_id'],
      imageGenerated: json['image_generated'],
      imagePath: json['image_path'],
      prompt: json['prompt'],
      scriptKR: json['script_kr'],
      scriptEN: json['script_en'],
      scriptJP: json['script_jp'],
      scriptCN: json['script_cn'],
      scriptAR: json['script_ar']
    );
  }
}