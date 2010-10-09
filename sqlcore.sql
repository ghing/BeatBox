BEGIN;
INSERT into spatial_ref_sys (srid, auth_name, auth_srid, proj4text, srtext) values ( 9102671, 'esri', 102671, '+proj=tmerc +lat_0=36.66666666666666 +lon_0=-88.33333333333333 +k=0.9999749999999999 +x_0=300000 +y_0=0 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs ', 'PROJCS["NAD_1983_StatePlane_Illinois_East_FIPS_1201_Feet",GEOGCS["GCS_North_American_1983",DATUM["North_American_Datum_1983",SPHEROID["GRS_1980",6378137,298.257222101]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",984249.9999999999],PARAMETER["False_Northing",0],PARAMETER["Central_Meridian",-88.33333333333333],PARAMETER["Scale_Factor",0.999975],PARAMETER["Latitude_Of_Origin",36.66666666666666],UNIT["Foot_US",0.30480060960121924],AUTHORITY["EPSG","102671"]]');
CREATE TABLE "core_communityarea" (
    "id" serial NOT NULL PRIMARY KEY,
    "area_number" varchar(2) NOT NULL,
    "community" varchar(80) NOT NULL,
	geom geometry NOT NULL,
    CONSTRAINT enforce_dims_geom CHECK ((st_ndims(geom) = 2)),
    CONSTRAINT enforce_geotype_geom CHECK (((geometrytype(geom) = 'POLYGON'::text) OR (geom IS NULL))),
    CONSTRAINT enforce_srid_geom CHECK ((st_srid(geom) = 102671))
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
    "weblink" varchar(250) NOT NULL,
	geom geometry NOT NULL,
    CONSTRAINT enforce_dims_geom CHECK ((st_ndims(geom) = 2)),
    CONSTRAINT enforce_geotype_geom CHECK (((geometrytype(geom) = 'POLYGON'::text) OR (geom IS NULL))),
    CONSTRAINT enforce_srid_geom CHECK ((st_srid(geom) = 102671))
)
;
CREATE TABLE "core_wards" (
    "id" serial NOT NULL PRIMARY KEY,
    "data_admin" double precision NOT NULL,
    "perimeter" double precision NOT NULL,
    "ward" varchar(4) NOT NULL,
    "alderman" varchar(60) NOT NULL,
    "thisclass" varchar(2) NOT NULL,
    "ward_phone" varchar(12) NOT NULL,
    "hall_phone" varchar(12) NOT NULL,
    "hall_offic" varchar(45) NOT NULL,
    "address" varchar(39) NOT NULL,
    "edit_date1" varchar(10) NOT NULL,
    "shape_area" double precision NOT NULL,
    "shape_len" double precision NOT NULL,
	geom geometry NOT NULL,
    CONSTRAINT enforce_dims_geom CHECK ((st_ndims(geom) = 2)),
    CONSTRAINT enforce_geotype_geom CHECK (((geometrytype(geom) = 'POLYGON'::text) OR (geom IS NULL))),
    CONSTRAINT enforce_srid_geom CHECK ((st_srid(geom) = 102671))
)
;
CREATE TABLE "core_cpdareas" (
    "id" serial NOT NULL PRIMARY KEY,
    "objectid" integer NOT NULL,
    "area_num" varchar(1) NOT NULL,
    "shape_area" double precision NOT NULL,
    "shape_len" double precision NOT NULL,
	geom geometry NOT NULL,
    CONSTRAINT enforce_dims_geom CHECK ((st_ndims(geom) = 2)),
    CONSTRAINT enforce_geotype_geom CHECK (((geometrytype(geom) = 'POLYGON'::text) OR (geom IS NULL))),
    CONSTRAINT enforce_srid_geom CHECK ((st_srid(geom) = 102671))
)
;
CREATE TABLE "core_cpdbeats" (
    "id" serial NOT NULL PRIMARY KEY,
    "objectid" integer NOT NULL,
    "district" varchar(2) NOT NULL,
    "sector" varchar(1) NOT NULL,
    "beat" varchar(1) NOT NULL,
    "beat_num" varchar(4) NOT NULL,
    "shape_area" double precision NOT NULL,
    "shape_len" double precision NOT NULL,
	geom geometry NOT NULL,
    CONSTRAINT enforce_dims_geom CHECK ((st_ndims(geom) = 2)),
    CONSTRAINT enforce_geotype_geom CHECK (((geometrytype(geom) = 'POLYGON'::text) OR (geom IS NULL))),
    CONSTRAINT enforce_srid_geom CHECK ((st_srid(geom) = 102671))
)
;
CREATE TABLE "core_cpddistricts" (
    "id" serial NOT NULL PRIMARY KEY,
    "objectid" integer NOT NULL,
    "dist_label" varchar(16) NOT NULL,
    "dist_num" varchar(2) NOT NULL,
    "pdf" varchar(20) NOT NULL,
    "district" varchar(3) NOT NULL,
    "shape_area" double precision NOT NULL,
    "shape_len" double precision NOT NULL,
	geom geometry NOT NULL,
    CONSTRAINT enforce_dims_geom CHECK ((st_ndims(geom) = 2)),
    CONSTRAINT enforce_geotype_geom CHECK (((geometrytype(geom) = 'POLYGON'::text) OR (geom IS NULL))),
    CONSTRAINT enforce_srid_geom CHECK ((st_srid(geom) = 102671))
)
;
CREATE TABLE "core_neighborhoods" (
    "id" serial NOT NULL PRIMARY KEY,
    "objectid" integer NOT NULL,
    "pri_neigh_field" varchar(3) NOT NULL,
    "pri_neigh" varchar(50) NOT NULL,
    "sec_neigh_field" varchar(3) NOT NULL,
    "sec_neigh" varchar(50) NOT NULL,
    "shape_area" double precision NOT NULL,
    "shape_len" double precision NOT NULL,
	geom geometry NOT NULL,
    CONSTRAINT enforce_dims_geom CHECK ((st_ndims(geom) = 2)),
    CONSTRAINT enforce_geotype_geom CHECK (((geometrytype(geom) = 'POLYGON'::text) OR (geom IS NULL))),
    CONSTRAINT enforce_srid_geom CHECK ((st_srid(geom) = 102671))
)
;
CREATE TABLE "core_podcamera" (
    "objid" serial NOT NULL PRIMARY KEY,
    "address" varchar(255) NOT NULL,
    "installdate" date NOT NULL,
    "wardIntersection_id" integer REFERENCES "core_wards" ("id") DEFERRABLE INITIALLY DEFERRED,
    "neighborhoodIntersection_id" integer REFERENCES "core_neighborhoods" ("id") DEFERRABLE INITIALLY DEFERRED,
    "cpdAreaIntersection_id" integer REFERENCES "core_cpdareas" ("id") DEFERRABLE INITIALLY DEFERRED,
    "cpdBeatIntersection_id" integer REFERENCES "core_cpdbeats" ("id") DEFERRABLE INITIALLY DEFERRED,
    "cpdDistrictIntersection_id" integer REFERENCES "core_cpddistricts" ("id") DEFERRABLE INITIALLY DEFERRED,
    "communityIntersection_id" integer REFERENCES "core_communityarea" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "core_crimeinstance" (
    "objid" serial NOT NULL PRIMARY KEY,
    "address" varchar(255) NOT NULL,
    "crimedate" timestamp with time zone NOT NULL,
    "casenumber" varchar(10) NOT NULL,
    "crimetype" varchar(64) NOT NULL,
    "secondcrimetype" varchar(128) NOT NULL,
    "place" varchar(64) NOT NULL,
    "domestic" boolean NOT NULL,
    "wardIntersection_id" integer REFERENCES "core_wards" ("id") DEFERRABLE INITIALLY DEFERRED,
    "neighborhoodIntersection_id" integer REFERENCES "core_neighborhoods" ("id") DEFERRABLE INITIALLY DEFERRED,
    "cpdAreaIntersection_id" integer REFERENCES "core_cpdareas" ("id") DEFERRABLE INITIALLY DEFERRED,
    "cpdBeatIntersection_id" integer REFERENCES "core_cpdbeats" ("id") DEFERRABLE INITIALLY DEFERRED,
    "cpdDistrictIntersection_id" integer REFERENCES "core_cpddistricts" ("id") DEFERRABLE INITIALLY DEFERRED,
    "communityIntersection_id" integer REFERENCES "core_communityarea" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
SELECT AddGeometryColumn('core_podcamera', 'geom', 4326, 'POINT', 2);
ALTER TABLE "core_podcamera" ALTER "geom" SET NOT NULL;
CREATE INDEX "core_podcamera_geom_id" ON "core_podcamera" USING GIST ( "geom" GIST_GEOMETRY_OPS );
SELECT AddGeometryColumn('core_crimeinstance', 'geom', 4326, 'POINT', 2);
CREATE INDEX "core_crimeinstance_geom_id" ON "core_crimeinstance" USING GIST ( "geom" GIST_GEOMETRY_OPS );
CREATE INDEX "core_podcamera_wardIntersection_id" ON "core_podcamera" ("wardIntersection_id");
CREATE INDEX "core_podcamera_neighborhoodIntersection_id" ON "core_podcamera" ("neighborhoodIntersection_id");
CREATE INDEX "core_podcamera_cpdAreaIntersection_id" ON "core_podcamera" ("cpdAreaIntersection_id");
CREATE INDEX "core_podcamera_cpdBeatIntersection_id" ON "core_podcamera" ("cpdBeatIntersection_id");
CREATE INDEX "core_podcamera_cpdDistrictIntersection_id" ON "core_podcamera" ("cpdDistrictIntersection_id");
CREATE INDEX "core_podcamera_communityIntersection_id" ON "core_podcamera" ("communityIntersection_id");
CREATE INDEX "core_crimeinstance_wardIntersection_id" ON "core_crimeinstance" ("wardIntersection_id");
CREATE INDEX "core_crimeinstance_neighborhoodIntersection_id" ON "core_crimeinstance" ("neighborhoodIntersection_id");
CREATE INDEX "core_crimeinstance_cpdAreaIntersection_id" ON "core_crimeinstance" ("cpdAreaIntersection_id");
CREATE INDEX "core_crimeinstance_cpdBeatIntersection_id" ON "core_crimeinstance" ("cpdBeatIntersection_id");
CREATE INDEX "core_crimeinstance_cpdDistrictIntersection_id" ON "core_crimeinstance" ("cpdDistrictIntersection_id");
CREATE INDEX "core_crimeinstance_communityIntersection_id" ON "core_crimeinstance" ("communityIntersection_id");
COMMIT;
