const PAGE = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>JAXO Premium Key</title>
<style>
:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;min-height:100vh;display:grid;place-items:center;background:#090d18;color:#edf2ff;font:16px system-ui,sans-serif;padding:24px}.card{width:min(100%,440px);padding:32px;border:1px solid #293653;border-radius:20px;background:#111a2d;box-shadow:0 20px 70px #0008}h1{margin:0 0 8px;font-size:28px}p{color:#aab7d0;line-height:1.5}label{display:block;margin:22px 0 8px}input{width:100%;padding:13px;border-radius:10px;border:1px solid #435273;background:#080f20;color:white;font-size:16px}button{margin-top:14px;width:100%;padding:13px;border:0;border-radius:10px;background:#3978f6;color:white;font-weight:700;font-size:16px;cursor:pointer}button:disabled{opacity:.6;cursor:wait}.key{display:none;margin-top:22px;padding:16px;border:1px solid #365b9b;border-radius:12px;background:#0a1428;overflow-wrap:anywhere}.key code{font-size:18px;letter-spacing:1px}.error{color:#ff9b9b;min-height:24px}.small{font-size:12px;color:#7f8da8;margin-top:22px}
</style>
</head>
<body><main class="card">
<h1>JAXO Premium</h1>
<p>Enter the access password to reveal the JAXO Premium license key.</p>
<form id="form"><label for="password">Access password</label><input id="password" type="password" autocomplete="current-password" required><button id="submit" type="submit">Unlock key</button></form>
<p class="error" id="error" role="alert"></p>
<section class="key" id="keybox"><p>Your JAXO Premium key:</p><code id="key"></code><button id="copy" type="button">Copy key</button><p>In JAXO, run <b>/license</b> and enter this key.</p></section>
<p class="small">Only use this page if you trust the person who shared it with you.</p>
</main>
<script>
const form=document.querySelector("#form"),button=document.querySelector("#submit"),error=document.querySelector("#error"),keybox=document.querySelector("#keybox"),keytext=document.querySelector("#key");
form.addEventListener("submit",async e=>{e.preventDefault();button.disabled=true;error.textContent="";keybox.style.display="none";try{const response=await fetch("/unlock",{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify({password:document.querySelector("#password").value})});const data=await response.json();if(!response.ok)throw new Error(data.error||"Could not unlock the key.");keytext.textContent=data.key;keybox.style.display="block";form.reset()}catch(err){error.textContent=err.message}finally{button.disabled=false}});
document.querySelector("#copy").addEventListener("click",async()=>{try{await navigator.clipboard.writeText(keytext.textContent);document.querySelector("#copy").textContent="Copied!"}catch{error.textContent="Copy failed. Select and copy the key manually."}});
</script></body></html>`;

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const headers = {
      "Cache-Control": "no-store, max-age=0",
      "X-Content-Type-Options": "nosniff",
      "Referrer-Policy": "no-referrer",
      "X-Frame-Options": "DENY",
      "Content-Security-Policy": "default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; connect-src 'self'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'"
    };

    if (request.method === "GET" && url.pathname === "/") {
      return new Response(PAGE, { headers: { ...headers, "Content-Type": "text/html; charset=utf-8" } });
    }

    if (request.method === "POST" && url.pathname === "/unlock") {
      if (!env.PORTAL_PASSWORD || !env.PREMIUM_KEY) {
        return Response.json({ error: "Portal is not configured yet." }, { status: 503, headers });
      }
      let body;
      try { body = await request.json(); }
      catch { return Response.json({ error: "Invalid request." }, { status: 400, headers }); }

      if (typeof body.password !== "string" || body.password !== env.PORTAL_PASSWORD) {
        return Response.json({ error: "Incorrect password. Try again." }, { status: 401, headers });
      }
      return Response.json({ key: env.PREMIUM_KEY }, { headers });
    }

    return new Response("Not found", { status: 404, headers });
  }
};
