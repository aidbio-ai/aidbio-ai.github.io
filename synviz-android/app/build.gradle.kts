plugins {
    id("com.android.application")
}

android {
    namespace = "ai.aidbio.synviz"
    compileSdk = 34

    defaultConfig {
        applicationId = "ai.aidbio.synviz"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }

    buildTypes {
        release {
            // Debuggable-signing is applied in CI; keep the release variant
            // shrink-free so the WebView + bundled HTML asset are untouched.
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}

dependencies {
    implementation("androidx.core:core:1.13.1")
    implementation("androidx.activity:activity:1.9.2")
}
