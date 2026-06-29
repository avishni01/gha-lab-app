from fastapi import FastAPI, HTTPException

from app.config import APP_NAME, APP_VERSION, get_app_env

app = FastAPI(title=APP_NAME, version=APP_VERSION)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"name": APP_NAME, "version": APP_VERSION}


@app.get("/health")
def read_health() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/config-check")
def read_config_check() -> dict[str, str | bool | None]:
    app_env = get_app_env()
    return {
        "variable": "APP_ENV",
        "configured": app_env is not None,
        "value": app_env,
    }


@app.get("/fail-demo")
def read_fail_demo() -> None:
    raise HTTPException(
        status_code=500,
        detail="Intentional failure for GitHub Actions debugging practice.",
    )

