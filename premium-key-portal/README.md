# JAXO Premium key portal (Cloudflare Worker)

This is a small server-side password gate. The password and license key are **Cloudflare Worker secrets**, not stored in this GitHub repository or in the webpage source.

## Deploy it

1. Create a free account at https://dash.cloudflare.com/ and open **Workers & Pages**.
2. Create a Worker named `jaxo-premium-key`.
3. Open its editor and replace the starter code with the contents of `worker.js` from this folder. Deploy once.
4. Open the Worker settings and add these two **secrets** (not plain text variables):
   - `PORTAL_PASSWORD` — enter the password you want users to type.
   - `PREMIUM_KEY` — enter the JAXO premium key.
5. Deploy again if the dashboard asks, then open the Worker URL ending in `.workers.dev`.

You can also deploy from a terminal with Wrangler:
```bash
npm install -g wrangler
wrangler login
cd premium-key-portal
wrangler deploy
wrangler secret put PORTAL_PASSWORD
wrangler secret put PREMIUM_KEY
``
When prompted, type each value directly into the terminal. Do not paste secrets into GitHub, chat, or source files.

## Share the link

Share the Worker URL with users. They enter the portal password, copy the key, then run `/license` inside JAXO.

## Important security notes

- Use a long, unique portal password and share it privately. Anyone who knows it can retrieve the shared key.
- Add a Cloudflare rate-limiting rule for `POST /unlock` to slow password guessing.
- The JAXO client is a local app; a determined user can patch local premium checks. This portal controls distribution, not paid-license enforcement.
- The repository's earlier Git history already contained the old plaintext premium key. Removing it from the current source does not erase old commits or copies. Treat that old key as exposed if the repository is public; rotating it requires changing the app's verification hash and the Worker secret together.
