# XDF-Export-Tool
Python tool to export individual streams from an [XDF](https://github.com/sccn/xdf) file into CSV.

This application is based on PyQt5 and runs on Python 3.7.

## Instructions

* Run the XDF_export_tool.py to execute the application and the GUI will be loaded.

* Use the `Select XDF file(s)` button to select one or more XDF files. It is useful to select more than one file if we have, for example, recordings from different participants.

* Write the desired `Stream name` of the stream that will be exported. It has to be written exactly as it was in the LSL stream. This field is mandatory.

* Optionally, write the `Markers stream name`, if the XDF file contains a secondary stream with markers that you would like to export together with the desired stream.

* Optionally, in combination with the previous field, write `Markers to write` to define which markers you would like to write in the resulting file. If `Markers stream name` is written but `Markers to write` is empty, all markers will be written.

* Click the `Export stream(s)` button to export the desired stream from the selected files. The result of the operation will be shown in the `Log` field. The exported CSV files (one per XDF file) will be created in the same folder as the XDF files. The subject number will be appended to the name if the XDF files are named as *-1.xdf, *-2xdf, etc., like `recording-1.xdf`.

# ![Screnshot](https://raw.githubusercontent.com/HectorCarral/XDF-Export-Tool/master/Screenshot.png)
