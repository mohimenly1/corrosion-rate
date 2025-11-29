import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/corrosion_sample.dart';
import '../models/corrosion_calculation.dart';

class ApiService {
  // For Android Emulator, use 10.0.2.2 to access localhost
  // For iOS Simulator or physical devices, use your computer's local IP (e.g., 192.168.0.14)
  // For web/desktop, use localhost
  // Note: Port changed to 5001 because 5000 is used by AirPlay on macOS
  static const String baseUrl = 'http://10.0.2.2:5001/api';  // Android Emulator
  
  // Uncomment and use one of these if needed:
  // static const String baseUrl = 'http://localhost:5001/api';  // Web/Desktop
  // static const String baseUrl = 'http://192.168.0.14:5001/api';  // Physical devices or iOS Simulator

  Future<List<CorrosionSample>> getSamples({
    String? material,
    double? minTemp,
    double? maxTemp,
    double? minPh,
    double? maxPh,
    String? medium,
  }) async {
    try {
      final uri = Uri.parse('$baseUrl/samples').replace(queryParameters: {
        if (material != null) 'material': material,
        if (minTemp != null) 'min_temp': minTemp.toString(),
        if (maxTemp != null) 'max_temp': maxTemp.toString(),
        if (minPh != null) 'min_ph': minPh.toString(),
        if (maxPh != null) 'max_ph': maxPh.toString(),
        if (medium != null) 'medium': medium,
      });

      final response = await http.get(uri);

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final List<dynamic> samplesJson = data['samples'];
        return samplesJson.map((json) => CorrosionSample.fromJson(json)).toList();
      } else {
        // Try to get error message from response
        try {
          final errorData = json.decode(response.body);
          throw Exception(errorData['error'] ?? 'Failed to load samples: ${response.statusCode}');
        } catch (_) {
          throw Exception('Failed to load samples: ${response.statusCode}');
        }
      }
    } catch (e) {
      throw Exception('Error fetching samples: $e');
    }
  }

  Future<CorrosionCalculation> calculateCorrosionRate({
    required String material,
    required double temperature,
    double? ph,
    double? naclPercentage,
    String? medium,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/calculate-corrosion-rate'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'material': material,
          'temperature': temperature,
          'ph': ph,
          'nacl_percentage': naclPercentage,
          'medium': medium,
        }),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return CorrosionCalculation.fromJson(data);
      } else {
        final error = json.decode(response.body);
        throw Exception(error['error'] ?? 'Failed to calculate corrosion rate');
      }
    } catch (e) {
      throw Exception('Error calculating corrosion rate: $e');
    }
  }

  Future<Map<String, dynamic>> uploadCsv(String filePath) async {
    try {
      final request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseUrl/upload-csv'),
      );

      request.files.add(await http.MultipartFile.fromPath('file', filePath));

      final streamedResponse = await request.send();
      final response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        final error = json.decode(response.body);
        throw Exception(error['error'] ?? 'Failed to upload CSV');
      }
    } catch (e) {
      throw Exception('Error uploading CSV: $e');
    }
  }

  Future<Map<String, dynamic>> uploadCsvFromBytes(
    List<int> bytes,
    String filename,
  ) async {
    try {
      final request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseUrl/upload-csv'),
      );

      request.files.add(
        http.MultipartFile.fromBytes(
          'file',
          bytes,
          filename: filename,
        ),
      );

      final streamedResponse = await request.send();
      final response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        final error = json.decode(response.body);
        throw Exception(error['error'] ?? 'Failed to upload CSV');
      }
    } catch (e) {
      throw Exception('Error uploading CSV: $e');
    }
  }

  Future<Map<String, dynamic>> getStatistics() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/statistics'));

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to load statistics: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching statistics: $e');
    }
  }

  Future<List<String>> getMaterials() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/materials'));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return List<String>.from(data['materials']);
      } else {
        throw Exception('Failed to load materials: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching materials: $e');
    }
  }

  Future<List<String>> getMediums() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/mediums'));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return List<String>.from(data['mediums']);
      } else {
        throw Exception('Failed to load mediums: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching mediums: $e');
    }
  }

  Future<bool> healthCheck() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/health'));
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
}

