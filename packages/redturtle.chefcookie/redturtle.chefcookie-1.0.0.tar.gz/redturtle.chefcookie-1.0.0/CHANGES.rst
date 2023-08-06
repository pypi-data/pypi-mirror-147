Changelog
=========

1.0.0 (2022-04-19)
------------------

- Merge analytics and tech cookies labels into functional cookies field.
  [cekk]
- More extensibility for transformers (now you can set a transform for each provider name).
  [cekk]
- Handle recaptcha.
  [cekk]
- policy_url field now can handle multi-language strings.
  [cekk]
- Do not break for iframes without src attribute.
  [cekk]


0.2.3 (2022-03-24)
------------------

- Add flag to control panel that allow to enable cookie banner
- Add cookie prefix to control panel to control the js plugin option
- Allow to select endpoint for consent registry
- Add domain whitelist so in case you have site with multiple domain can show 
  the banner in selected domain
- Add matomo
- Some minor fix to prevent cases where site editor remove configuration lines 
  partially
- Add log tracking to new introduced actions
- Fix problem loading twitter timeline in tile manager from
  redturtle.tiles.management
  [lucabel]
- Do not use $ but vanilla javascript for old Plone sites compatibility.
  [cekk]

0.2.2 (2022-01-27)
------------------

- Align text with label of buttons.
- Removed cookie_setting_open button when only_technical_cookies is checked.
  [eikichi18]


0.2.1 (2022-01-11)
------------------

- Fix layers in adapters.
  [cekk]

0.2.0 (2022-01-11)
------------------

- Add facebook script manually (copied from original chefcookie script).
  [cekk]
- Allow to handle social based on link/script like twitter timeline
  [lucabel]


0.1.3 (2022-01-10)
------------------

- Remove YouTube unused field.
  [cekk]


0.1.2 (2022-01-10)
------------------

- Fix accept_iframe loading.
  [cekk]

0.1.1 (2022-01-10)
------------------

- Fix domain names when saving cookie settings.
  [cekk]


0.1.0 (2022-01-10)
------------------

- Initial release.
  [cekk, lucabel]
