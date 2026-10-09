# Javier Masonry Service (test site)

Static website, English, no build step needed to view it. Open `index.html` or serve the folder with any static host.

## Structure
- `index.html`, `outdoor-kitchens.html`, `services.html`, `gallery.html`, `about.html`, `contact.html`
- City pages: `katy-tx.html`, `cypress-tx.html`, `tomball-tx.html`, `houston-tx.html`
- `thanks.html` (form confirmation), `404.html`
- `assets/css/style.css`, `assets/js/main.js`

## Quote form
Uses Web3Forms (`https://api.web3forms.com/submit`). The access key is in each form as a hidden `access_key` field (it is public by design). Subject: `NEW QUOTE REQUEST`. Submissions currently go to the email the key was created with (test account).
To switch to Javier's email, create a new access key with his address and replace the value everywhere it appears.

## Photos
Hosted on Cloudinary (`kat6qihq`), delivered with `f_auto,q_auto` and a width limit. Folders are not part of the URLs.

## Landing page for Google Ads
- `lp-outdoor-kitchens.html` (noindex, no menu, one service) and `lp-thanks.html` (conversion page).
- Form subject: `NEW QUOTE REQUEST - Outdoor Kitchen (Google Ads)`. It also captures `gclid` and `utm_*` from the ad URL.
- Paste the Google Ads global site tag where the HTML comment says so in both files, and the conversion event in `lp-thanks.html`.
- Suggested final URL for the ad: `/lp-outdoor-kitchens.html`. Add more kitchen photos in `tools/build.py` (`page_lp_kitchens`) when Javier sends them.

## Regenerating the pages
`python3 tools/build.py` rewrites all HTML files from the data in that script (phone, email, hours, photos, copy).

## Before going live
- Add the real domain: canonical URL, `og:url`, sitemap.xml.
- Do not mention license or insurance unless the client provides them.
