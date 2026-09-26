# Deploy ResuTrack

## 1. Publish the repository to GitHub

Create a **public** GitHub repository, then upload this project to its `main` branch. Do not upload a `.env` file or `.streamlit/secrets.toml` file.

## 2. Deploy the Streamlit evaluator

1. Open [Streamlit Community Cloud](https://share.streamlit.io/) and choose **Create app**.
2. Select the GitHub repository, the `main` branch, and `streamlit_app.py` as the entrypoint.
3. In **Advanced settings → Secrets**, add your Gemini key:

```toml
GOOGLE_API_KEY = "your-gemini-api-key"
```

4. Deploy and copy the resulting `https://…streamlit.app` URL.
5. In `deploy-config.js`, replace `https://YOUR-STREAMLIT-APP.streamlit.app` with that URL, then commit and push.

## 3. Publish the marketing site with GitHub Pages

In the GitHub repository, open **Settings → Pages**. Under **Build and deployment**, choose **Deploy from a branch**, then select `main` and `/(root)`, and save.

GitHub will show the published site URL, normally `https://<your-username>.github.io/<repository>/`.

## Deployment notes

- GitHub Pages hosts only the static website. It cannot run `streamlit_app.py`.
- Streamlit Community Cloud runs the analysis app and reads `GOOGLE_API_KEY` from its secret settings.
- The current demo login checks a hard-coded browser-side username/password. Replace it with proper server-side authentication before any production launch.
