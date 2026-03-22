class CorrosionCalculation {
  final double corrosionRateMmPerYr;
  final double corrosionRateMpy;
  final String equationUsed;
  final String? modelName;
  final String? fitMethod;
  final Map<String, dynamic>? modelMetrics;

  CorrosionCalculation({
    required this.corrosionRateMmPerYr,
    required this.corrosionRateMpy,
    required this.equationUsed,
    this.modelName,
    this.fitMethod,
    this.modelMetrics,
  });

  // Helper method to safely convert to double
  static double _toDouble(dynamic value, [double defaultValue = 0.0]) {
    if (value == null) return defaultValue;
    if (value is double) return value;
    if (value is int) return value.toDouble();
    if (value is String) {
      final parsed = double.tryParse(value);
      return parsed ?? defaultValue;
    }
    return defaultValue;
  }

  factory CorrosionCalculation.fromJson(Map<String, dynamic> json) {
    return CorrosionCalculation(
      corrosionRateMmPerYr: _toDouble(json['corrosion_rate_mm_per_yr'], 0.0),
      corrosionRateMpy: _toDouble(json['corrosion_rate_mpy'], 0.0),
      equationUsed: json['equation_used'] ?? '',
      modelName: json['model_name'],
      fitMethod: json['fit_method'],
      modelMetrics: json['model_metrics'] is Map<String, dynamic>
          ? json['model_metrics']
          : (json['model_metrics'] is Map
              ? Map<String, dynamic>.from(json['model_metrics'])
              : null),
    );
  }
}
