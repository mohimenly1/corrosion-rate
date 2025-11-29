class CorrosionCalculation {
  final double corrosionRateMmPerYr;
  final double corrosionRateMpy;
  final String equationUsed;

  CorrosionCalculation({
    required this.corrosionRateMmPerYr,
    required this.corrosionRateMpy,
    required this.equationUsed,
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
    );
  }
}

