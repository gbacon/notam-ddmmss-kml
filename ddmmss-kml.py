#! /usr/bin/python

import argparse
from lxml import etree
import os
import re
import simplekml
from typing import List, Tuple

class GeoNotam:
  id: str = ...
  lat: float = ...
  lon: float = ...

  def __init__(self, id, lat, lon):
    def dd(d, m, s, h):
      val = float(d) + (float(m)/60) + (float(s)/3600)
      if h in ('S','W'): val = -1 * val
      return val
    self.lat = dd(*lat)
    self.lon = dd(*lon)
    self.id = id

  def ident(self): return self.id

  def coordinates_z(self) -> Tuple[float, float, float]:
    return (self.lon, self.lat, 0.0)  # KML order

  def __str__(self):
    return f'{self.id}: {self.lat},{self.lon}'

  @staticmethod
  def from_text(notam: str):
    if m := re.match(r"^(M[0-9]+/[0-9]+)\b", notam):
      id = m.group(1)

      if m := re.search(
          r"\b([0-9]{2}) ([0-9]{2}) ([0-9]{2}(?:\.[0-9]+)?) ?([NS])\b" +
          r"\s+" +
          r"\b([0-9]{2}) ([0-9]{2}) ([0-9]{2}(?:\.[0-9]+)?) ?([EW])\b",
          notam):
        lat = tuple(m.group(i) for i in range(1,5))
        lon = tuple(m.group(i) for i in range(5,9))
        return GeoNotam(id, lat, lon)
      elif m := re.search(
          r"\b([NS])([0-9]{2}) ([0-9]{2})' ([0-9]{2}(?:\.[0-9]+)?)\"" +
          r"\s+" +
          r"\b([EW])([0-9]{2}) ([0-9]{2})' ([0-9]{2}(?:\.[0-9]+)?)\"",
          notam):
        lat = tuple(m.group(i) for i in (2, 3, 4, 1))
        lon = tuple(m.group(i) for i in (6, 7, 8, 5))
        return GeoNotam(id, lat, lon)
    else:
      return None

class Overlay:
  geonotams: List[GeoNotam] = ...

  def __init__(self, data: str):
    self.geonotams = []

    doc = etree.HTML(data)

    for pre in doc.xpath("//table/tr/td/pre"):
      point = GeoNotam.from_text("".join(pre.xpath("text()")))
      if point is not None:
        self.geonotams.append(point)

  def write_kml(self, output: str):
    kml = simplekml.Kml()
    kml.document.name = os.path.basename(output).split('.')[0]

    for n in self.geonotams:
      point = kml.newpoint(name=n.ident())
      point.coords = [n.coordinates_z()]
      point.style.iconstyle.scale = 0.5
      point.style.iconstyle.icon.href = (
        'http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png'
      )

    kml.save(output)

def main(input: str, output: str) -> None:
  try:
    with open(input, "r") as f:
      o = Overlay(f.read())
      o.write_kml(output)
  except FileNotFoundError as e:
    print(e)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    description="Convert FAA NOTAMs with DDMMSS(.ss) to a KML layer"
  )
  parser.add_argument("input", type=str, help="input NOTAMS HTML file")
  parser.add_argument(
    "-o",
    "--output",
    type=str,
    help="output KML file (default: input + .kml)"
  )
  args = parser.parse_args()
  main(args.input, args.input + ".kml" if args.output is None else args.output)