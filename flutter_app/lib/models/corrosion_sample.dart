class CorrosionSample {
  final int? id;
  final String? sampleId;
  final String material;
  final String? medium;
  final double? naclPercentage;
  final double temperature;
  final double? ph;
  final double? corrosionRateMmPerYr;
  final double? corrosionRateMpy;
  final String? method;
  final String? source;
  final String? notes;

  CorrosionSample({
    this.id,
    this.sampleId,
    required this.material,
    this.medium,
    this.naclPercentage,
    required this.temperature,
    this.ph,
    this.corrosionRateMmPerYr,
    this.corrosionRateMpy,
    this.method,
    this.source,
    this.notes,
  });

  // Helper method to safely convert to double
  static double? _toDouble(dynamic value) {
    if (value == null) return null;
    if (value is double) return value;
    if (value is int) return value.toDouble();
    if (value is String) {
      final parsed = double.tryParse(value);
      return parsed;
    }
    return null;
  }

  factory CorrosionSample.fromJson(Map<String, dynamic> json) {
    return CorrosionSample(
      id: json['id'],
      sampleId: json['sample_id'],
      material: json['material'] ?? '',
      medium: json['medium'],
      naclPercentage: _toDouble(json['nacl_percentage']),
      temperature: _toDouble(json['temperature']) ?? 0.0,
      ph: _toDouble(json['ph']),
      corrosionRateMmPerYr: _toDouble(json['corrosion_rate_mm_per_yr']),
      corrosionRateMpy: _toDouble(json['corrosion_rate_mpy']),
      method: json['method'],
      source: json['source'],
      notes: json['notes'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'sample_id': sampleId,
      'material': material,
      'medium': medium,
      'nacl_percentage': naclPercentage,
      'temperature': temperature,
      'ph': ph,
      'corrosion_rate_mm_per_yr': corrosionRateMmPerYr,
      'corrosion_rate_mpy': corrosionRateMpy,
      'method': method,
      'source': source,
      'notes': notes,
    };
  }
}

