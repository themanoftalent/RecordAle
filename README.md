# RecordAle

<p align="center">
  <img width="180" alt="RecordAle Logo" src="./public/app-icons/recordalemac-512.png" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/macOS%20%7C%20Windows%20%7C%20Linux-111827?style=for-the-badge" alt="macOS Windows Linux" />
  <img src="https://img.shields.io/badge/open%20source-AGPL3.0-2563eb?style=for-the-badge" alt="AGPL 3.0 license" />
  <img src="https://img.shields.io/badge/maintained%20by-SoftAI%20Yazılım-10b981?style=for-the-badge" alt="Maintained by SoftAI Yazılım" />
</p>

<h3 align="center">Create polished walkthroughs, product demos, and tutorial videos in minutes</h3>

**RecordAle** is an open-source desktop screen recorder and professional motion video editor engineered for creators, software developers, educators, and product teams. It delivers high-production values—dynamic auto-zooming, smooth cursor tracks, customized backgrounds, webcam bubbles, and studio frame styling—directly on your machine without requiring complex timeline video suites.

---

## 📥 macOS Installation Guide (DMG)

### 1. Download & Install
1. Download **`RecordAle-arm64.dmg`** from [GitHub Releases](https://github.com/themanoftalent/RecordAle/releases).
2. Double-click the `.dmg` file to mount it.
3. Drag **RecordAle.app** into your **Applications** folder.

### 2. First-Time Launch (Bypassing macOS Gatekeeper)
Because open-source releases are built without an Apple Developer subscription, macOS Gatekeeper may display a prompt like:
> *"RecordAle" cannot be opened because Apple cannot check it for malicious software.*

**To open RecordAle, choose either method:**

- **Method A (Terminal command - Recommended)**:
  Open Terminal and run:
  ```bash
  xattr -cr /Applications/RecordAle.app
  ```
  *(This clears the downloaded quarantine flag and allows RecordAle to open immediately).*

- **Method B (Finder)**:
  1. Open `/Applications` in Finder.
  2. **Right-click (or Control-click)** on `RecordAle.app` and choose **Open**.
  3. Click **Open** in the confirmation popup.

---

## Key Features

### 🎬 Screen Recording & Capture Backends
- **macOS Native ScreenCaptureKit (SCK)**: Hardware-accelerated recording on macOS 14.0+ with dedicated high-performance Swift helpers (`ScreenCaptureKitRecorder`, `ScreenCaptureKitWindowList`, `SystemCursorAssets`, `NativeCursorMonitor`).
- **Windows Graphics Capture (WGC)**: Native GPU-accelerated capture with WASAPI low-latency loopback audio.
- **Linux Recording**: Display and window capture with native audio routing.
- **Multi-display & Window Isolation**: Capture fullscreen, custom regions, or pinpoint individual app windows.
- **Microphone & System Audio Muxing**: Record voice narration alongside crisp system sound.

### 🔍 Motion & Auto-Zoom
- **Intelligent Cursor-Driven Auto-Zoom**: Automatically zooms and pans into user actions, clicks, and keystrokes.
- **Smooth Cursor Trajectories**: Records cursor coordinates and renders polished, customizable cursor trails and click ripples.
- **Custom Zoom Regions**: Easily create, trim, and adjust manual zoom keys on the visual timeline.

### 🎨 Studio Canvas & Framing
- **Beautiful Backgrounds**: Gradients, mesh wallpapers, colors, blur underlays, and custom image backdrops.
- **Window Framing & Shadows**: Add macOS-style titlebars, window controls, rounded corners, drop shadows, and adjustable padding.
- **Interactive Webcam Overlay**: Positionable webcam bubble with roundness control, mirroring, shadows, and zoom-reactive framing.

### ✂️ Precision Timeline Editor
- **Non-destructive Project Workflow**: Save and resume anytime with native `.recordale` project packages (with backward compatibility for `.recoreale` and `.recordly` files).
- **Trimming & Speed Regions**: Cut out mistakes, speed up repetitive tasks, or create dramatic slow-motion moments.
- **Annotations & Captions**: Text overlays, figures, callouts, arrows, and automated Whisper captions (`v1.8.4`).
- **Direct Export**: Ultra-fast MP4, WebM, and GIF rendering with optional NVIDIA CUDA/NVENC hardware acceleration.

---

## Project Structure

```
RecordAle/
├── electron/                 # Electron main and preload processes
│   ├── main.ts               # App entrypoint, lifecycle, IPC bootstrapping
│   ├── windows.ts            # Window creation and management
│   ├── appPaths.ts           # Application data paths (RecordAle-dev / RecordAle)
│   ├── native/               # Compiled native helpers (macOS SCK & Windows WGC)
│   │   ├── bin/darwin-arm64/ # Apple Silicon Swift helper binaries
│   │   └── bin/darwin-x64/   # Intel Mac Swift helper binaries
│   └── ipc/                  # Modular IPC handlers (recording, project, export)
├── src/                      # React 19 Frontend & Video Editor Canvas
│   ├── components/           # UI components, timeline, dashboard, canvas
│   ├── contexts/             # ThemeContext (recordale.theme), Session, Recording
│   ├── i18n/                 # Localization (EN, TR, ES, FR, etc.)
│   └── lib/                  # Utilities, math, geometry, color palettes
├── public/                   # Static web assets & RecordAle icons
├── scripts/                  # Build scripts & native helper compilers
└── package.json              # Project definition & scripts
```

---

## Getting Started

### Prerequisites
- **Node.js**: v20 or higher (Node v22+ recommended)
- **NPM**: v10 or higher
- **macOS Requirements**: macOS 14.0+ and Xcode Command Line Tools (`swiftc` for native helpers)
- **Windows Requirements**: Windows 10 Build 19041+ with Visual Studio C++ build tools

### Installation

```bash
# Clone the repository
git clone https://github.com/themanoftalent/RecordAle.git
cd RecordAle

# Install dependencies
npm install
```

### Development

```bash
# Start Vite renderer and Electron concurrently in development mode
npm run dev
```

### Testing & Verification

```bash
# Run TypeScript typechecks
npm run typecheck

# Run test suite
npm run test
```

### Packaging & Release

```bash
# Package DMG for macOS
npx electron-builder --mac dmg --arm64

# Package for Windows (NSIS and portable)
npm run build:win

# Package for Linux (AppImage)
npm run build:linux
```

---

## File Formats & Compatibility

RecordAle introduces `.recordale` as the default project file format:
- **`.recordale`**: High-performance JSON manifest and bundled media assets preserving all cuts, zooms, annotations, and camera tracks.
- **Backward Compatibility**: Fully opens and edits legacy `.recoreale`, `.recordly`, and `.openscreen` project files seamlessly.

---

## Credits & Acknowledgements

RecordAle is maintained and enhanced by **SoftAI Yazılım (Mehmet Akif Çifçi)**.

RecordAle builds upon the pioneering open-source work of:
- [Recordly](https://github.com/webadderallorg/Recordly) by [@webadderall](https://x.com/webadderall)
- [OpenScreen](https://github.com/siddharthvaddem/openscreen) by Siddharth Vaddem

Licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

---

## ☕ Sponsor or Buy Me a Coffee

If you find this project helpful, consider supporting it or reaching out for collaboration:

[![Buy Me A Coffee](https://img.shields.io/badge/BUY%20ME%20A%20COFFEE-SUPPORT%20PROJECT-green?style=for-the-badge&logo=buymeacoffee)](https://buymeacoffee.com/themanoftalent) [![GitHub Sponsors](https://img.shields.io/badge/SPONSOR-GITHUB%20SPONSORS-ea4aaa?style=for-the-badge&logo=githubsponsors)](https://github.com/sponsors/themanoftalent) [![Let's Connect](https://img.shields.io/badge/LET%27S%20CONNECT-EMAIL-blue?style=for-the-badge&logo=gmail)](mailto:cs.akifcifci@gmail.com)
