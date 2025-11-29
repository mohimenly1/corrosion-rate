import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:google_fonts/google_fonts.dart';
import 'providers/corrosion_provider.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => CorrosionProvider(),
      child: MaterialApp(
        title: 'نموذج معدل التآكل',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(
            seedColor: Colors.blue.shade700,
            brightness: Brightness.light,
          ),
          useMaterial3: true,
          textTheme: GoogleFonts.cairoTextTheme(),
        ),
        home: const HomeScreen(),
      ),
    );
  }
}
