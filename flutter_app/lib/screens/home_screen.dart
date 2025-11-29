import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'calculation_screen.dart';
import 'data_screen.dart';
import 'statistics_screen.dart';
import 'upload_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _currentIndex = 0;

  final List<Widget> _screens = [
    const CalculationScreen(),
    const DataScreen(),
    const StatisticsScreen(),
    const UploadScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          'نموذج معدل التآكل',
          style: GoogleFonts.cairo(
            fontSize: 24,
            fontWeight: FontWeight.bold,
          ),
        ),
        centerTitle: true,
        backgroundColor: Colors.blue.shade700,
        foregroundColor: Colors.white,
        elevation: 4,
      ),
      body: _screens[_currentIndex],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _currentIndex,
        onDestinationSelected: (index) {
          setState(() {
            _currentIndex = index;
          });
        },
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.calculate),
            label: 'حساب',
          ),
          NavigationDestination(
            icon: Icon(Icons.table_chart),
            label: 'البيانات',
          ),
          NavigationDestination(
            icon: Icon(Icons.bar_chart),
            label: 'الإحصائيات',
          ),
          NavigationDestination(
            icon: Icon(Icons.upload_file),
            label: 'رفع ملف',
          ),
        ],
      ),
    );
  }
}

