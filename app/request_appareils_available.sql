# -----------------------------
#VALUES
#TS_DEPART_NV_VOL = '2018-10-18 17:35:00'
#TS_ARRIVEE_NV_VOL = '2018-10-19 05:15:00'
#TPS_VOL = TS_ARRIVEE_NV_VOL - TS_DEPART_NV_VOL
#NB_HEURES_VOL_NV_VOL = INT(TPS_VOL)
#CODE_ORIGINE_NV_VOL = 'CDG'
#CODE_DESTINATION_NV_VOL = 'HDD'

CREATE TEMPORARY TABLE appareils_no_flight 
SELECT immatriculation, type
FROM appareils
WHERE appareils.immatriculation NOT IN (
SELECT immatriculation FROM departs);

# -----------------------------

CREATE TEMPORARY TABLE appareils_next_flight
SELECT immatriculation,
	ts_depart AS ts_depart_next_flight,
	ts_arrivee AS ts_arrivee_next_flight,
        code_origine AS code_origine_next_flight,
        code_destination AS code_destination_next_flight
FROM(

	SELECT appareils_et_vols.immatriculation, 
		appareils_et_vols.ts_depart, 
		appareils_et_vols.ts_arrivee,
		appareils_et_vols.liaison
	FROM (

		SELECT immatriculation, 
			   MIN(ts_depart) as min_ts_depart
		FROM departs
		LEFT JOIN vols ON departs.num_vol = vols.num_vol
		WHERE ts_depart > '2018-10-18 17:35:00'
		GROUP BY immatriculation
	) AS appareils_next_flight
	JOIN (
		SELECT immatriculation, 
			ts_depart,
            ts_arrivee,
			liaison
		FROM departs
		LEFT JOIN vols ON departs.num_vol = vols.num_vol
		) AS appareils_et_vols
			ON appareils_next_flight.immatriculation = appareils_et_vols.immatriculation
			AND appareils_next_flight.min_ts_depart = appareils_et_vols.ts_depart
	) AS full_appareils_et_vols
JOIN liaisons 
	ON full_appareils_et_vols.liaison = liaisons.id_liaison
JOIN (
	SELECT id_aeroports AS id_aeroport_destination, 
		code AS code_destination, 
		nom AS nom_destination 
	FROM airline.aeroports
    ) AS aeroports_destination
 	ON liaisons.aeroport_destination = aeroports_destination.id_aeroport_destination
JOIN (
	SELECT id_aeroports AS id_aeroport_origine, 
		code AS code_origine, 
		nom AS nom_origine FROM airline.aeroports
     ) AS aeroports_origine
 	ON liaisons.aeroport_origine = aeroports_origine.id_aeroport_origine;

# -----------------------------

CREATE TEMPORARY TABLE appareils_last_flight
SELECT immatriculation,
	ts_depart AS ts_depart_last_flight,
	ts_arrivee AS ts_arrivee_last_flight,
	code_origine AS code_origine_last_flight,
	code_destination AS code_destination_last_flight
FROM(

	SELECT appareils_et_vols.immatriculation, 
		appareils_et_vols.ts_depart, 
		appareils_et_vols.ts_arrivee,
		appareils_et_vols.liaison
	FROM (

		SELECT immatriculation, 
			   MAX(ts_depart) as max_ts_depart
		FROM departs
		LEFT JOIN vols ON departs.num_vol = vols.num_vol
		WHERE ts_arrivee < '2018-10-18 17:35:00'
		GROUP BY immatriculation
	) AS appareils_next_flight
	JOIN (
		SELECT immatriculation, 
			ts_depart,
            ts_arrivee,
			liaison
		FROM departs
		LEFT JOIN vols ON departs.num_vol = vols.num_vol
		) AS appareils_et_vols
			ON appareils_next_flight.immatriculation = appareils_et_vols.immatriculation
			AND appareils_next_flight.max_ts_depart = appareils_et_vols.ts_depart
	) AS full_appareils_et_vols
JOIN liaisons 
	ON full_appareils_et_vols.liaison = liaisons.id_liaison
JOIN (
	SELECT id_aeroports AS id_aeroport_destination, 
		code AS code_destination, 
		nom AS nom_destination 
	FROM airline.aeroports
    ) AS aeroports_destination
 	ON liaisons.aeroport_destination = aeroports_destination.id_aeroport_destination
JOIN (
	SELECT id_aeroports AS id_aeroport_origine, 
		code AS code_origine, 
		nom AS nom_origine FROM airline.aeroports
     ) AS aeroports_origine
 	ON liaisons.aeroport_origine = aeroports_origine.id_aeroport_origine;
    
# -----------------------------

SELECT *
FROM (
	(SELECT immatriculation, type
    FROM(
		SELECT departs.immatriculation,
		   type,
		   ts_depart,
		   ts_arrivee,
		   code_origine,
		   code_destination,
		   ts_depart_next_flight,
		   ts_arrivee_next_flight,
		   code_origine_next_flight,
		   code_destination_next_flight,
		   ts_depart_last_flight,
		   ts_arrivee_last_flight,
		   code_origine_last_flight,
		   code_destination_last_flight
		FROM departs
		LEFT JOIN vols ON departs.num_vol = vols.num_vol
        LEFT JOIN appareils ON departs.immatriculation = appareils.immatriculation
		LEFT JOIN liaisons ON vols.liaison = liaisons.id_liaison
		LEFT JOIN (
			SELECT id_aeroports AS id_aeroport_destination, 
				code AS code_destination, 
				nom AS nom_destination 
			FROM airline.aeroports
			) AS aeroports_destination
			ON liaisons.aeroport_destination = aeroports_destination.id_aeroport_destination
		LEFT JOIN (
			SELECT id_aeroports AS id_aeroport_origine, 
				code AS code_origine, 
				nom AS nom_origine FROM airline.aeroports
			 ) AS aeroports_origine
			ON liaisons.aeroport_origine = aeroports_origine.id_aeroport_origine
		LEFT JOIN appareils_next_flight ON departs.immatriculation = appareils_next_flight.immatriculation
		LEFT JOIN appareils_last_flight ON departs.immatriculation = appareils_last_flight.immatriculation
		WHERE (code_destination_last_flight = 'CDG')
			AND ((code_origine_next_flight = 'HDD'
					AND '2018-10-19 05:15:00' < ts_depart_next_flight)
				OR (code_origine_next_flight != 'HDD'
					AND ADDTIME('2018-10-19 05:15:00', '1 11:40:00') < ts_depart_next_flight)
				OR ts_depart_next_flight IS NULL) 
	) AS appareils_final
	WHERE appareils_final.immatriculation NOT IN (
		SELECT immatriculation
		FROM departs
		LEFT JOIN vols ON departs.num_vol = vols.num_vol
		WHERE (ts_depart < '2018-10-18 17:35:00' AND '2018-10-18 17:35:00' < ts_arrivee)
			OR (ts_depart < '2018-10-19 05:15:00' AND '2018-10-19 05:15:00' < ts_arrivee)
			OR ('2018-10-18 17:35:00' < ts_depart AND ts_arrivee < '2018-10-19 05:15:00')
	))
    UNION
    (SELECT * FROM appareils_no_flight)
    ) AS all_available_appareils;

DROP TEMPORARY TABLE appareils_no_flight;
DROP TEMPORARY TABLE appareils_next_flight;
DROP TEMPORARY TABLE appareils_last_flight;
