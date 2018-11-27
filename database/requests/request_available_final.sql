# -----------------------------
#VALUES
#TS_DEPART_NV_VOL = '2018-10-18 17:35:00'
#TS_ARRIVEE_NV_VOL = '2018-10-19 05:15:00'
#NB_HEURES_VOL_NV_VOL = INT(TS_ARRIVEE_NV_VOL - TS_DEPART_NV_VOL)
#CODE_ORIGINE_NV_VOL = 'CDG'
#@CODE_DESTINATION_NV_VOL = 'HDD'



CREATE TEMPORARY TABLE naviguants_no_flight
SELECT naviguants.numero_securite_sociale,
	nom,
        prenom,
	fonction,
        nbr_heures_vol
FROM naviguants
JOIN employes ON employes.numero_securite_sociale=naviguants.numero_securite_sociale
NOT IN ( SELECT naviguant FROM (
	(SELECT pilote_1 AS naviguant
			FROM departs
			JOIN vols ON departs.num_vol = vols.num_vol)
		UNION
		(SELECT pilote_2 AS naviguant
			FROM departs
			JOIN vols ON departs.num_vol = vols.num_vol)
		UNION
		(SELECT equipage_1 AS naviguant
			FROM departs
			JOIN vols ON departs.num_vol = vols.num_vol)
		UNION
		(SELECT equipage_2 AS naviguant
			FROM departs
			JOIN vols ON departs.num_vol = vols.num_vol)
	) AS total_naviguants
WHERE pays = (SELECT pays FROM aeroports WHERE aeroports.code = CODE_ORIGINE_NV_VOL));

# -----------------------------

CREATE TEMPORARY TABLE naviguants_next_flight
SELECT naviguant,
	ts_depart AS ts_depart_next_flight,
	ts_arrivee AS ts_arrivee_next_flight,
        code_origine AS code_origine_next_flight,
        code_destination AS code_destination_next_flight
FROM(

	SELECT naviguants_et_vols.naviguant,
		naviguants_et_vols.ts_depart,
		naviguants_et_vols.ts_arrivee,
		naviguants_et_vols.liaison
	FROM (

		SELECT naviguant,
			   MIN(ts_depart) as min_ts_depart
		FROM (
			(SELECT pilote_1 AS naviguant, num_vol
				FROM departs)
			UNION
			(SELECT pilote_2 AS naviguant, num_vol
				FROM departs)
			UNION
			(SELECT equipage_1 AS naviguant, num_vol
				FROM departs)
			UNION
			(SELECT equipage_2 AS naviguant, num_vol
				FROM departs)
			) AS naviguants_vols
		LEFT JOIN vols
			ON naviguants_vols.num_vol = vols.num_vol
		WHERE ts_depart > TS_DEPART_NV_VOL
		GROUP BY naviguant
	) AS naviguants_next_flight
	JOIN (
		SELECT naviguant,
			ts_depart,
            ts_arrivee,
			liaison
		FROM (
			(SELECT pilote_1 AS naviguant, num_vol
				FROM departs)
			UNION
			(SELECT pilote_2 AS naviguant, num_vol
				FROM departs)
			UNION
			(SELECT equipage_1 AS naviguant, num_vol
				FROM departs)
			UNION
			(SELECT equipage_2 AS naviguant, num_vol
				FROM departs)
			) AS naviguants_vols
		LEFT JOIN vols
			ON naviguants_vols.num_vol = vols.num_vol
		) AS naviguants_et_vols
			ON naviguants_next_flight.naviguant = naviguants_et_vols.naviguant
			AND naviguants_next_flight.min_ts_depart = naviguants_et_vols.ts_depart
	) AS full_naviguants_et_vols
JOIN liaisons
	ON full_naviguants_et_vols.liaison = liaisons.id_liaison
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

CREATE TEMPORARY TABLE naviguants_last_flight
SELECT naviguant,
	ts_depart AS ts_depart_last_flight,
	ts_arrivee AS ts_arrivee_last_flight,
        code_origine AS code_origine_last_flight,
        code_destination AS code_destination_last_flight
FROM(

	SELECT naviguants_et_vols.naviguant,
		naviguants_et_vols.ts_depart,
		naviguants_et_vols.ts_arrivee,
		naviguants_et_vols.liaison
	FROM (

		SELECT naviguant,
			   MAX(ts_arrivee) as max_ts_arrivee
		FROM (
			(SELECT pilote_1 AS naviguant, num_vol
				FROM departs)
			UNION
			(SELECT pilote_2 AS naviguant, num_vol
				FROM departs)
			UNION
			(SELECT equipage_1 AS naviguant, num_vol
				FROM departs)
			UNION
			(SELECT equipage_2 AS naviguant, num_vol
				FROM departs)
			) AS naviguants_vols
		LEFT JOIN vols
			ON naviguants_vols.num_vol = vols.num_vol
		WHERE ts_arrivee < TS_DEPART_NV_VOL
		GROUP BY naviguant
	) AS naviguants_next_flight
	JOIN (
		SELECT naviguant,
			ts_depart,
			ts_arrivee,
			liaison
		FROM (
			(SELECT pilote_1 AS naviguant, num_vol
				FROM departs)
			UNION
			(SELECT pilote_2 AS naviguant, num_vol
				FROM departs)
			UNION
			(SELECT equipage_1 AS naviguant, num_vol
				FROM departs)
			UNION
			(SELECT equipage_2 AS naviguant, num_vol
				FROM departs)
			) AS naviguants_vols
		LEFT JOIN vols
			ON naviguants_vols.num_vol = vols.num_vol
		) AS naviguants_et_vols
			ON naviguants_next_flight.naviguant = naviguants_et_vols.naviguant
			AND naviguants_next_flight.max_ts_arrivee = naviguants_et_vols.ts_arrivee
	) AS full_naviguants_et_vols
JOIN liaisons
	ON full_naviguants_et_vols.liaison = liaisons.id_liaison
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
CREATE TEMPORARY TABLE naviguants_in_flight
SELECT naviguant
FROM (
	(SELECT pilote_1 AS naviguant, num_vol
		FROM departs)
	UNION DISTINCT
	(SELECT pilote_2 AS naviguant, num_vol
		FROM departs)
	UNION DISTINCT
    (SELECT equipage_1 AS naviguant, num_vol
		FROM departs)
	UNION DISTINCT
    (SELECT equipage_2 AS naviguant, num_vol
		FROM departs)
) AS naviguants_vols
LEFT JOIN vols ON naviguants_vols.num_vol = vols.num_vol
WHERE (ts_depart < TS_DEPART_NV_VOL AND TS_DEPART_NV_VOL < ts_arrivee)
	OR (ts_depart < TS_ARRIVEE_NV_VOL AND TS_ARRIVEE_NV_VOL < ts_arrivee)
    OR (TS_DEPART_NV_VOL < ts_depart AND ts_arrivee < TS_ARRIVEE_NV_VOL);

# -----------------------------

SELECT nom,
       prenom,
       fonction,
       naviguant,
	   num_vol,
       nbr_heures_vol,
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

FROM (
	SELECT nom,
		prenom,
        fonction,
       naviguants_vols.naviguant,
	   naviguants_vols.num_vol,
       nbr_heures_vol,
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
	FROM (
		(SELECT pilote_1 AS naviguant, num_vol
			FROM departs)
		UNION DISTINCT
		(SELECT pilote_2 AS naviguant, num_vol
			FROM departs)
		UNION DISTINCT
		(SELECT equipage_1 AS naviguant, num_vol
			FROM departs)
		UNION DISTINCT
		(SELECT equipage_2 AS naviguant, num_vol
			FROM departs)
	) AS naviguants_vols
	LEFT JOIN vols ON naviguants_vols.num_vol = vols.num_vol
	LEFT JOIN employes ON naviguants_vols.naviguant = employes.numero_securite_sociale
	LEFT JOIN naviguants ON naviguants_vols.naviguant = naviguants.numero_securite_sociale
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
	LEFT JOIN naviguants_next_flight ON naviguants_vols.naviguant = naviguants_next_flight.naviguant
	LEFT JOIN naviguants_last_flight ON naviguants_vols.naviguant = naviguants_last_flight.naviguant
	WHERE (code_destination_last_flight = CODE_ORIGINE_NV_VOL)
		AND ((code_origine_next_flight = @CODE_DESTINATION_NV_VOL
				AND TS_ARRIVEE_NV_VOL < ts_depart_next_flight
                AND nbr_heures_vol + NB_HEURES_VOL_NV_VOL < 95)
			OR (code_origine_next_flight != @CODE_DESTINATION_NV_VOL
				AND TS_ARRIVEE_NV_VOL + (TS_ARRIVEE_NV_VOL - TS_DEPART_NV_VOL) < ts_depart_next_flight
                AND nbr_heures_vol + 2*NB_HEURES_VOL_NV_VOL < 95))
) AS naviguants_final
WHERE naviguants_final.naviguant NOT IN (
	SELECT naviguant
	FROM (
		(SELECT pilote_1 AS naviguant, num_vol
			FROM departs)
		UNION DISTINCT
		(SELECT pilote_2 AS naviguant, num_vol
			FROM departs)
		UNION DISTINCT
		(SELECT equipage_1 AS naviguant, num_vol
			FROM departs)
		UNION DISTINCT
		(SELECT equipage_2 AS naviguant, num_vol
			FROM departs)
	) AS naviguants_vols
	LEFT JOIN vols ON naviguants_vols.num_vol = vols.num_vol
	WHERE (ts_depart < TS_DEPART_NV_VOL AND TS_DEPART_NV_VOL < ts_arrivee)
		OR (ts_depart < TS_ARRIVEE_NV_VOL AND TS_ARRIVEE_NV_VOL < ts_arrivee)
		OR (TS_DEPART_NV_VOL < ts_depart AND ts_arrivee < TS_ARRIVEE_NV_VOL)
);

DROP TEMPORARY TABLE naviguants_no_flight;
DROP TEMPORARY TABLE naviguants_next_flight;
DROP TEMPORARY TABLE naviguants_last_flight;
DROP TEMPORARY TABLE naviguants_in_flight;
