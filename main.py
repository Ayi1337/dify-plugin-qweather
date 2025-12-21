import logging
import os
from pathlib import Path

from dify_plugin import Plugin
from dify_plugin.config.config import DifyPluginEnv


def main() -> None:
    root = Path(__file__).resolve().parent
    os.chdir(root)

    dotenv_path = root / ".env"
    if dotenv_path.exists():
        for line in dotenv_path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            key = key.strip()
            value = value.strip().strip("'").strip('"')
            if key:
                os.environ[key] = value

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("qweather")

    env = DifyPluginEnv()

    try:
        import yaml  # type: ignore

        manifest = yaml.safe_load((root / "manifest.yaml").read_text(encoding="utf-8"))
        provider = yaml.safe_load((root / "qweather.yaml").read_text(encoding="utf-8"))

        logger.info(
            "Loaded manifest (version=%s, meta.version=%s), declared_tools=%s",
            (manifest or {}).get("version"),
            ((manifest or {}).get("meta") or {}).get("version"),
            len((provider or {}).get("tools") or []),
        )
    except Exception as e:
        logger.warning("Failed to load manifest/provider YAML: %s", e)

    remote_target = None
    if getattr(env.INSTALL_METHOD, "value", None) == "remote":
        try:
            install_host, install_port = Plugin._get_remote_install_host_and_port(env)
            remote_target = f"{install_host}:{install_port}"
        except Exception:
            remote_target = None

    logger.info(
        "Starting plugin (cwd=%s, install_method=%s, remote_target=%s, remote_host=%s, remote_port=%s, remote_url=%s, remote_key_set=%s)",
        os.getcwd(),
        env.INSTALL_METHOD,
        remote_target,
        env.REMOTE_INSTALL_HOST,
        env.REMOTE_INSTALL_PORT,
        env.REMOTE_INSTALL_URL,
        bool(env.REMOTE_INSTALL_KEY),
    )

    Plugin(env).run()


if __name__ == "__main__":
    main()
