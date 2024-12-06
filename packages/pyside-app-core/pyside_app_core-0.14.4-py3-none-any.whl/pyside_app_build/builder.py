import platform
import re
import shutil
import subprocess
import tarfile
import zipfile
from collections.abc import Callable
from pathlib import Path
from typing import Any

from hatchling.builders.config import BuilderConfig
from hatchling.builders.plugin.interface import BuilderInterface
from hatchling.plugin.manager import PluginManager

from pyside_app_build._custom_icon_gen import assert_icon_size, generate_project_icon
from pyside_app_build._exception import PySideBuildError
from pyside_app_build._pysidedeploy_spec_gen import build_deploy_spec
from pyside_app_build.config import PySideAppBuildConfig


class PySideAppBuilder(BuilderInterface[PySideAppBuildConfig, PluginManager]):
    PLUGIN_NAME = "pyside-app"

    @classmethod
    def get_config_class(cls) -> type[BuilderConfig]:
        return PySideAppBuildConfig

    # --------------------------------------------------------------------------

    def clean(self, _: str, __: list[str]) -> None:
        self._clean()

    def _clean(self) -> None:
        shutil.rmtree(self.config.dist_dir, ignore_errors=True)
        shutil.rmtree(self.config.build_dir, ignore_errors=True)
        self.config.dist_dir.mkdir(exist_ok=True)
        self.config.build_dir.mkdir(exist_ok=True)

    # --------------------------------------------------------------------------

    def get_version_api(self) -> dict[str, Callable[..., str]]:
        return {
            "standard": self._build_standard,
            "debug": self._build_debug,
        }

    # --------------------------------------------------------------------------

    def _build_debug(self, _: str, **__: Any) -> str:
        return self._build_standard(_, **__)

    def _build_standard(self, _: str, **__: Any) -> str:
        self._clean()

        self.app.display_debug("Building PySide App...")

        if not self.config.icon.exists():
            generate_project_icon(self.config.icon, self.config.entrypoint)
        else:
            assert_icon_size(self.config.icon)

        spec_file = self._gen_spec_file()
        bundle_tmp = self._pyside_deploy(spec_file)

        app_build_bundle = self.config.build_dir / bundle_tmp.name

        shutil.move(bundle_tmp, app_build_bundle)
        shutil.move(self.config.spec_root / "deployment", self.config.build_dir / "deployment")
        shutil.move(self.config.spec_root / "compilation-report.xml", self.config.build_dir / "compilation-report.xml")

        self.app.display_debug("Packaging App Executable...")
        match plat := platform.system():
            case "Darwin":
                artifact = self._bundle_macos(app_build_bundle)
            case "Linux":
                artifact = self._bundle_linux(app_build_bundle)
            case "Windows":
                artifact = self._bundle_windows(app_build_bundle)
            case _:
                raise PySideBuildError(f"Unsupported platform: {plat}")

        return str(artifact)

    # --------------------------------------------------------------------------

    def _gen_spec_file(self) -> Path:
        return build_deploy_spec(
            self.config.spec_root,
            entrypoint=self.config.entrypoint,
            icon=self.config.icon,
            extra_python_packages=self.config.extra_python_packages,
            extra_qt_modules=self.config.extra_qt_modules,
            extra_qt_plugins=self.config.extra_qt_plugins,
            macos_permissions=self.config.macos_permissions,
            extra_package_data=self.config.extra_package_data,
            extra_data_dirs=self.config.extra_data_dirs,
        )

    def _pyside_deploy(self, spec_file: Path) -> Path:
        match plat := platform.system():
            case "Darwin":
                mode = "standalone"
            case "Linux":
                mode = "onefile"
            case "Windows":
                mode = "onefile"
            case _:
                raise PySideBuildError(f"Unsupported platform: {plat}")

        out = subprocess.run(
            [
                "pyside6-deploy",
                "--force",
                "--mode",
                mode,
                "--keep-deployment-files",
                "--c",
                str(spec_file),
            ],
            text=True,
            cwd=str(spec_file.parent),
            capture_output=True,
            check=True,
        )

        if self.app.verbosity >= 1:
            print(out.stdout)
            print(out.stderr)

        if out.returncode != 0:
            raise PySideBuildError(f"PySide Deploy failed: {out.stderr}")

        match_lines = re.findall(r"\[DEPLOY] Executed file created in (.+)", out.stdout, re.MULTILINE)
        if not match_lines:
            raise PySideBuildError(f"Failed to find output file in text: {out.stdout}")

        app_bundle = match_lines[0]

        self.app.display_debug(f'---> "{app_bundle}"')

        return Path(app_bundle)

    def _bundle_macos(
        self,
        app: Path,
    ) -> Path:
        app_name = app.name
        dmg_name = app_name.replace(".app", ".dmg")

        dmg_source = app.parent / dmg_name
        dmg_target = self.config.dist_dir / dmg_name
        dmg_target.unlink(missing_ok=True)

        out = subprocess.run(
            [
                "hdiutil",
                "create",
                "-volname",
                app_name,
                "-srcfolder",
                app_name,
                "-ov",
                "-format",
                "UDZO",
                dmg_name,
            ],
            text=True,
            cwd=str(app.parent),
            capture_output=True,
            check=False,
        )

        if self.app.verbosity >= 1:
            print(out.stdout)

        if out.returncode != 0:
            raise PySideBuildError(f"DMG Packaging failed: {out.stderr}")

        shutil.move(dmg_source, dmg_target)

        return dmg_target

    def _bundle_linux(
        self,
        bundle: Path,
    ) -> Path:
        tar_target = self.config.dist_dir / f"{self.metadata.name}-linux.tar.gz"

        with tarfile.open(tar_target, "w:gz") as tar:
            tar.add(bundle, arcname=bundle.name.removesuffix(".bin"))

        return tar_target

    def _bundle_windows(self, bundle: Path) -> Path:
        zip_target = self.config.dist_dir / f"{self.metadata.name}-win.zip"

        with zipfile.ZipFile(zip_target, "w") as zip:
            zip.write(bundle, arcname=bundle.name)

        return zip_target
