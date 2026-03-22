import 'package:flutter/foundation.dart';
import '../models/corrosion_sample.dart';
import '../models/corrosion_calculation.dart';
import '../services/api_service.dart';

class CorrosionProvider with ChangeNotifier {
  final ApiService _apiService = ApiService();

  List<CorrosionSample> _samples = [];
  CorrosionCalculation? _lastCalculation;
  Map<String, dynamic>? _statistics;
  List<String> _materials = [];
  List<String> _mediums = [];
  bool _isLoading = false;
  String? _error;

  List<CorrosionSample> get samples => _samples;
  CorrosionCalculation? get lastCalculation => _lastCalculation;
  Map<String, dynamic>? get statistics => _statistics;
  List<String> get materials => _materials;
  List<String> get mediums => _mediums;
  bool get isLoading => _isLoading;
  String? get error => _error;

  Future<void> loadSamples({
    String? material,
    double? minTemp,
    double? maxTemp,
    double? minPh,
    double? maxPh,
    String? medium,
  }) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _samples = await _apiService.getSamples(
        material: material,
        minTemp: minTemp,
        maxTemp: maxTemp,
        minPh: minPh,
        maxPh: maxPh,
        medium: medium,
      );
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> calculateCorrosionRate({
    required String material,
    required double temperature,
    double? ph,
    double? naclPercentage,
    String? medium,
  }) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _lastCalculation = await _apiService.calculateCorrosionRate(
        material: material,
        temperature: temperature,
        ph: ph,
        naclPercentage: naclPercentage,
        medium: medium,
      );
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<Map<String, dynamic>?> uploadCsv(String filePath) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await _apiService.uploadCsv(filePath);
      await loadSamples();
      return response;
    } catch (e) {
      _error = e.toString();
      return null;
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<Map<String, dynamic>?> uploadCsvFromBytes(
    List<int> bytes,
    String filename,
  ) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await _apiService.uploadCsvFromBytes(bytes, filename);
      await loadSamples();
      return response;
    } catch (e) {
      _error = e.toString();
      return null;
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> loadStatistics() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _statistics = await _apiService.getStatistics();
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> loadMaterials() async {
    try {
      _materials = await _apiService.getMaterials();
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      notifyListeners();
    }
  }

  Future<void> loadMediums() async {
    try {
      _mediums = await _apiService.getMediums();
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      notifyListeners();
    }
  }

  Future<Map<String, dynamic>?> clearDatabase() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await _apiService.clearDatabase();
      _samples = [];
      _statistics = null;
      _materials = [];
      _mediums = [];
      return response;
    } catch (e) {
      _error = e.toString();
      return null;
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
}
