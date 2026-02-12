# Proguard rules for Vehicle Diagnostics app
# Keep Retrofit and Gson model classes
-keep class com.vehiclediag.app.data.models.** { *; }
-keepattributes Signature
-keepattributes *Annotation*
