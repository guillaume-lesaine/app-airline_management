SELECT ts_arrivee, 
	   ville_destination, 
       pays_destination 
FROM departs
JOIN vols ON vols.num_vol = departs.num_vol
JOIN airline.liaisons ON vols.liaison = liaisons.id_liaison
JOIN (SELECT id_aeroports AS id_aeroport_destination, 
			 code AS code_destination, 
             nom AS nom_destination, 
             ville AS ville_destination,
             pays AS pays_destination
             FROM airline.aeroports) AS aeroports_destination
 ON liaisons.aeroport_destination = aeroports_destination.id_aeroport_destination
WHERE vols.ts_arrivee = (
	SELECT MAX(ts_arrivee) AS ts_depart_next_flight FROM (
		(SELECT pilote_1 AS naviguant, ts_arrivee
			FROM airline.departs
			JOIN airline.vols ON departs.num_vol = vols.num_vol)
		UNION
		(SELECT pilote_2 AS naviguant, ts_arrivee
			FROM airline.departs
			JOIN airline.vols ON departs.num_vol = vols.num_vol)
		UNION
		(SELECT equipage_1 AS naviguant, ts_arrivee
			FROM airline.departs
			JOIN airline.vols ON departs.num_vol = vols.num_vol)
		UNION
		(SELECT equipage_2 AS naviguant, ts_arrivee
			FROM airline.departs
			JOIN airline.vols ON departs.num_vol = vols.num_vol)
		) AS total_naviguant
	WHERE total_naviguant.naviguant = '191851249560845' AND ts_arrivee < NOW()
	GROUP BY naviguant);