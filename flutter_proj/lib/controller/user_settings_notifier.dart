import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:Curious_Cookie/model/user_settings.dart';
import 'package:shared_preferences/shared_preferences.dart';

class UserSettingsNotifier extends StateNotifier<UserSettings> {
  UserSettingsNotifier() : super(UserSettings(style: '2d', quizId: '0', language: 'kr', fontSize: 32.0))
  {
    _loadFromPreferences();
  }

  Future<void> _loadFromPreferences() async {
    final prefs = await SharedPreferences.getInstance();
    final style = prefs.getString('style') ?? '2d';
    final quizId = prefs.getString('quizId') ?? '0';
    final language = prefs.getString('language') ?? 'kr';
    final fontSize = prefs.getDouble('fontSize') ?? 32.0;
    state = UserSettings(style: style, quizId: quizId, language: language, fontSize: fontSize);
  }

  Future<void> _saveToPreferences() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('style', state.style);
    await prefs.setString('quizId', state.quizId);
    await prefs.setString('language', state.language);
    await prefs.setDouble('fontSize', state.fontSize);
  }

  void updateStyle(String newStyle) {
    state = state.copyWith(style: newStyle);
    _saveToPreferences();
  }

  void updateQuizId(String newQuizId) {
    state = state.copyWith(quizId: newQuizId);
    _saveToPreferences();
  }

  void updateLanguage(String newLanguage) {
    state = state.copyWith(language: newLanguage);
    _saveToPreferences();
  }
  void updateFontSize(double newFontSize) {
    state = state.copyWith(fontSize: newFontSize);
    _saveToPreferences();
  }
}