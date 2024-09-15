class QuestionModel {
  final int id;
  final String question;
  final String category;
  final String generatedPicture;
  final String generatedScript;

  QuestionModel({
    required this.id,
    required this.question,
    required this.category,
    required this.generatedPicture,
    required this.generatedScript
  });

  factory QuestionModel.fromJson(Map<dynamic, dynamic> json) {
    return QuestionModel(
      id: json['id'],
      question: json['question'],
      category: json['category'],
      generatedPicture: json['generated_picture'],
      generatedScript: json['generated_script']
    );
  }
}