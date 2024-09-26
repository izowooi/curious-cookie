// main.dart
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:Curious_Cookie/controller/user_settings_notifier.dart';
import 'package:Curious_Cookie/model/user_settings.dart';
import 'package:Curious_Cookie/widget/setting_widget.dart';
import 'package:Curious_Cookie/widget/home_widget.dart';
import 'package:Curious_Cookie/widget/story_widget.dart';

final storyIndexProvider = StateProvider<int>((ref) {
  return 0;
});

final navigationIndexProvider = StateProvider<int>((ref) {
  return 0;
});

final userSettingsProvider = StateNotifierProvider<UserSettingsNotifier, UserSettings>((ref) {
  return UserSettingsNotifier();
});

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setPreferredOrientations([DeviceOrientation.landscapeLeft, DeviceOrientation.landscapeRight])
      .then((_) {
    runApp(const ProviderScope(child: MainApp()));
  });
  
}

class MainApp extends ConsumerWidget{

  const MainApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
  final navigationIndex = ref.watch(navigationIndexProvider);
    final List<Widget> pages = [
    HomeWidget(),
    const StoryWidget(),
    SettingWidget(),
    ];
    return MaterialApp(
      title: 'Curious Cookie',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: Scaffold(
      body: Row(
        children: <Widget>[
          NavigationRail(
            selectedIndex: navigationIndex,
            onDestinationSelected: (int index) {
              ref.read(navigationIndexProvider.notifier).state = index;
            },
            labelType: NavigationRailLabelType.selected,
            destinations: const [
              NavigationRailDestination(
                icon: Icon(Icons.home),
                selectedIcon: Icon(Icons.home_filled),
                label: Text('Home'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.menu_book),
                selectedIcon: Icon(Icons.menu_book),
                label: Text('Story'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.settings),
                selectedIcon: Icon(Icons.settings),
                label: Text('Settings'),
              ),
            ],
          ),
          const VerticalDivider(thickness: 1, width: 1),
          // This is the main content.
          Expanded(
            child: pages[navigationIndex],
          )
        ],
      ),
    ),
    );
  }
}
