## 0.9.0 (2024-11-23)

### Feat

- support sphinx 8

## 0.8.1 (2024-02-17)

## 0.8.0 (2023-06-28)

### Feat

- cadquery:svg help dropdown
- add option inline-uri to cadquery:svg
- cadquery:svg directive
- cadquery:vtk directive
- stable api for cadquery-{vtk,svg}, cadquery, cq_plot

### Refactor

- use pathlib as_posix()
- fix shadow name from outer scope
- rename help widget to overlay
- make cqgi.cqgi_parse public
- inherit from shphinxdirective
- reduce complexity
- extract figure node assembly
- move vtk json exporter to cqgi module
- move cqgi class to independent module

## 0.7.0 (2023-05-28)

### Feat

- upgrade vtk.js to 28.2.0
- add option color to cadquery-vtk directive

## 0.6.0 (2023-05-17)

### Feat

- add border around svg image

### Fix

- allow sphinx >=5.3.0,<7.0.0

## 0.5.0 (2023-03-05)

### Feat

- vtk.js navigation legend

## 0.4.0 (2023-01-29)

### Feat

- improve cqgi error reporting
- improve cqgi error reporting

### Fix

- remove option "align" from cadquery-svg
- vtk size and align options

### Refactor

- setup assets installed flag
- raise error if no directive content
- common jinja environment config
- rename variable to reflect cadquery.cqgi
- svg error if show_object not called
- compact vtk wrapper json
- reduce complexity

## 0.3.0 (2023-01-22)

### Feat

- cadquery-vtk load source from file
- info message for deprecated directives

### Fix

- padding when source code not displayed

### Refactor

- pep8 naming conventions
- use template engine to create rst
- move rendering js to static file

## 0.2.1 (2023-01-10)

### Fix

- ipython constraint >=7.31.1

## 0.2.0 (2023-01-09)

### Feat

- config value cadquery_include_source
- directive aliases cadquery-svg and cadquery-vtk

### Fix

- vtk.js html template text-align

### Refactor

- remove unused code

## 0.1.0 (2023-01-05)

### Feat

- vtk.js and svg renderers from cq
