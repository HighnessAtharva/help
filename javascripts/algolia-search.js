/*
 * Algolia DocSearch v5 for help.accuknox.com.
 *
 * Mounts two widgets:
 *   1. The search button and modal (keyword search plus Ask AI) in #docsearch.
 *   2. The Ask AI sidepanel in #docsearch-sidepanel.
 *
 * The index was built by the Algolia crawler in the generic "pages" shape
 * (title, description, content, url, path). DocSearch expects its own shape
 * (hierarchy.lvl0 to lvl6, type, url), so mapHit() converts each result.
 * Results link to the relative path, so links work on localhost, on preview
 * builds and on production.
 */
(function () {
  "use strict";

  var APP_ID = "YCPZKRYLSM";
  var API_KEY = "920e87f2f06ed2399a7bc102e0e2706b"; // public search-only key
  var INDEX = "help_accuknox_com_ycpzkrylsm_pages";
  var AGENT_ID = "0eb02a08-7cf3-4260-a755-0a8ef9e2f4ad";
  var TITLE_SUFFIX = /\s*\|\s*AccuKnox Docs\s*$/i;

  // Ask AI calls https://ycpzkrylsm.algolia.net/agent-studio/... Some home
  // and office routers fail to resolve that host, so Ask AI shows "Failed to
  // fetch". The -dsn host serves the same Agent Studio API and resolves
  // everywhere search works, so send Ask AI requests there.
  // DocSearch writes the app ID in capitals, so match without case.
  var AGENT_HOST = new RegExp("^https://" + APP_ID + "\\.algolia\\.net/agent-studio/", "i");
  var AGENT_HOST_DSN = "https://" + APP_ID.toLowerCase() + "-dsn.algolia.net/agent-studio/";
  var nativeFetch = window.fetch.bind(window);

  function reroute(url) {
    return url.replace(AGENT_HOST, AGENT_HOST_DSN);
  }

  window.fetch = function (input, init) {
    if (typeof input === "string") {
      input = reroute(input);
    } else if (input instanceof URL) {
      input = reroute(input.href);
    } else if (input instanceof Request && AGENT_HOST.test(input.url)) {
      input = new Request(reroute(input.url), input);
    }
    return nativeFetch(input, init);
  };

  // "getting-started" becomes "Getting Started". The home page becomes "Home".
  function sectionName(path) {
    var first = (path || "/").split("/").filter(Boolean)[0];
    if (!first) return "Home";
    return first
      .split("-")
      .map(function (word) {
        return word.charAt(0).toUpperCase() + word.slice(1);
      })
      .join(" ");
  }

  function relativeUrl(hit) {
    if (hit.path) return hit.path;
    try {
      var u = new URL(hit.url);
      return u.pathname + u.hash;
    } catch (e) {
      return hit.url;
    }
  }

  function value(result) {
    return result && result.value ? result.value : "";
  }

  function mapHit(hit) {
    var hl = hit._highlightResult || {};
    var sn = hit._snippetResult || {};
    var section = sectionName(hit.path);
    var title = (hit.title || "").replace(TITLE_SUFFIX, "");
    var titleHl = (value(hl.title) || title).replace(TITLE_SUFFIX, "");
    var desc = hit.description || "";
    var descHl = value(sn.description) || value(hl.description) || desc;

    var hierarchy = {
      lvl0: section,
      lvl1: desc,
      lvl2: title,
      lvl3: null,
      lvl4: null,
      lvl5: null,
      lvl6: null,
    };

    return Object.assign({}, hit, {
      type: "lvl2",
      url: relativeUrl(hit),
      url_without_anchor: relativeUrl(hit),
      hierarchy: hierarchy,
      content: null,
      _highlightResult: Object.assign({}, hl, {
        hierarchy: {
          lvl0: { value: section, matchLevel: "none", matchedWords: [] },
          lvl1: { value: descHl, matchLevel: "none", matchedWords: [] },
          lvl2: { value: titleHl, matchLevel: "full", matchedWords: [] },
        },
      }),
      _snippetResult: Object.assign({}, sn, {
        hierarchy: {
          lvl1: { value: descHl, matchLevel: "none" },
          lvl2: { value: titleHl, matchLevel: "full" },
        },
      }),
    });
  }

  // DocSearch reads html[data-theme]. Material sets body[data-md-color-scheme].
  function syncTheme() {
    var scheme = document.body.getAttribute("data-md-color-scheme");
    document.documentElement.setAttribute(
      "data-theme",
      scheme === "slate" ? "dark" : "light"
    );
  }

  // Fallback: show the built-in MkDocs search when Algolia is not usable.
  // Add ?search=local to any page URL to force the fallback for testing.
  var HEALTH_URL = "https://" + APP_ID.toLowerCase() + "-dsn.algolia.net/1/isalive";
  var HEALTH_TIMEOUT_MS = 4000;
  var usingFallback = false;

  function useLocalSearch(reason) {
    if (usingFallback) return;
    usingFallback = true;
    document.documentElement.classList.add("ak-search-fallback");
    if (window.console) console.warn("[search] Algolia unavailable, using local search:", reason);
  }

  function checkAlgolia() {
    var timer;
    var timeout = new Promise(function (resolve, reject) {
      timer = setTimeout(function () {
        reject(new Error("health check timed out"));
      }, HEALTH_TIMEOUT_MS);
    });
    var ping = nativeFetch(HEALTH_URL, { mode: "cors", cache: "no-store" }).then(function (res) {
      if (!res.ok) throw new Error("health check returned " + res.status);
    });
    Promise.race([ping, timeout])
      .catch(function (err) {
        useLocalSearch(err.message);
      })
      .then(function () {
        clearTimeout(timer);
      });
  }

  function init() {
    syncTheme();
    new MutationObserver(syncTheme).observe(document.body, {
      attributes: true,
      attributeFilter: ["data-md-color-scheme"],
    });

    if (/[?&]search=local\b/.test(window.location.search)) {
      useLocalSearch("forced by ?search=local");
      return;
    }
    if (!window.docsearch) {
      useLocalSearch("DocSearch script did not load");
      return;
    }

    try {
      window.docsearch({
        container: "#docsearch",
        appId: APP_ID,
        apiKey: API_KEY,
        indices: [
          {
            name: INDEX,
            searchParameters: {
              attributesToRetrieve: ["title", "description", "url", "path"],
              attributesToHighlight: ["title", "description"],
              attributesToSnippet: ["description:24"],
              hitsPerPage: 12,
            },
          },
        ],
        askAi: { agentId: AGENT_ID, indexName: INDEX },
        maxResultsPerGroup: 6,
        placeholder: "Search the AccuKnox docs",
        transformItems: function (items) {
          return items.map(mapHit);
        },
      });
    } catch (err) {
      useLocalSearch("DocSearch failed to start: " + err.message);
      return;
    }

    checkAlgolia();

    // Ask AI is optional. If the sidepanel fails, search keeps working.
    if (window.docsearchSidepanel) {
      try {
        window.docsearchSidepanel({
          container: "#docsearch-sidepanel",
          appId: APP_ID,
          apiKey: API_KEY,
          // The agent's search tool already names the index. Passing
          // "indices" here makes Agent Studio reject the request.
          agentId: AGENT_ID,
        });
      } catch (err) {
        if (window.console) console.warn("[search] Ask AI sidepanel failed:", err.message);
      }
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
