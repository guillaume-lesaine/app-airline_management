SELECT vols.num_vol, 
	   ts_depart, 
       ts_arrivee, 
       code_origine, 
       code_destination 
FROM departs
JOIN vols ON vols.num_vol = departs.num_vol
JOIN airline.liaisons ON vols.liaison = liaisons.id_liaison
JOIN (
	SELECT id_aeroports AS id_aeroport_destination, 
		   code AS code_destination 
	FROM airline.aeroports
) AS aeroports_destination
ON liaisons.aeroport_destination = aeroports_destination.id_aeroport_destination
JOIN (
	SELECT id_aeroports AS id_aeroport_origine, 
		   code AS code_origine 
	FROM airline.aeroports
) AS aeroports_origine
 ON liaisons.aeroport_origine = aeroports_origine.id_aeroport_origine
 
WHERE vols.ts_depart = (
SELECT MIN(ts_depart) AS ts_depart_next_flight FROM (
	(SELECT pilote_1 AS naviguant, ts_depart
		FROM airline.departs
		JOIN airline.vols ON departs.num_vol = vols.num_vol)
	UNION
	(SELECT pilote_2 AS naviguant, ts_depart
		FROM airline.departs
		JOIN airline.vols ON departs.num_vol = vols.num_vol)
	UNION
    (SELECT equipage_1 AS naviguant, ts_depart
		FROM airline.departs
		JOIN airline.vols ON departs.num_vol = vols.num_vol)
	UNION
    (SELECT equipage_2 AS naviguant, ts_depart
		FROM airline.departs
		JOIN airline.vols ON departs.num_vol = vols.num_vol)
	) AS total_naviguant
	WHERE total_naviguant.naviguant = '191851249560845' AND ts_depart > NOW()
	GROUP BY naviguant);