# SynViz — Synesthetic Photism Visualizer (Android)

A native Android wrapper around the **Synesthetic Photism Visualizer**, a
self-contained WebGL + Web Audio experience. The app hosts the visualizer in a
full-screen, hardware-accelerated `WebView` and feeds it the device microphone
so the graphics react to sound in real time.

The entire visualizer lives in [`app/src/main/assets/index.html`](app/src/main/assets/index.html)
and runs fully offline — no network is required at runtime.

## Features

- Full-screen immersive WebView (system bars hidden, screen kept on).
- Microphone capture wired through to the page's `getUserMedia` call, with the
  Android runtime permission requested up front.
- WebGL + `localStorage` (tone presets) enabled.
- Pure-XML adaptive launcher icon — no binary assets in the repo.

## Requirements

- Android 8.0 (API 26) or newer.
- A device microphone (the visualizer reacts to the mic spectrum).

## Building the APK

### On GitHub Actions (recommended)

Every push builds a debug APK. Grab it from the **Actions** run's
**Artifacts** section (`synviz-debug-apk`). Pushing a `v*` tag additionally
attaches the APK to a GitHub Release.

The workflow lives at
[`.github/workflows/android-build.yml`](.github/workflows/android-build.yml).

### Locally

You need the Android SDK (via Android Studio or the command-line tools) with
platform `android-34` and build-tools installed. Then:

```bash
./gradlew assembleDebug
```

The APK is written to `app/build/outputs/apk/debug/app-debug.apk`.

> Note: this project was authored in a sandbox that could not reach Google's
> SDK/Maven servers, so it is compiled on GitHub's runners rather than in the
> authoring environment. The committed Gradle wrapper (8.9) and AGP (8.5.2)
> download normally on any machine with network access to Google.

## Installing

```bash
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

Or copy `synviz-debug.apk` to the device and open it (enable
"install from unknown sources" for your file manager).

## Project layout

```
synviz-android/
├── app/
│   ├── build.gradle.kts
│   └── src/main/
│       ├── AndroidManifest.xml          # RECORD_AUDIO permission
│       ├── assets/index.html            # the visualizer (self-contained)
│       ├── java/ai/aidbio/synviz/MainActivity.java
│       └── res/                         # theme, strings, adaptive icon
├── build.gradle.kts
├── settings.gradle.kts
└── gradle/ + gradlew                    # Gradle wrapper (8.9)
```

## Turning this into its own repository

This project currently lives in the `synviz-android/` subdirectory of
`aidbio-ai/aidbio-ai.github.io`. To split it into a standalone repo, create an
empty repo on GitHub and then:

```bash
# from the repo root, on the branch that contains synviz-android/
git subtree split --prefix=synviz-android -b synviz-standalone
git push git@github.com:<you>/synviz-android.git synviz-standalone:main
```

The in-project workflow at `.github/workflows/android-build.yml` is already
written for a standalone layout (project at repo root), so CI works immediately
in the new repo.
