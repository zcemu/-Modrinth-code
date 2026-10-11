# PortaCraft 便携版（非官方 / unofficial portable build）

> **声明 / Disclaimer**：本构建为个人自用，公开发布仅为方便有同样需求的人下载，
> 并非作为正式软件提供。基于 Modrinth 官方 [`modrinth/code`](https://github.com/modrinth/code)
> 源码构建，仅增加便携模式（`portable.txt`）、移除 Modrinth+ 升级推广入口，并替换
> 名称与图标以避免与官方品牌混淆；其余均为官方原版功能。本项目与 Modrinth 官方无关。
>
> This build is for personal use. It is published publicly only for the convenience
> of anyone who wants it — it is not offered as official software. Built from the
> official [`modrinth/code`](https://github.com/modrinth/code) source with only
> portable mode (`portable.txt`) added, the Modrinth+ upsell entry removed, and the
> name/icons replaced to avoid confusion with the official brand; everything else
> is stock official functionality. This project is not affiliated with Modrinth.

## 使用方法（中文）

1. 下载 `PortaCraft-Portable.zip`，解压到任意位置（推荐放到非系统盘，如 `D:\Games\PortaCraft`）。
2. 确保 `portable.txt`（空文件）跟 `PortaCraft.exe` 放在同一目录——zip 里已经自带，通常不用再动。
3. 运行 `PortaCraft.exe`。

首次启动会在 exe 旁边自动创建 `data/` 文件夹，启动器的**所有数据**（数据库、日志、
备份、实例、下载、WebView2 缓存）都存放在 `data/` 里，不再往 C 盘写：

- 重装系统没影响，只要把整个文件夹放在非系统盘。
- 整文件夹拷到另一台电脑直接能用。
- 删掉 `portable.txt` 即可回到官方默认行为（数据存 `%APPDATA%\ModrinthApp`）。

### 注意事项

- **未签名**：Windows SmartScreen 在首次运行时会弹警告，点 *More info* → *Run anyway*。
- **无自动更新**：这是故意的——官方更新会把便携版覆盖成正式版，便携模式就丢了。
  想升级就下载新版便携包，把 exe 换掉就行，`data/`（实例、存档、设置）不受影响。
- 源码来自官方 [`modrinth/code`](https://github.com/modrinth/code)，只加了一个
  约 20 行的便携模式补丁（`apply_portable.py`，见本仓库根目录）。

---

## How to use (English)

1. Download `PortaCraft-Portable.zip` and extract it anywhere you like
   (e.g. `D:\Games\PortaCraft` — a non-system drive is recommended).
2. Make sure an (empty) file named `portable.txt` sits next to
   `PortaCraft.exe` — it's already included in the zip, so usually
   there's nothing to do.
3. Run `PortaCraft.exe`.

On first launch a `data/` folder is created next to the exe. **Everything**
the launcher stores — database, logs, backups, instances, downloads,
WebView2 cache — lives inside `data/`. Nothing important is written to `C:`.

- Reinstalling Windows doesn't affect it: just keep the folder on a non-system drive.
- Copy the whole folder to a different PC and it just works.
- Delete `portable.txt` to fall back to the official default behavior
  (data stored in `%APPDATA%\ModrinthApp`).

### Notes

- **Unsigned binary**: Windows SmartScreen will warn on first run —
  click *More info* → *Run anyway*.
- **No auto-updater** — that's intentional: an official update would overwrite
  the portable build and kill portable mode. To update, download the newer
  portable release and replace the exe — your `data/` folder (instances, worlds,
  settings) stays untouched.
- Source: official [`modrinth/code`](https://github.com/modrinth/code)
  plus a ~20-line portable-mode patch (see `apply_portable.py` in this repo).
