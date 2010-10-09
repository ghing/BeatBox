BEGIN;
CREATE TABLE "core_communityarea" (
    "id" serial NOT NULL PRIMARY KEY,
    "area_number" varchar(2) NOT NULL,
    "community" varchar(80) NOT NULL
)
;
CREATE TABLE "core_station" (
    "id" serial NOT NULL PRIMARY KEY,
    "shortname" varchar(20) NOT NULL,
    "name" varchar(50) NOT NULL,
    "lines" varchar(50) NOT NULL,
    "address" varchar(50) NOT NULL,
    "ada" integer NOT NULL,
    "legend" varchar(5) NOT NULL,
    "alt_legend" varchar(5) NOT NULL,
    "weblink" varchar(250) NOT NULL
)
;
SELECT AddGeometryColumn('core_communityarea', 'geom', 4269, 'POLYGON', 2);
ALTER TABLE "core_communityarea" ALTER "geom" SET NOT NULL;
CREATE INDEX "core_communityarea_geom_id" ON "core_communityarea" USING GIST ( "geom" GIST_GEOMETRY_OPS );
SELECT AddGeometryColumn('core_station', 'geom', 4269, 'POINT', 2);
ALTER TABLE "core_station" ALTER "geom" SET NOT NULL;
CREATE INDEX "core_station_geom_id" ON "core_station" USING GIST ( "geom" GIST_GEOMETRY_OPS );
INSERT into spatial_ref_sys (srid, auth_name, auth_srid, proj4text, srtext) values ( 9102671, 'esri', 102671, '+proj=tmerc +lat_0=36.66666666666666 +lon_0=-88.33333333333333 +k=0.9999749999999999 +x_0=300000 +y_0=0 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs ', 'PROJCS["NAD_1983_StatePlane_Illinois_East_FIPS_1201_Feet",GEOGCS["GCS_North_American_1983",DATUM["North_American_Datum_1983",SPHEROID["GRS_1980",6378137,298.257222101]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",984249.9999999999],PARAMETER["False_Northing",0],PARAMETER["Central_Meridian",-88.33333333333333],PARAMETER["Scale_Factor",0.999975],PARAMETER["Latitude_Of_Origin",36.66666666666666],UNIT["Foot_US",0.30480060960121924],AUTHORITY["EPSG","102671"]]');
COMMIT;
