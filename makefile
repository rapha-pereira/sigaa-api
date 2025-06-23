# Run the SIGAA API server with auto-reload
# This command runs the SIGAA API server using the Uvicorn ASGI server with auto-reload enabled.
# It starts the server and monitors the source code for changes, automatically restarting the server whenever a change is detected.
run-dev:
	uv run uvicorn sigaa_api.main:app --reload

# Alternative target name for compatibility
run-server:
	uv run uvicorn sigaa_api.main:app --reload
