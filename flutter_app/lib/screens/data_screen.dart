import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import 'package:data_table_2/data_table_2.dart';
import '../providers/corrosion_provider.dart';

class DataScreen extends StatefulWidget {
  const DataScreen({super.key});

  @override
  State<DataScreen> createState() => _DataScreenState();
}

class _DataScreenState extends State<DataScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      Provider.of<CorrosionProvider>(context, listen: false).loadSamples();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<CorrosionProvider>(
      builder: (context, provider, child) {
        if (provider.isLoading && provider.samples.isEmpty) {
          return const Center(child: CircularProgressIndicator());
        }

        if (provider.error != null) {
          return Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(Icons.error_outline, size: 64, color: Colors.red.shade300),
                const SizedBox(height: 16),
                Text(
                  'خطأ في تحميل البيانات',
                  style: GoogleFonts.cairo(fontSize: 18),
                ),
                const SizedBox(height: 8),
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 32),
                  child: Text(
                    provider.error!,
                    style: GoogleFonts.cairo(color: Colors.grey),
                    textAlign: TextAlign.center,
                    maxLines: 5,
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  'تأكد من أن Backend يعمل وأن قاعدة البيانات موجودة',
                  style: GoogleFonts.cairo(
                    color: Colors.orange,
                    fontSize: 12,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 16),
                ElevatedButton(
                  onPressed: () => provider.loadSamples(),
                  child: const Text('إعادة المحاولة'),
                ),
              ],
            ),
          );
        }

        if (provider.samples.isEmpty) {
          return Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(Icons.table_chart_outlined, size: 64, color: Colors.grey.shade400),
                const SizedBox(height: 16),
                Text(
                  'لا توجد بيانات',
                  style: GoogleFonts.cairo(fontSize: 18, color: Colors.grey),
                ),
                const SizedBox(height: 8),
                Text(
                  'يرجى رفع ملف CSV أو إضافة بيانات',
                  style: GoogleFonts.cairo(color: Colors.grey),
                ),
              ],
            ),
          );
        }

        return Column(
          children: [
            Padding(
              padding: const EdgeInsets.all(16),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'البيانات (${provider.samples.length})',
                    style: GoogleFonts.cairo(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  IconButton(
                    icon: const Icon(Icons.refresh),
                    onPressed: () => provider.loadSamples(),
                  ),
                ],
              ),
            ),
            Expanded(
              child: SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: SingleChildScrollView(
                  child: DataTable2(
                    columnSpacing: 12,
                    horizontalMargin: 12,
                    minWidth: 1000,
                    columns: [
                      DataColumn2(
                        label: Text('ID', style: GoogleFonts.cairo(fontWeight: FontWeight.bold)),
                        size: ColumnSize.S,
                      ),
                      DataColumn2(
                        label: Text('العينة', style: GoogleFonts.cairo(fontWeight: FontWeight.bold)),
                        size: ColumnSize.L,
                      ),
                      DataColumn2(
                        label: Text('الوسط', style: GoogleFonts.cairo(fontWeight: FontWeight.bold)),
                        size: ColumnSize.L,
                      ),
                      DataColumn2(
                        label: Text('درجة الحرارة', style: GoogleFonts.cairo(fontWeight: FontWeight.bold)),
                        size: ColumnSize.M,
                      ),
                      DataColumn2(
                        label: Text('pH', style: GoogleFonts.cairo(fontWeight: FontWeight.bold)),
                        size: ColumnSize.S,
                      ),
                      DataColumn2(
                        label: Text('NaCl %', style: GoogleFonts.cairo(fontWeight: FontWeight.bold)),
                        size: ColumnSize.S,
                      ),
                      DataColumn2(
                        label: Text('معدل التآكل (mm/yr)', style: GoogleFonts.cairo(fontWeight: FontWeight.bold)),
                        size: ColumnSize.M,
                      ),
                      DataColumn2(
                        label: Text('معدل التآكل (mpy)', style: GoogleFonts.cairo(fontWeight: FontWeight.bold)),
                        size: ColumnSize.M,
                      ),
                    ],
                    rows: provider.samples.take(100).map((sample) {
                      return DataRow2(
                        cells: [
                          DataCell(Text('${sample.id ?? ''}')),
                          DataCell(Text(sample.material)),
                          DataCell(Text(sample.medium ?? '-')),
                          DataCell(Text('${sample.temperature}°C')),
                          DataCell(Text(sample.ph?.toStringAsFixed(1) ?? '-')),
                          DataCell(Text(sample.naclPercentage?.toStringAsFixed(2) ?? '-')),
                          DataCell(Text(
                            sample.corrosionRateMmPerYr?.toStringAsFixed(4) ?? '-',
                            style: TextStyle(
                              color: _getRateColor(sample.corrosionRateMmPerYr),
                              fontWeight: FontWeight.bold,
                            ),
                          )),
                          DataCell(Text(
                            sample.corrosionRateMpy?.toStringAsFixed(2) ?? '-',
                            style: TextStyle(
                              color: _getRateColor(sample.corrosionRateMmPerYr),
                              fontWeight: FontWeight.bold,
                            ),
                          )),
                        ],
                      );
                    }).toList(),
                  ),
                ),
              ),
            ),
          ],
        );
      },
    );
  }

  Color _getRateColor(double? rate) {
    if (rate == null) return Colors.grey;
    if (rate < 0.1) return Colors.green;
    if (rate < 1.0) return Colors.orange;
    return Colors.red;
  }
}

