(() => {
  "use strict";

  const measurementId = "G-JF2J68V0C0";
  const host = window.location.hostname.toLowerCase();
  const isAgentTrustLab = host === "agenttrustlab.com" || host.endsWith(".agenttrustlab.com");
  const platform = isAgentTrustLab ? "Agent Trust Lab" : "RegEvidenceHub";
  const rehHost = host === "regevidencehub.com" || host.endsWith(".regevidencehub.com");
  const privacyUrl = isAgentTrustLab ? "https://agenttrustlab.com/privacy" : "https://regevidencehub.com/privacy/";
  const consentKey = "ga4-analytics-consent-v1";
  const cookieDomain = isAgentTrustLab ? "agenttrustlab.com" : "regevidencehub.com";
  const funnelProducts = new Set(["works_monitoring", "premises_report"]);
  const funnelPrefix = (product) => product === "works_monitoring" ? "works" : "premises";
  let analyticsLoaded = false;

  const readCookie = () => {
    const prefix = "ga4_analytics_consent=";
    const item = document.cookie.split(";").map((part) => part.trim()).find((part) => part.startsWith(prefix));
    return item ? decodeURIComponent(item.slice(prefix.length)) : null;
  };
  const writeCookie = (choice) => {
    document.cookie = `ga4_analytics_consent=${encodeURIComponent(choice)}; Max-Age=15552000; Path=/; Domain=${cookieDomain}; SameSite=Lax; Secure`;
  };
  const readConsent = () => {
    const sharedChoice = readCookie();
    if (sharedChoice === "granted" || sharedChoice === "denied") return sharedChoice;
    try {
      const localChoice = window.localStorage.getItem(consentKey);
      if (localChoice === "granted" || localChoice === "denied") {
        if (rehHost) writeCookie(localChoice);
        return localChoice;
      }
    } catch (_error) { /* Continue with the shared cookie or ask on this page. */ }
    return null;
  };
  const clearAnalyticsCookies = () => {
    const names = document.cookie.split(";").map((part) => part.trim().split("=")[0]);
    for (const name of names) {
      if (!name.startsWith("_ga")) continue;
      document.cookie = `${name}=; Max-Age=0; path=/; SameSite=Lax`;
      document.cookie = `${name}=; Max-Age=0; path=/; domain=${cookieDomain}; SameSite=Lax`;
      document.cookie = `${name}=; Max-Age=0; path=/; domain=.${cookieDomain}; SameSite=Lax`;
    }
  };

  const safePageLocation = (value) => {
    try {
      const url = new URL(value, window.location.origin);
      return url.origin + url.pathname;
    } catch (_error) {
      return window.location.origin + window.location.pathname;
    }
  };

  const emitPendingFunnelEvents = () => {
    if (!analyticsLoaded || typeof window.gtag !== "function") return;
    const page = safePageLocation(window.location.href);
    window.gtag("event", "page_view", {
      page_location: page,
      page_referrer: document.referrer ? safePageLocation(document.referrer) : "",
      page_title: document.title
    });
    document.querySelectorAll("form").forEach((form) => {
      let product = form.getAttribute("data-ga4-funnel-product");
      if (!product && host === "works.regevidencehub.com") {
        try {
          if (new URL(form.action, window.location.origin).pathname === "/monitoring-report/checkout") {
            product = "works_monitoring";
          }
        } catch (_error) { /* Ignore invalid form actions. */ }
      }
      if (!funnelProducts.has(product)) return;
      window.gtag("event", `${funnelPrefix(product)}_report_form_view`, { event_scope: "paid_report_funnel", product_id: product });
      let started = false;
      form.addEventListener("focusin", () => {
        if (readConsent() !== "granted" || started) return;
        started = true;
        window.gtag("event", `${funnelPrefix(product)}_report_form_start`, { event_scope: "paid_report_funnel", product_id: product });
      }, { once: true });
      form.addEventListener("submit", () => {
        if (readConsent() !== "granted") return;
        window.gtag("event", `${funnelPrefix(product)}_checkout_attempt`, { event_scope: "paid_report_funnel", product_id: product });
      });
    });
    document.querySelectorAll("[data-ga4-funnel-cta]").forEach((element) => {
      const product = element.getAttribute("data-ga4-funnel-cta");
      if (!funnelProducts.has(product)) return;
      element.addEventListener("click", () => {
        if (readConsent() !== "granted") return;
        window.gtag("event", `${funnelPrefix(product)}_cta_click`, { event_scope: "paid_report_funnel", product_id: product });
      });
    });
    const confirmedProduct = document.body?.getAttribute("data-ga4-confirmed-product");
    if (funnelProducts.has(confirmedProduct)) {
      window.gtag("event", `${funnelPrefix(confirmedProduct)}_paid_report_displayed`, {
        event_scope: "paid_report_funnel",
        product_id: confirmedProduct
      });
    }
  };

  const loadAnalytics = () => {
    if (analyticsLoaded) {
      window.gtag?.("consent", "update", { analytics_storage: "granted" });
      return;
    }
    analyticsLoaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function gtag() { window.dataLayer.push(arguments); };
    window.gtag("consent", "default", {
      analytics_storage: "denied",
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied"
    });
    window.gtag("js", new Date());
    window.gtag("set", {
      site_platform: platform,
      content_group: platform,
      page_location: safePageLocation(window.location.href),
      page_referrer: document.referrer ? safePageLocation(document.referrer) : ""
    });
    window.gtag("consent", "update", { analytics_storage: "granted" });
    window.gtag("config", measurementId, {
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
      send_page_view: false
    });

    const script = document.createElement("script");
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(measurementId)}`;
    script.referrerPolicy = "strict-origin-when-cross-origin";
    document.head.appendChild(script);
    emitPendingFunnelEvents();
  };

  const saveChoice = (choice) => {
    try { window.localStorage.setItem(consentKey, choice); }
    catch (_error) { /* The current-page choice still applies if storage is unavailable. */ }
    if (rehHost) writeCookie(choice);
    const banner = document.getElementById("ga4-consent-banner");
    if (banner) banner.remove();
    if (choice === "granted") loadAnalytics();
    else {
      window.gtag?.("consent", "update", { analytics_storage: "denied" });
      clearAnalyticsCookies();
    }
    window.dispatchEvent(new CustomEvent("ga4-analytics-consent-change", { detail: { choice } }));
  };

  const showPreferences = (focus = false) => {
    let banner = document.getElementById("ga4-consent-banner");
    if (banner) {
      banner.hidden = false;
      if (focus) banner.querySelector("button")?.focus();
      return;
    }

    const style = document.createElement("style");
    style.id = "ga4-consent-style";
    style.textContent = `
      #ga4-consent-banner{position:fixed;z-index:2147483000;inset:auto 0 0;background:#fff;color:#17212b;border-top:1px solid #cbd5e1;box-shadow:0 -8px 30px rgba(15,23,42,.18);font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
      #ga4-consent-banner .ga4-inner{max-width:1180px;margin:0 auto;padding:18px 24px;display:flex;align-items:center;gap:20px}
      #ga4-consent-banner p{flex:1;margin:0}
      #ga4-consent-banner a{color:#0755a5;text-decoration:underline}
      #ga4-consent-banner .ga4-actions{display:flex;flex-wrap:wrap;gap:10px}
      #ga4-consent-banner button,#ga4-preferences-button{font:inherit;cursor:pointer}
      #ga4-consent-banner button{min-height:42px;padding:8px 14px;border:1px solid #334155;border-radius:6px;background:#fff;color:#17212b;font-weight:650}
      #ga4-consent-banner button[data-ga4-accept]{background:#154f8a;border-color:#154f8a;color:#fff}
      #ga4-preferences-button{margin:6px 10px 0 0;padding:0;border:0;background:transparent;color:inherit;text-decoration:underline}
      @media(max-width:720px){#ga4-consent-banner .ga4-inner{align-items:stretch;flex-direction:column;gap:12px;padding:16px}#ga4-consent-banner .ga4-actions{display:grid;grid-template-columns:1fr 1fr}}
      @media(max-width:420px){#ga4-consent-banner .ga4-actions{grid-template-columns:1fr}}
    `;
    if (!document.getElementById(style.id)) document.head.appendChild(style);

    banner = document.createElement("section");
    banner.id = "ga4-consent-banner";
    banner.setAttribute("role", "region");
    banner.setAttribute("aria-label", "Optional analytics preferences");
    const inner = document.createElement("div");
    inner.className = "ga4-inner";
    const message = document.createElement("p");
    message.append("Optional Google Analytics helps us understand site visits and a small set of product steps. The same measurement ID covers RegEvidenceHub and Agent Trust Lab. We never send form answers, contact details, or case facts. Analytics runs only if you allow it. ");
    const privacyLink = document.createElement("a");
    privacyLink.href = privacyUrl;
    privacyLink.textContent = "Privacy details";
    message.appendChild(privacyLink);

    const actions = document.createElement("div");
    actions.className = "ga4-actions";
    const accept = document.createElement("button");
    accept.type = "button";
    accept.dataset.ga4Accept = "true";
    accept.textContent = "Allow analytics";
    accept.addEventListener("click", () => saveChoice("granted"));
    const reject = document.createElement("button");
    reject.type = "button";
    reject.textContent = "Reject optional analytics";
    reject.addEventListener("click", () => saveChoice("denied"));
    actions.append(accept, reject);
    inner.append(message, actions);
    banner.appendChild(inner);
    document.body.appendChild(banner);
    if (focus) accept.focus();
  };

  const preferenceHost = document.querySelector("footer") || document.body;
  if (!document.getElementById("ga4-preferences-button")) {
    const preferences = document.createElement("button");
    preferences.id = "ga4-preferences-button";
    preferences.type = "button";
    preferences.textContent = "Cookie preferences";
    preferences.setAttribute("aria-label", "Change optional analytics preferences");
    preferences.addEventListener("click", () => showPreferences(true));
    preferenceHost.appendChild(preferences);
  }

  const choice = readConsent();
  if (choice === "granted") loadAnalytics();
  else if (choice !== "denied") showPreferences();
})();
