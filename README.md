# Plot DD MM SS(.ss) Points from NOTAMs on KML

Remembering and hand-jamming the [lat-lon formats in ForeFlight][fflatlon]
can be a challenge. The code in this repository automates the conversion of
multiple points from NOTAM output to a single KML layer.

# Usage

    ddmmss-kml.py -o layer.kml notams.html

Then load *layer.kml* as a [custom map layer][ffkml].

# Legal Disclaimer

All files are provided for informational purposes only. They are not to
be used for navigation. No claim is made regarding the accuracy of any
generated overlay.

[fflatlon]: https://support.foreflight.com/hc/en-us/articles/204026105-How-do-I-enter-a-latitude-and-longitude-waypoint-
[ffkml]: https://foreflight.com/support/support-center/category/about-foreflight-mobile/360000219488