# AMIT.AI - 1:1 Complete Standalone WebGL / 3D Gaussian Splats Experience

A complete 1:1 offline-ready recreation of [https://oryzo.ai/](https://oryzo.ai/) with full 3D WebGL scenes, 3D Gaussian Splats, Rive animations, and interactive materials.

## Features & Assets Included
- **3D Geometry Models (`/models/`)**: 25 `.buf` binary models (hero hand, animations, coffee cup, tray, desk, pinboard, wearable models, etc.).
- **WebGL Textures (`/textures/`)**: 73 texture maps including BRDF LUT, SMAA area/search, skin/hand materials, gobo lighting, and all hero desk props (pencil, eraser, cutter, pen, paperclips).
- **3D Gaussian Splats (`/splats/`)**: `props.sog` (3.09 MB), `table_reflection.sog` (486 KB), and mobile variants.
- **Gaussian Splat Sorter WASM**: `splat_sorter_bg-BfJrILzx.wasm` (38.5 KB).
- **Rive 2D Animation Engine (`/rive/`)**: `oryzo.riv` (59 KB) with standalone local WebAssembly runtimes (`rive.wasm` and `rive_fallback.wasm`).
- **3D MSDF Fonts & Web Fonts (`/fonts/`)**: Inter MSDF font geometry and texture, Literata, and DM Mono.
- **Wearable Gallery Media (`/images/wearable-gallery/`)**: Full video loops (`yoga.mp4`, `bite.mp4`) and high-res previews.
- **Custom Local Server (`server.py`)**: Built-in MIME handling for WASM, octet-stream buffers, WebP/AVIF images, and MP4 videos with CORS and fallback support.

## How to Run
1. Double-click `start_oryzo.bat` or run:
   ```cmd
   python -u server.py
   ```
2. Open your browser and navigate to:
   ```
   http://localhost:5501/index.html
   ```
