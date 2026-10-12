# PlayGTA5 Local Runner

Run an archived PlayGTA5 browser client from your own computer. This project serves a local client mirror over `http://localhost`; the browser runs the game engine and uses the computer's CPU and GPU.

> **Unofficial project.** This is a community client snapshot, not the original website's development repository, and is not affiliated with or endorsed by Rockstar Games.

> **License status.** The client's reuse rights have not been verified. The repository is public, but it does not currently grant an open-source license; do not assume permission to reuse or redistribute its contents.

## What you need

- Windows 10/11 x64 for the included launcher and bundled runtime. Other platforms can run the server with an installed Python 3.11 or newer.
- A current Chrome, Brave, or Edge browser with WebGPU enabled and hardware acceleration on.
- A complete client site mirror that you are authorized to use. The archived mirror was roughly **20 GB**; the exact size varies by copy.

The game-data mirror is a separate, large download and is not included in Git. Do not commit the mirror files to this repository.

## Download the mirror with qBittorrent

The user-provided mirror archive is approximately **19.7 GB**. Copy the full magnet URI below, open qBittorrent, select **File → Add Torrent Link**, paste the URI, and start the download.

```text
magnet:?xt=urn:btih:57a4193cc3d3f069ce436fcda040ed4c705b76c7&dn=GTA5Webport.zip&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Fopen.demonii.com%3A1337%2Fannounce&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce&tr=http%3A%2F%2Ftracker2.dler.org%3A80%2Fannounce&tr=http%3A%2F%2Ftracker.dler.org%3A6969%2Fannounce
```

After the download finishes, extract the archive and use the folder containing `index.html`, `data\`, and `b\8b0b5899ed\` as the site root described below. Keep the mirror outside Git.

## Quick start on Windows

### 1. Clone the repository

Open PowerShell and run:

```powershell
Set-Location "$env:USERPROFILE\Downloads"
git clone https://github.com/Adityabaskati-weeb/playgta5.git
Set-Location .\playgta5
```

This creates a checkout at:

```text
C:\Users\<your-Windows-user>\Downloads\playgta5
```

The repository includes a portable Python runtime, so the Windows launcher does not require a separate Python installation.

### 2. Place your local mirror

Copy the mirror's **site root** to `mirror\playgta5.com`. The site root is the folder that directly contains `index.html`, `data\`, and `b\8b0b5899ed\`:

```text
C:\Users\<your-Windows-user>\Downloads\playgta5\mirror\playgta5.com\index.html
C:\Users\<your-Windows-user>\Downloads\playgta5\mirror\playgta5.com\data\manifest.json
C:\Users\<your-Windows-user>\Downloads\playgta5\mirror\playgta5.com\b\8b0b5899ed\game.wasm
```

Keep the folder structure intact. Do not point the launcher at the parent `mirror` folder or at a folder that contains another `playgta5.com` folder.

If your site root is elsewhere, leave it there and pass its full path in step 3.

### Optional: build a mirror from the configured public source

The repository includes a resumable downloader for the public asset endpoint configured in `mirror_site.py`. If that source is reachable and you are authorized to fetch its files, run it from the repository folder:

```powershell
.\runtime\python.exe .\mirror_site.py --workers 3 --rate-mib 24
```

The transfer is large and may take hours; completed files are retained so a later run can resume. The downloader does not verify or grant rights to the downloaded content. If the configured source is unavailable, use a mirror you are authorized to access and point the launcher at its site root.

### 3. Start the local server

Double-click `Launch-Local.cmd`. It checks for the required files, starts the server, and opens the default browser at:

```text
http://localhost:8000/
```

For a mirror stored at another path, run this from the repository folder:

```powershell
.\Launch-Local.cmd --root "D:\GameData\playgta5.com"
```

Or use the PowerShell launcher:

```powershell
.\Start-Local.ps1 -Root "D:\GameData\playgta5.com" -Port 8000
```

Keep the server window open while playing. Press **Ctrl+C** in that window to stop it. If port 8000 is already occupied, stop the other local server before launching this one.

### Run without the launcher

The bundled runtime can start the server directly:

```powershell
.\runtime\python.exe .\serve_local.py --open
```

Or, with an installed Python 3.11+:

```powershell
python .\serve_local.py --root "D:\GameData\playgta5.com" --port 8000 --open
```

On macOS or Linux, run the same server with your installed Python and the site's mirror root:

```sh
python3 ./serve_local.py --root "/path/to/playgta5.com" --port 8000 --open
```

## Browser and graphics setup

The server supplies the cross-origin isolation headers the WebAssembly engine needs. `localhost` is treated as a secure browser context, so no insecure-origin flag is needed.

In Chrome or Brave, enable **Use graphics acceleration when available** in the browser's system settings, then restart the browser. Check `chrome://gpu` or `brave://gpu` for WebGPU status. Windows **Settings → System → Display → Graphics** can set the browser executable to **High performance** when the computer has a discrete GPU. The browser and OS choose the adapter; this project cannot force a particular GPU.

The local server only sends files. The browser performs the rendering and decides how much system RAM and GPU memory to use; the page does not reserve a fixed 4 GB or 6 GB allocation.

## Performance options

The local page defaults to a reduced-resource profile and 75% render scale. At 75% width and height, the renderer draws about 56% as many pixels as native resolution. The reduced profile lowers texture, shadow, crowd, vehicle, and level-of-detail settings to favor stability.

Append a query string to the URL to change the profile:

| URL | Effect |
| --- | --- |
| `http://localhost:8000/` | Reduced-resource profile, 75% scale, default 60 FPS cap |
| `http://localhost:8000/?scale=1` | Request 100% render scale (still subject to the profile's resolution cap) |
| `http://localhost:8000/?low=0` | Disable the reduced-resource profile; may use substantially more memory |
| `http://localhost:8000/?fps=30` | Set the game's frame limiter to 30 FPS |
| `http://localhost:8000/?fps=0` | Disable the game's frame limiter for diagnostics |

Press **`=`** in the game to toggle its FPS readout. Actual frame rate depends on the browser, GPU, CPU, resolution, and scene; a cap is not a guarantee that the system can sustain that rate.

## Controls

- **Enter** — Story Mode
- **Space** — Sandbox/map selection
- **5** — GTA V map; **6** — `env_test` map in Sandbox Mode
- **Esc** — Release the mouse after clicking the game canvas
- **Shift+P** — Switch keyboard input mode

Direct Sandbox URLs:

```text
http://localhost:8000/?mode=sandbox
http://localhost:8000/?mode=sandbox&map=env_test
```

## Troubleshooting

- **“Mirror is missing or incomplete”** — Confirm the `--root` path points to the folder containing `index.html`, `data\manifest.json`, and `b\8b0b5899ed\game.wasm`.
- **Blank page or WebGPU error** — Update the browser, enable hardware acceleration, and check its GPU status page.
- **Memory error or browser tab crash** — Keep the reduced profile enabled, close other tabs and restart the game. Browser memory use cannot be hard-capped by this launcher.
- **Port is busy** — Stop the other process using port 8000 before launching this server.

## Repository map

- `serve_local.py` and the launchers start the isolated local HTTP server.
- `mirror_site.py` downloads the configured public client assets into the ignored `mirror/` directory.
- `homepage.html`, `loader.js`, `game.js`, `io_worker.js`, and `wgpu_worker.js` make up the captured browser client and local changes.
- `snapshot/` contains asset inventories, provenance notes, and generated verification/package records.
- `runtime/` contains the portable Windows Python runtime; `bundle_runtime.py` rebuilds it from a compatible local Windows Python installation.

## Project provenance and license

This repository preserves a public client snapshot that was previously served at `playgta5.com`; it is not the site's original development source. The upstream project does not provide a verified license for the client snapshot, so this repository does **not** claim that the snapshot is open-source or grant permission to reuse it. Public visibility on GitHub is not a substitute for a license. The large game-data mirror is hosted separately and is not included in Git; the torrent link points to that separate archive and does not change the licensing of the client snapshot or game content.

The upstream README credited Sebas Furbastian for collecting the snapshot. GTA V, its marks, and its game content belong to their respective rights holders.

For takedown requests or concerns about material in this repository, email [animeweeb082004@gmail.com](mailto:animeweeb082004@gmail.com). Please include the repository URL and identify the material in question.
