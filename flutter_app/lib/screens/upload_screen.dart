import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import 'package:file_picker/file_picker.dart';
import '../providers/corrosion_provider.dart';

class UploadScreen extends StatefulWidget {
  const UploadScreen({super.key});

  @override
  State<UploadScreen> createState() => _UploadScreenState();
}

class _UploadScreenState extends State<UploadScreen> {
  String? _selectedFile;
  bool _uploading = false;

  Future<void> _confirmAndClearDatabase() async {
    final shouldClear = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(
          'تأكيد المسح',
          style: GoogleFonts.cairo(fontWeight: FontWeight.bold),
        ),
        content: Text(
          'سيتم حذف جميع العينات المستوردة والحسابات المحفوظة وسجل الملفات المرفوعة. هل تريد المتابعة؟',
          style: GoogleFonts.cairo(),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: Text('إلغاء', style: GoogleFonts.cairo()),
          ),
          ElevatedButton(
            onPressed: () => Navigator.pop(context, true),
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.red.shade700,
              foregroundColor: Colors.white,
            ),
            child: Text('مسح', style: GoogleFonts.cairo()),
          ),
        ],
      ),
    );

    if (shouldClear != true || !mounted) return;

    final provider = Provider.of<CorrosionProvider>(context, listen: false);
    final result = await provider.clearDatabase();
    if (!mounted) return;

    if (provider.error == null && result != null) {
      final deletedCounts =
          Map<String, dynamic>.from(result['deleted_counts'] ?? {});
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            'تم المسح بنجاح: عينات ${deletedCounts['corrosion_samples'] ?? 0}، حسابات ${deletedCounts['calculated_corrosion_rates'] ?? 0}',
          ),
          backgroundColor: Colors.green,
        ),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('خطأ: ${provider.error ?? 'تعذر مسح البيانات'}'),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  Future<void> _pickAndUploadFile() async {
    try {
      // Use file_picker to pick CSV files
      // On Android, we use withData to get file content directly
      FilePickerResult? result;
      
      try {
        // Use FileType.any to allow all files, then filter by extension
        // This works better on Android where MIME types can be inconsistent
        result = await FilePicker.platform.pickFiles(
          type: FileType.any,
          allowMultiple: false,
          withData: true, // Get file data for Android compatibility
          withReadStream: false,
        );
        
        // Filter to only CSV files
        if (result != null && result.files.isNotEmpty) {
          final file = result.files.single;
          final fileName = file.name.toLowerCase();
          if (!fileName.endsWith('.csv')) {
            debugPrint('═══════════════════════════════════════════════════════════');
            debugPrint('⚠️ ملف غير صحيح:');
            debugPrint('File Name: ${file.name}');
            debugPrint('File Extension: ${file.extension}');
            debugPrint('Expected: .csv');
            debugPrint('═══════════════════════════════════════════════════════════');
            
            if (!mounted) return;
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(
                content: Text('يرجى اختيار ملف CSV فقط (.csv)'),
                backgroundColor: Colors.orange,
                duration: Duration(seconds: 3),
              ),
            );
            return;
          }
        }
      } catch (pickError) {
        // Log error to debug console
        debugPrint('═══════════════════════════════════════════════════════════');
        debugPrint('❌ خطأ في فتح ملف picker:');
        debugPrint('Error: $pickError');
        debugPrint('Error Type: ${pickError.runtimeType}');
        debugPrint('Stack Trace: ${StackTrace.current}');
        debugPrint('═══════════════════════════════════════════════════════════');
        
        if (!mounted) return;
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('خطأ في فتح ملف picker: $pickError'),
            backgroundColor: Colors.red,
            duration: const Duration(seconds: 4),
          ),
        );
        return;
      }

      if (result == null) {
        // User cancelled
        return;
      }

      if (result.files.isEmpty) {
        if (!mounted) return;
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('لم يتم اختيار ملف'),
            backgroundColor: Colors.orange,
          ),
        );
        return;
      }

      final file = result.files.single;

      // Log file information
      debugPrint('═══════════════════════════════════════════════════════════');
      debugPrint('📄 معلومات الملف المختار:');
      debugPrint('File Name: ${file.name}');
      debugPrint('File Path: ${file.path ?? "Not available"}');
      debugPrint('File Size: ${file.size} bytes');
      debugPrint('File Bytes: ${file.bytes != null ? "Available (${file.bytes!.length} bytes)" : "Not available"}');
      debugPrint('File Extension: ${file.extension}');
      debugPrint('═══════════════════════════════════════════════════════════');

      setState(() {
        _selectedFile = file.name;
        _uploading = true;
      });

      final provider = Provider.of<CorrosionProvider>(context, listen: false);
      Map<String, dynamic>? uploadResult;
      
      // Try to upload using path first, then bytes if path is not available
      if (file.path != null) {
        debugPrint('📤 رفع الملف باستخدام path: ${file.path}');
        // Use path if available (faster)
        uploadResult = await provider.uploadCsv(file.path!);
      } else if (file.bytes != null) {
        debugPrint('📤 رفع الملف باستخدام bytes: ${file.bytes!.length} bytes');
        // Use bytes directly if path is not available (Android compatibility)
        uploadResult = await provider.uploadCsvFromBytes(file.bytes!, file.name);
      } else {
        // No path and no bytes - show error
        debugPrint('═══════════════════════════════════════════════════════════');
        debugPrint('❌ تعذر الوصول إلى الملف:');
        debugPrint('File Name: ${file.name}');
        debugPrint('File Path: ${file.path}');
        debugPrint('File Bytes: ${file.bytes != null ? "Available (${file.bytes!.length} bytes)" : "Not available"}');
        debugPrint('File Size: ${file.size}');
        debugPrint('═══════════════════════════════════════════════════════════');
        
        if (!mounted) return;
        setState(() {
          _uploading = false;
          _selectedFile = null;
        });
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text(
              'تعذر الوصول إلى الملف. يرجى المحاولة مرة أخرى أو اختيار ملف من موقع آخر',
            ),
            backgroundColor: Colors.orange,
            duration: Duration(seconds: 4),
          ),
        );
        return;
      }

      if (!mounted) return;

      final messenger = ScaffoldMessenger.of(context);
      if (provider.error == null) {
        debugPrint('═══════════════════════════════════════════════════════════');
        debugPrint('✅ تم رفع الملف بنجاح!');
        debugPrint('File Name: $_selectedFile');
        debugPrint('Samples Processed: ${provider.samples.length}');
        debugPrint('═══════════════════════════════════════════════════════════');
        
        messenger.showSnackBar(
          SnackBar(
            content: Text(
              'تم رفع الملف بنجاح! تمت معالجة ${uploadResult?['rows_processed'] ?? 0} صفوف وحفظ ${uploadResult?['rows_saved'] ?? 0}',
            ),
            backgroundColor: Colors.green,
            duration: const Duration(seconds: 3),
          ),
        );
        // Clear selected file after successful upload
        setState(() {
          _selectedFile = null;
        });
      } else {
        // Log error to debug console
        debugPrint('═══════════════════════════════════════════════════════════');
        debugPrint('❌ خطأ في رفع الملف:');
        debugPrint('Error: ${provider.error}');
        debugPrint('File Name: $_selectedFile');
        debugPrint('═══════════════════════════════════════════════════════════');
        
        messenger.showSnackBar(
          SnackBar(
            content: Text('خطأ: ${provider.error}'),
            backgroundColor: Colors.red,
            duration: const Duration(seconds: 4),
          ),
        );
      }
    } catch (e, stackTrace) {
      // Log error to debug console
      debugPrint('═══════════════════════════════════════════════════════════');
      debugPrint('❌ خطأ غير متوقع في رفع الملف:');
      debugPrint('Error: $e');
      debugPrint('Error Type: ${e.runtimeType}');
      debugPrint('Stack Trace:');
      debugPrint(stackTrace.toString());
      debugPrint('═══════════════════════════════════════════════════════════');
      
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('خطأ: $e'),
          backgroundColor: Colors.red,
          duration: const Duration(seconds: 5),
        ),
      );
    } finally {
      if (mounted) {
        setState(() {
          _uploading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<CorrosionProvider>(
      builder: (context, provider, child) {
        return SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Card(
                elevation: 4,
                child: Padding(
                  padding: const EdgeInsets.all(24),
                  child: Column(
                    children: [
                      Icon(
                        Icons.cloud_upload,
                        size: 64,
                        color: Colors.blue.shade700,
                      ),
                      const SizedBox(height: 16),
                      Text(
                        'رفع ملف CSV',
                        style: GoogleFonts.cairo(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        'اختر ملف CSV يحتوي على بيانات التآكل',
                        style: GoogleFonts.cairo(
                          fontSize: 16,
                          color: Colors.grey,
                        ),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 24),
                      if (_selectedFile != null) ...[
                        Container(
                          padding: const EdgeInsets.all(12),
                          decoration: BoxDecoration(
                            color: Colors.blue.shade50,
                            borderRadius: BorderRadius.circular(8),
                            border: Border.all(
                              color: Colors.blue.shade200,
                              width: 1,
                            ),
                          ),
                          child: Row(
                            children: [
                              Icon(
                                Icons.insert_drive_file,
                                color: Colors.blue.shade700,
                                size: 24,
                              ),
                              const SizedBox(width: 12),
                              Expanded(
                                child: Text(
                                  _selectedFile!,
                                  style: GoogleFonts.cairo(
                                    fontSize: 14,
                                    fontWeight: FontWeight.w500,
                                  ),
                                  maxLines: 2,
                                  overflow: TextOverflow.ellipsis,
                                ),
                              ),
                              IconButton(
                                icon: const Icon(Icons.close, size: 20),
                                onPressed: () {
                                  setState(() {
                                    _selectedFile = null;
                                  });
                                },
                                padding: EdgeInsets.zero,
                                constraints: const BoxConstraints(),
                                color: Colors.grey.shade600,
                              ),
                            ],
                          ),
                        ),
                        const SizedBox(height: 16),
                      ],
                      SizedBox(
                        width: double.infinity,
                        height: 50,
                        child: ElevatedButton.icon(
                          onPressed: (_uploading || provider.isLoading)
                              ? null
                              : _pickAndUploadFile,
                          icon: (_uploading || provider.isLoading)
                              ? const SizedBox(
                                  width: 20,
                                  height: 20,
                                  child: CircularProgressIndicator(
                                    strokeWidth: 2,
                                    color: Colors.white,
                                  ),
                                )
                              : const Icon(Icons.upload_file),
                          label: Text(
                            (_uploading || provider.isLoading)
                                ? 'جاري الرفع...'
                                : (_selectedFile != null
                                      ? 'رفع الملف المختار'
                                      : 'اختر ملف CSV'),
                            style: GoogleFonts.cairo(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.blue.shade700,
                            foregroundColor: Colors.white,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                            ),
                            elevation: 2,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 24),
              Card(
                elevation: 4,
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      Text(
                        'إدارة البيانات',
                        style: GoogleFonts.cairo(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        'استخدم هذا الخيار لمسح جميع البيانات المستوردة والحسابات المحفوظة وإعادة العرض من البداية.',
                        style: GoogleFonts.cairo(
                          fontSize: 14,
                          color: Colors.grey.shade700,
                        ),
                      ),
                      const SizedBox(height: 16),
                      OutlinedButton.icon(
                        onPressed: provider.isLoading ? null : _confirmAndClearDatabase,
                        icon: const Icon(Icons.delete_sweep_outlined),
                        label: Text(
                          'مسح قاعدة البيانات',
                          style: GoogleFonts.cairo(
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        style: OutlinedButton.styleFrom(
                          foregroundColor: Colors.red.shade700,
                          side: BorderSide(color: Colors.red.shade300),
                          padding: const EdgeInsets.symmetric(vertical: 14),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 24),
              Card(
                elevation: 4,
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'متطلبات ملف CSV',
                        style: GoogleFonts.cairo(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 12),
                      _buildRequirement(
                        'Material',
                        'نوع العينة (مثال: API-5L X65, Carbon steel)',
                      ),
                      _buildRequirement('Temperature', 'درجة الحرارة (°C)'),
                      _buildRequirement('pH', 'pH (اختياري)'),
                      _buildRequirement('NaCl (%)', 'نسبة NaCl (اختياري)'),
                      _buildRequirement(
                        'Medium/Environment',
                        'الوسط (اختياري)',
                      ),
                      _buildRequirement(
                        'Corrosion Rate',
                        'معدل التآكل (mm/yr أو mpy)',
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  Widget _buildRequirement(String field, String description) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(Icons.check_circle, size: 16, color: Colors.green),
          const SizedBox(width: 8),
          Expanded(
            child: Text(
              '$field: $description',
              style: GoogleFonts.cairo(fontSize: 14),
            ),
          ),
        ],
      ),
    );
  }
}
