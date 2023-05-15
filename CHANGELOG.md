# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).


## [Unreleased]

### Added

* feature: toggling between endianness
* feature: allow selecting bit-depth of exported integers: 16, 24
* descriptions for operators (buttons)


### Changed

* Addon name


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
