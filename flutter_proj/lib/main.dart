// main.dart
import 'package:Curious_Cookie/controller/question_manager.dart';
import 'package:Curious_Cookie/widget/setting_widget.dart';
import 'firebase_options.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:Curious_Cookie/widget/home_widget.dart';
import 'package:Curious_Cookie/widget/story_widget.dart';
import 'package:Curious_Cookie/widget/setting_widget.dart';

final navigationIndexProvider = StateProvider<int>((ref) {
  return 0;
});

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setPreferredOrientations([DeviceOrientation.landscapeLeft, DeviceOrientation.landscapeRight])
      .then((_) {
    runApp(ProviderScope(child: MainApp()));
  });
  
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );

  await QuestionManager().initialize();
}

class MainApp extends ConsumerWidget{

  MainApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final navigationIndex = ref.watch(navigationIndexProvider);
    final List<Widget> _pages = [
    HomeWidget(),
    StoryWidget(),
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
            destinations: [
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
          VerticalDivider(thickness: 1, width: 1),
          // This is the main content.
          Expanded(
            child: _pages[navigationIndex],
          )
        ],
      ),
    ),
    );
  }
}
