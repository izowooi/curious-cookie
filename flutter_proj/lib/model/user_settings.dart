class UserSettings {
  final String style;
  final String quizId;
  final String language;
  final double fontSize;

  UserSettings({
    required this.style,
    required this.quizId,
    required this.language,
    required this.fontSize,
  });

  UserSettings copyWith({
    String? style,
    String? quizId,
    String? language,
    double? fontSize,
  }) {
    return UserSettings(
      style: style ?? this.style,
      quizId: quizId ?? this.quizId,
      language: language ?? this.language,
      fontSize: fontSize ?? this.fontSize,
    );
  }
}