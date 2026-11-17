# AMIT / Igloo Inc. 3D WebGL Experience (1:1 Offline Clone)

This folder contains the complete, self-contained, 1:1 offline replica of the award-winning **Igloo Inc.** 3D interactive web experience, fully rebranded to **AMIT** with custom typography, 3D glitch-blink shaders, and native audio.

---

## 🚀 Quick Start

### 1. Launch with Batch Script
Double-click either launcher script:
- `start_amit.bat` (Recommended)
- `start_igloo.bat`

This starts the high-performance local server on port **5502** and automatically opens [http://localhost:5502/](http://localhost:5502/) in your default browser.

### 2. Manual Command Line
```powershell
cd c:\Users\amitk\Music\family\adsblocking1\igloo
python server.py
```
Then navigate to:
- **Local URL**: [http://localhost:5502/](http://localhost:5502/)
- **Direct IP**: [http://127.0.0.1:5502/](http://127.0.0.1:5502/)

---

## 📁 Directory Structure & Downloaded Assets

Every single asset is downloaded and hosted locally (zero external CDN dependencies):

```
igloo/
├── index.html                   # Entry point (offline relative paths, AMIT Inc. metadata)
├── robots.txt                   # Standard crawler policy
├── favicon.ico                  # Browser tab icon
├── server.py                    # Threaded HTTP server with byte-range audio & MIME support
├── start_amit.bat               # Windows double-click launcher (AMIT)
├── start_igloo.bat              # Windows double-click launcher (Igloo)
└── assets/
    ├── index-2e130bc1.js        # Core application bootstrapper & preloader coordinator
    ├── App3D-d68cb154.js        # Three.js 3D engine, custom GLSL shaders, camera & timeline
    ├── audioworker-036a09db.js  # Multi-threaded audio playback worker
    ├── bitmapworker-046527f8.js # Image bitmap decoding worker
    ├── msdfworker-ac346fa7.js   # Multi-channel Signed Distance Field font renderer
    ├── exrworker-41cbee65.js    # HDR/EXR environment map worker
    ├── fonts/                   # IBM Plex Mono MSDF fonts and character metrics
    │   ├── IBMPlexMono-Medium.json
    │   ├── IBMPlexMono-Medium-datatexture.ktx2
    │   ├── IBMPlexMono-Regular.json
    │   └── IBMPlexMono-Regular-datatexture.ktx2
    ├── geometries/              # Draco-compressed 3D meshes (.drc)
    │   ├── ground.drc           # Snowy ground terrain
    │   ├── mountain.drc         # Background mountain ridges
    │   ├── igloo.drc            # Photorealistic igloo block dome
    │   ├── floor.drc            # Interior floor geometry
    │   ├── shattered_ring.drc   # Sci-fi particle accelerator rings
    │   ├── smoke_trail.drc      # Volumetric smoke trails
    │   └── cubes/               # 3D interactive portfolio showcase models
    ├── images/                  # KTX2 Basis-compressed GPU textures & noise maps
    │   ├── bokeh.ktx2
    │   ├── caustics.ktx2
    │   ├── clouds_noise.ktx2
    │   ├── cubes_env.exr        # 32-bit floating-point environment map
    │   └── ui/
    │       ├── amit-logo.png    # Custom antialiased AMIT geometric wordmark
    │       ├── logo-datatexture.ktx2
    │       ├── close-datatexture.ktx2
    │       ├── sound-datatexture.ktx2
    │       └── visit-datatexture.ktx2
    ├── libs/                    # WebAssembly decoders
    │   ├── basis/               # Basis Universal transcoder (JS + WASM)
    │   └── draco/               # Google Draco 3D geometry decoder (JS + WASM)
    └── audio/                   # 18 spatial audio tracks (.ogg)
        ├── music-highq.ogg      # Ambient background synth score
        ├── room.ogg             # Atmospheric room tone
        ├── wind.ogg             # Arctic wind howling
        ├── igloo.ogg            # Resonant dome acoustics
        ├── beeps.ogg / beeps2.ogg / beeps3.ogg
        ├── circles.ogg / particles.ogg / shard.ogg
        ├── click-project.ogg / enter-project.ogg / leave-project.ogg
        └── manifesto.ogg
```

---

## 🎨 Features & Rebranding

1. **AMIT 3D Wordmark**: Replaces the top-left logo with custom geometric typography while preserving native cyber glitch, blink shaders, and hover audio triggers.
2. **Dynamic Decrypt Animations**: Real-time IBM Plex Mono font decoding effect on UI elements.
3. **Volumetric Lighting & Fog**: High-end Three.js post-processing pipeline with custom Bloom pass and tone mapping.
4. **Spatial Audio Integration**: HTML5 Audio & Web Audio API with automatic user interaction handling and volume curves based on scroll timeline depth.
5. **100% Offline**: Requires no internet connection to run.
