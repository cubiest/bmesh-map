# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).


## [1.4.0] - 2023-08-28

### Added

* feature: OpenEXR export
* feature: 32-bit `RAW` export


### Changed

* y-axis inversion as a default was removed


### Fixed

* Fix incorrect y-axis mapping on RAW export: y-axis was inverted/flipped


## [1.3.0] - 2023-05-16

### Added

* feature: toggling between endianness
* feature: allow selecting bit-depth of exported integers: 16, 24
* descriptions for operators (buttons)
* errors for invalid export path


### Changed

* Addon name
* Min and Max height Labels are now Entries
* Change Filename Entry to Filepath Entry (enables user to use file dialog to choose save location)


## [1.2.0] - 2023-04-24

### Added

* Version info in the panel footer
* Quality check
  * dimensions: are they equal and power of 2?
  * resolution: is it power of 2 + 1?
  * are vertex positions (object-space) valid and not out-of-bounds?
* Feedback on Success and Error: show in status bar oder as tooltip over button (latter only for errors)


### Changed

* GUI Layout


### Fixed

* When selecting another object, the stats were not updated.


## [1.1.0] - 2023-04-24

### Added

config options
* `Invert Y-axis`
* `Invert X-axis`
  * this one is required to have the same map in Godot (Zylann's Plugin) as in Blender
