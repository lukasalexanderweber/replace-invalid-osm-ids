# replace-invalid-osm-ids
Update invalid (&lt;1) Ids within a OSM file

Using Editors as JSOM store yet not existing OSM IDs as negatives.
However, tools like [osm2pgsql](https://github.com/openstreetmap/osm2pgsql/issues/1097) do not support such negative IDs.

This script updates all invalid IDs to valid IDs.

## Usage

`python replace_invalid_osm_ids.py invalid.osm valid.osm`

<details>
<summary>invalid.osm</summary>

```xml
<?xml version='1.0' encoding='UTF-8'?>
<osm version='0.6' generator='JOSM'>
<bounds minlat='49.00492' minlon='8.43571' maxlat='49.00814' maxlon='8.44413' origin='JOSM' />
<node id='1' version='1' lat='49.00601320632' lon='8.4378525903' />
<node id='2' version='1' lat='49.00600598625' lon='8.43919538768' />
<node id='-111' version='1' lat='49.00600598625' lon='8.440516172' />
<node id='123' version='1' lat='49.00600598625' lon='8.4414957537' />
<node id='-222' version='1' lat='49.00675686751' lon='8.4414957537' />
<way id='-111' version='1'>
  <nd ref='1' />
  <nd ref='123' />
  <tag k='highway' v='primary' />
  <tag k='name' v='Ostring' />
  <tag k='oneway' v='yes' />
</way>
<way id='2' version='1'>
  <nd ref='-111' />
  <nd ref='1' />
  <tag k='highway' v='primary' />
  <tag k='name' v='Ostring' />
  <tag k='oneway' v='yes' />
</way>
<way id='-222' version='1'>
  <nd ref='2' />
  <nd ref='-222' />
  <tag k='highway' v='secondary' />
  <tag k='name' v='Gerwig' />
  <tag k='oneway' v='yes' />
</way>
<relation id="-15" version="1">
  <member type="way" ref="2" role="from"/>
  <member type="way" ref="-222" role="to"/>
  <member type="node" ref="-222" role="via"/>
  <tag k="restriction" v="no_left_turn"/>
  <tag k="type" v="restriction"/>
</relation>
</osm>
```
</details>

<details>
<summary>valid.osm</summary>

```xml
<?xml version="1.0" ?><osm version="0.6" generator="JOSM">
<bounds minlat="49.00492" minlon="8.43571" maxlat="49.00814" maxlon="8.44413" origin="JOSM"/>
<node id="1" version="1" lat="49.00601320632" lon="8.4378525903"/>
<node id="2" version="1" lat="49.00600598625" lon="8.43919538768"/>
<node id="3" version="1" lat="49.00600598625" lon="8.440516172"/>
<node id="123" version="1" lat="49.00600598625" lon="8.4414957537"/>
<node id="4" version="1" lat="49.00675686751" lon="8.4414957537"/>
<way id="1" version="1">
  <nd ref="1"/>
  <nd ref="123"/>
  <tag k="highway" v="primary"/>
  <tag k="name" v="Ostring"/>
  <tag k="oneway" v="yes"/>
</way>
<way id="2" version="1">
  <nd ref="3"/>
  <nd ref="1"/>
  <tag k="highway" v="primary"/>
  <tag k="name" v="Ostring"/>
  <tag k="oneway" v="yes"/>
</way>
<way id="3" version="1">
  <nd ref="2"/>
  <nd ref="4"/>
  <tag k="highway" v="secondary"/>
  <tag k="name" v="Gerwig"/>
  <tag k="oneway" v="yes"/>
</way>
<relation id="1" version="1">
  <member type="way" ref="2" role="from"/>
  <member type="way" ref="3" role="to"/>
  <member type="node" ref="4" role="via"/>
  <tag k="restriction" v="no_left_turn"/>
  <tag k="type" v="restriction"/>
</relation>
</osm>
```
</details>
