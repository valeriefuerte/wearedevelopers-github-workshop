#!/usr/bin/env python3
"""Build the complete template locally; never fetch, push or change repository settings."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

KIT = Path(__file__).resolve().parents[1]
ROOT = KIT.parents[1]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def source_files():
    paths = subprocess.check_output(
        ["git", "-C", str(ROOT), "ls-files", "--cached", "--others", "--exclude-standard", "-z"])
    files = []
    for name in sorted(set(paths.decode().split("\0")) - {""}):
        path = ROOT / name
        if path.is_symlink() or not path.is_file() or ".." in Path(name).parts:
            raise ValueError(f"Invalid template payload: {name}")
        files.append(path)
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--refresh-manifest", action="store_true")
    args = parser.parse_args()
    output = args.output_dir.resolve()
    if output == ROOT or ROOT in output.parents:
        parser.error("Output must be outside the template checkout.")
    manifest_path = KIT / "workshop-kit.json"
    template_path = ROOT / "template-source.json"
    manifest = json.loads(manifest_path.read_text())
    template = json.loads(template_path.read_text())
    if (template["repository"] != "frye/pets-devsecops-workshop-template"
            or template["version"] != manifest["version"]
            or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", template["version"])):
        parser.error("Repository/version metadata is inconsistent.")
    for name, expected in manifest["fingerprints"].items():
        if digest((ROOT / name).read_bytes().replace(b"\r\n", b"\n")) != expected:
            parser.error(f"Training baseline drift: {name}. Review the source pin before updating.")
    files = source_files()
    kit_inventory = {p.relative_to(KIT).as_posix(): digest(p.read_bytes())
                     for p in files if KIT in p.parents and p != manifest_path}
    if args.refresh_manifest:
        manifest["inventory"] = kit_inventory
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        template["inventory"] = {
            p.relative_to(ROOT).as_posix(): digest(p.read_bytes())
            for p in files if p != template_path}
        template_path.write_text(json.dumps(template, indent=2) + "\n")
    actual = {p.relative_to(ROOT).as_posix(): digest(p.read_bytes())
              for p in files if p != template_path}
    if actual != template["inventory"] or kit_inventory != manifest["inventory"]:
        parser.error("Inventory is stale; review changes and refresh it explicitly.")
    output.mkdir(parents=True, exist_ok=True)
    basename = "pets-devsecops-workshop-template-" + template["version"]
    archive = output / (basename + ".zip")
    with ZipFile(archive, "w", compression=ZIP_DEFLATED, compresslevel=9) as bundle:
        for path in files:
            name = path.relative_to(ROOT).as_posix()
            info = ZipInfo(basename + "/" + name, (2026, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (0o100755 if path.stat().st_mode & 0o111 else 0o100644) << 16
            bundle.writestr(info, path.read_bytes())
    checksum = digest(archive.read_bytes())
    archive.with_suffix(".zip.sha256").write_text(f"{checksum}  {archive.name}\n")
    print(archive)
    print("SHA-256:", checksum)
    print("Local template artifact only; no publication or live-readiness claim.")


if __name__ == "__main__":
    main()
