# Changelog

<!--next-version-placeholder-->

## v0.3.2 (2024-11-21)

### Fix

* Remove unused `yarl` dependency ([`10df86c`](https://github.com/educationwarehouse/edwh-files-plugin/commit/10df86c9a59d91dab00132745261a49d91665f9c))

## v0.3.1 (2024-07-18)

### Fix

* Improved type hints, code style etc ([`1bb1c45`](https://github.com/educationwarehouse/edwh-files-plugin/commit/1bb1c451d8e8ad1fe5b918adbbe022939580d878))

## v0.3.0 (2024-07-02)

### Feature

* Use `requests_toolbelt` to also show progress bar for upload ([`f0880c7`](https://github.com/educationwarehouse/edwh-files-plugin/commit/f0880c75a166594dbd75c97b359661e403053ed3))
* Show spinning animation on slow tasks where progress bar isn't really possible (zip, upload) ([`b6d4ac7`](https://github.com/educationwarehouse/edwh-files-plugin/commit/b6d4ac7607c75bba5e32c2d9f28cfe70bbef51c3))

## v0.2.0 (2024-03-07)

### Feature

* **upload:** Allow sending (zipped) directories ([`ea59803`](https://github.com/educationwarehouse/edwh-files-plugin/commit/ea59803fc417b965d19fa6acb5cba81eec9d3916))

## v0.1.5 (2023-10-03)
### Fix
* **download:** Progress bar was unresponsive, now it works again ([`57283b4`](https://github.com/educationwarehouse/edwh-files-plugin/commit/57283b491f89dcd97956ac5d29cbb0074776e961))

## v0.1.4 (2023-09-20)
### Fix
* Re-add rich as dependency ([`dc6037a`](https://github.com/educationwarehouse/edwh-files-plugin/commit/dc6037ac03f6c897763ccf3d90ec6ecef9b5f525))

## v0.1.3 (2023-09-19)
### Performance
* Replaced rich.progress with simpler progress.Bar ([`e874297`](https://github.com/educationwarehouse/edwh-files-plugin/commit/e8742972bd6dfd3476b23a3fe14aa43fa1bda4f8))

## v0.1.2 (2023-09-19)
### Performance
* **httpx:** Replaced httpx with requests because the import was very slow (150ms) ([`b7f21c9`](https://github.com/educationwarehouse/edwh-files-plugin/commit/b7f21c968e3aa52989a88888dbfabded88a89e7d))

## v0.1.1 (2023-08-02)
### Fix
* Show download_url and delete_url for ease of use, minor refactoring ([`ac28453`](https://github.com/educationwarehouse/edwh-files-plugin/commit/ac28453bebc6769185af6517424f4d58ace566a8))

## v0.1.0 (2023-06-19)
### Feature
* Initial version ([`3d26441`](https://github.com/educationwarehouse/edwh-files-plugin/commit/3d26441ebe3ee538a02731aff8eb1df8fef9a50e))