import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import '../providers/corrosion_provider.dart';

class CalculationScreen extends StatefulWidget {
  const CalculationScreen({super.key});

  @override
  State<CalculationScreen> createState() => _CalculationScreenState();
}

class _CalculationScreenState extends State<CalculationScreen> {
  static const String _otherMaterialValue = '__other__';
  static const List<String> _curatedMaterials = [
    'API 5L X65',
    'Carbon Steel',
    'Stainless Steel 316',
    'Duplex Stainless Steel',
    'Low Alloy Steel',
  ];

  final _formKey = GlobalKey<FormState>();
  final _materialController = TextEditingController();
  final _temperatureController = TextEditingController();
  final _phController = TextEditingController();
  final _naclController = TextEditingController();
  final _mediumController = TextEditingController();

  String? _selectedMaterial;
  List<String> _materials = [];

  @override
  void initState() {
    super.initState();
    _loadMaterials();
  }

  Future<void> _loadMaterials() async {
    final provider = Provider.of<CorrosionProvider>(context, listen: false);
    await provider.loadMaterials();
    setState(() {
      _materials = _mergeMaterials(provider.materials);
      if (_materials.isNotEmpty) {
        _selectedMaterial = _materials.first;
      }
    });
  }

  List<String> _mergeMaterials(List<String> apiMaterials) {
    final merged = <String>[
      ..._curatedMaterials,
      ...apiMaterials.where((item) => !_curatedMaterials.contains(item)),
      _otherMaterialValue,
    ];
    return merged;
  }

  String _selectedMaterialValue() {
    if (_selectedMaterial == _otherMaterialValue) {
      return _materialController.text.trim();
    }
    return (_selectedMaterial ?? _materialController.text).trim();
  }

  Future<void> _calculate() async {
    if (_formKey.currentState!.validate()) {
      final provider = Provider.of<CorrosionProvider>(context, listen: false);
      
      await provider.calculateCorrosionRate(
        material: _selectedMaterialValue(),
        temperature: double.parse(_temperatureController.text),
        ph: _phController.text.isNotEmpty 
            ? double.parse(_phController.text) 
            : null,
        naclPercentage: _naclController.text.isNotEmpty 
            ? double.parse(_naclController.text) 
            : null,
        medium: _mediumController.text.isNotEmpty 
            ? _mediumController.text 
            : null,
      );

      if (provider.error == null && provider.lastCalculation != null) {
        _showResultDialog(provider.lastCalculation!);
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(provider.error ?? 'حدث خطأ')),
        );
      }
    }
  }

  void _showResultDialog(calculation) {
    showDialog(
      context: context,
      builder: (context) => Dialog(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
        ),
        child: Container(
          constraints: BoxConstraints(
            maxWidth: MediaQuery.of(context).size.width * 0.9,
            maxHeight: MediaQuery.of(context).size.height * 0.8,
          ),
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Row(
                      children: [
                        Icon(
                          Icons.calculate,
                          color: Colors.blue.shade700,
                          size: 28,
                        ),
                        const SizedBox(width: 12),
                        Flexible(
                          child: Text(
                            'نتيجة الحساب',
                            style: GoogleFonts.cairo(
                              fontSize: 22,
                              fontWeight: FontWeight.bold,
                              color: Colors.grey.shade800,
                            ),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(width: 8),
                  IconButton(
                    icon: const Icon(Icons.close),
                    onPressed: () => Navigator.pop(context),
                    padding: EdgeInsets.zero,
                    constraints: const BoxConstraints(),
                  ),
                ],
              ),
              const SizedBox(height: 24),
              const Divider(),
              const SizedBox(height: 20),
              // Content - Scrollable
              Flexible(
                child: SingleChildScrollView(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // Corrosion Rate mm/yr
                      _buildResultCard(
                        icon: Icons.speed,
                        iconColor: Colors.blue,
                        title: 'معدل التآكل',
                        subtitle: 'mm/yr',
                        value: calculation.corrosionRateMmPerYr.toStringAsFixed(4),
                        valueColor: _getRateColor(calculation.corrosionRateMmPerYr),
                      ),
                      const SizedBox(height: 16),
                      // Corrosion Rate mpy
                      _buildResultCard(
                        icon: Icons.trending_up,
                        iconColor: Colors.orange,
                        title: 'معدل التآكل',
                        subtitle: 'mpy',
                        value: calculation.corrosionRateMpy.toStringAsFixed(2),
                        valueColor: _getRateColor(calculation.corrosionRateMmPerYr),
                      ),
                      const SizedBox(height: 16),
                      // Equation Used
                      Container(
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          color: Colors.grey.shade50,
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(
                            color: Colors.grey.shade200,
                            width: 1,
                          ),
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                Icon(
                                  Icons.functions,
                                  size: 20,
                                  color: Colors.grey.shade600,
                                ),
                                const SizedBox(width: 8),
                                Text(
                                  'المعادلة المستخدمة',
                                  style: GoogleFonts.cairo(
                                    fontSize: 14,
                                    fontWeight: FontWeight.w600,
                                    color: Colors.grey.shade700,
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 8),
                            Text(
                              calculation.equationUsed,
                              style: GoogleFonts.cairo(
                                fontSize: 13,
                                color: Colors.grey.shade800,
                              ),
                              maxLines: 3,
                              overflow: TextOverflow.ellipsis,
                            ),
                          ],
                        ),
                      ),
                      if (calculation.modelName != null ||
                          calculation.fitMethod != null ||
                          calculation.modelMetrics != null) ...[
                        const SizedBox(height: 16),
                        Container(
                          padding: const EdgeInsets.all(16),
                          decoration: BoxDecoration(
                            color: Colors.blue.shade50,
                            borderRadius: BorderRadius.circular(12),
                            border: Border.all(
                              color: Colors.blue.shade100,
                              width: 1,
                            ),
                          ),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Row(
                                children: [
                                  Icon(
                                    Icons.insights,
                                    size: 20,
                                    color: Colors.blue.shade700,
                                  ),
                                  const SizedBox(width: 8),
                                  Text(
                                    'معلومات النموذج',
                                    style: GoogleFonts.cairo(
                                      fontSize: 14,
                                      fontWeight: FontWeight.w600,
                                      color: Colors.blue.shade900,
                                    ),
                                  ),
                                ],
                              ),
                              if (calculation.modelName != null) ...[
                                const SizedBox(height: 10),
                                _buildInfoLine(
                                  'اسم النموذج',
                                  calculation.modelName!,
                                ),
                              ],
                              if (calculation.fitMethod != null) ...[
                                const SizedBox(height: 6),
                                _buildInfoLine(
                                  'طريقة الملاءمة',
                                  calculation.fitMethod!,
                                ),
                              ],
                              if (calculation.modelMetrics != null) ...[
                                const SizedBox(height: 10),
                                _buildInfoLine(
                                  'R² للاختبار',
                                  _formatMetric(calculation.modelMetrics!['r2']),
                                ),
                                const SizedBox(height: 6),
                                _buildInfoLine(
                                  'RMSE للاختبار',
                                  '${_formatMetric(calculation.modelMetrics!['rmse'])} mm/yr',
                                ),
                                const SizedBox(height: 6),
                                _buildInfoLine(
                                  'MAE للاختبار',
                                  '${_formatMetric(calculation.modelMetrics!['mae'])} mm/yr',
                                ),
                              ],
                            ],
                          ),
                        ),
                      ],
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 24),
              // Action Button
              SizedBox(
                width: double.infinity,
                child: ElevatedButton.icon(
                  onPressed: () => Navigator.pop(context),
                  icon: const Icon(Icons.check),
                  label: Text(
                    'حسناً',
                    style: GoogleFonts.cairo(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blue.shade700,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 14),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildResultCard({
    required IconData icon,
    required Color iconColor,
    required String title,
    required String subtitle,
    required String value,
    required Color valueColor,
  }) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: Colors.grey.shade200,
          width: 1.5,
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.grey.shade200,
            blurRadius: 4,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: iconColor.withOpacity(0.1),
              borderRadius: BorderRadius.circular(10),
            ),
            child: Icon(
              icon,
              color: iconColor,
              size: 24,
            ),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  title,
                  style: GoogleFonts.cairo(
                    fontSize: 14,
                    color: Colors.grey.shade600,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
                const SizedBox(height: 4),
                Row(
                  crossAxisAlignment: CrossAxisAlignment.baseline,
                  textBaseline: TextBaseline.alphabetic,
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Flexible(
                      child: Text(
                        value,
                        style: GoogleFonts.cairo(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: valueColor,
                        ),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                    const SizedBox(width: 6),
                    Text(
                      subtitle,
                      style: GoogleFonts.cairo(
                        fontSize: 14,
                        color: Colors.grey.shade600,
                      ),
                      maxLines: 1,
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildInfoLine(String label, String value) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Expanded(
          flex: 4,
          child: Text(
            label,
            style: GoogleFonts.cairo(
              fontSize: 13,
              fontWeight: FontWeight.w600,
              color: Colors.grey.shade700,
            ),
          ),
        ),
        const SizedBox(width: 12),
        Expanded(
          flex: 6,
          child: Text(
            value,
            style: GoogleFonts.cairo(
              fontSize: 13,
              color: Colors.grey.shade900,
            ),
            textAlign: TextAlign.end,
          ),
        ),
      ],
    );
  }

  String _formatMetric(dynamic value) {
    if (value == null) return '-';
    if (value is num) return value.toStringAsFixed(4);
    return value.toString();
  }

  Color _getRateColor(double rate) {
    if (rate < 0.1) return Colors.green.shade700;
    if (rate < 1.0) return Colors.orange.shade700;
    return Colors.red.shade700;
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<CorrosionProvider>(
      builder: (context, provider, child) {
        return SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Card(
                  elevation: 4,
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'إدخال البيانات',
                          style: GoogleFonts.cairo(
                            fontSize: 20,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 20),
                        if (_materials.isNotEmpty) ...[
                          DropdownButtonFormField<String>(
                            value: _selectedMaterial,
                            decoration: const InputDecoration(
                              labelText: 'نوع العينة',
                              border: OutlineInputBorder(),
                            ),
                            items: _materials.map((material) {
                              return DropdownMenuItem(
                                value: material,
                                child: Text(
                                  material == _otherMaterialValue
                                      ? 'أخرى (إدخال يدوي)'
                                      : material,
                                ),
                              );
                            }).toList(),
                            validator: (value) {
                              if (value == null || value.isEmpty) {
                                return 'يرجى اختيار نوع العينة';
                              }
                              return null;
                            },
                            onChanged: (value) {
                              setState(() {
                                _selectedMaterial = value;
                              });
                            },
                          ),
                          const SizedBox(height: 16),
                          if (_selectedMaterial == _otherMaterialValue) ...[
                            TextFormField(
                              controller: _materialController,
                              decoration: const InputDecoration(
                                labelText: 'أدخل نوع العينة',
                                border: OutlineInputBorder(),
                              ),
                              validator: (value) {
                                if (_selectedMaterial == _otherMaterialValue &&
                                    (value == null || value.trim().isEmpty)) {
                                  return 'يرجى إدخال نوع العينة';
                                }
                                return null;
                              },
                            ),
                            const SizedBox(height: 16),
                          ],
                        ] else ...[
                          TextFormField(
                            controller: _materialController,
                            decoration: const InputDecoration(
                              labelText: 'نوع العينة (مثال: API-5L X65, Carbon steel)',
                              border: OutlineInputBorder(),
                            ),
                            validator: (value) {
                              if (value == null || value.isEmpty) {
                                return 'يرجى إدخال نوع العينة';
                              }
                              return null;
                            },
                          ),
                          const SizedBox(height: 16),
                        ],
                        TextFormField(
                          controller: _temperatureController,
                          decoration: const InputDecoration(
                            labelText: 'درجة الحرارة (°C)',
                            border: OutlineInputBorder(),
                          ),
                          keyboardType: TextInputType.number,
                          validator: (value) {
                            if (value == null || value.isEmpty) {
                              return 'يرجى إدخال درجة الحرارة';
                            }
                            if (double.tryParse(value) == null) {
                              return 'يرجى إدخال رقم صحيح';
                            }
                            return null;
                          },
                        ),
                        const SizedBox(height: 16),
                        TextFormField(
                          controller: _phController,
                          decoration: const InputDecoration(
                            labelText: 'pH (اختياري)',
                            border: OutlineInputBorder(),
                          ),
                          keyboardType: TextInputType.number,
                          validator: (value) {
                            if (value != null && value.isNotEmpty) {
                              final ph = double.tryParse(value);
                              if (ph == null || ph < 0 || ph > 14) {
                                return 'pH يجب أن يكون بين 0 و 14';
                              }
                            }
                            return null;
                          },
                        ),
                        const SizedBox(height: 16),
                        TextFormField(
                          controller: _naclController,
                          decoration: const InputDecoration(
                            labelText: 'نسبة NaCl (%) (اختياري)',
                            border: OutlineInputBorder(),
                          ),
                          keyboardType: TextInputType.number,
                        ),
                        const SizedBox(height: 16),
                        TextFormField(
                          controller: _mediumController,
                          decoration: const InputDecoration(
                            labelText: 'الوسط (مثال: NaCl, Seawater) (اختياري)',
                            border: OutlineInputBorder(),
                          ),
                        ),
                        const SizedBox(height: 24),
                        SizedBox(
                          width: double.infinity,
                          height: 50,
                          child: ElevatedButton(
                            onPressed: provider.isLoading ? null : _calculate,
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Colors.blue.shade700,
                              foregroundColor: Colors.white,
                            ),
                            child: provider.isLoading
                                ? const CircularProgressIndicator(color: Colors.white)
                                : Text(
                                    'حساب معدل التآكل',
                                    style: GoogleFonts.cairo(
                                      fontSize: 18,
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  @override
  void dispose() {
    _materialController.dispose();
    _temperatureController.dispose();
    _phController.dispose();
    _naclController.dispose();
    _mediumController.dispose();
    super.dispose();
  }
}
