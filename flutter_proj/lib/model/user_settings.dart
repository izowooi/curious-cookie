class UserSettings {
  final String style;
  final int questionId;
  final String language;
  final double fontSize;

  UserSettings({
    required this.style,
    required this.questionId,
    required this.language,
    required this.fontSize,
  });

  UserSettings copyWith({
    String? style,
    int? questionId,
    String? language,
    double? fontSize,
  }) {
    return UserSettings(
      style: style ?? this.style,
      questionId: questionId ?? this.questionId,
      language: language ?? this.language,
      fontSize: fontSize ?? this.fontSize,
    );
  }
}