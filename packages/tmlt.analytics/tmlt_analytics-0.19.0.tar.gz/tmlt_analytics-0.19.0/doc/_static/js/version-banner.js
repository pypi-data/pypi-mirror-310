/* SPDX-License-Identifier: CC-BY-SA-4.0 */
/* Copyright Tumult Labs 2024 */

function injectBanner(content) {
  var body = document.getElementsByClassName('bd-article')[0];
  if (body) {
    body.prepend(content);
  } else {
    console.warn("Unable to find body element, skipping banner injection");
  }
}

function init() {
  const banner_config_url = DOCUMENTATION_OPTIONS.URL_ROOT + "banner-config.json";
  fetch(banner_config_url)
    .then((resp) => {
      if (resp.status != 200) {
        throw new Error(
          "Unable to fetch banner configuration, got status code " + resp.status
        );
      }
      return resp.json();
    }).then((config) => {
      if (config.content != null) {
        var banner = document.createElement("div");
        banner.innerHTML = config.content;
        banner.className = "tmlt-banner-warning";
        injectBanner(banner);
      } else {
        console.log("Banner config has no content, not inserting banner")
      }
    }).catch((err) => console.log(err));
}

document.addEventListener("DOMContentLoaded", function () {
  init();
});
