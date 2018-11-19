-- MySQL dump 10.13  Distrib 5.7.20, for Linux (x86_64)
--
-- Host: localhost    Database: airline
-- ------------------------------------------------------
-- Server version	5.7.24-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `aeroports`
--

DROP TABLE IF EXISTS `aeroports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `aeroports` (
  `id_aeroports` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(3) DEFAULT NULL,
  `nom` varchar(45) DEFAULT NULL,
  `ville` varchar(45) DEFAULT NULL,
  `pays` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_aeroports`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aeroports`
--

LOCK TABLES `aeroports` WRITE;
/*!40000 ALTER TABLE `aeroports` DISABLE KEYS */;
INSERT INTO `aeroports` VALUES (1,'CDG','Aéroport de Paris-Charles-de-Gaulle','Paris','France'),(16,'YUL','Aéroport international Pierre-Elliott-Trudeau','Canada','Montréal'),(17,'YQB','Aéroport international Jean-Lesage','Canada','Québec'),(18,'MEX','Aéroport international Benito-Juárez','Mexique','Mexico'),(19,'ATL','Aéroport international Hartsfield-Jackson','États-Unis','Atlanta'),(20,'JFK','Aéroport international John-F.-Kennedy','États-Unis','New-York'),(21,'HND','Aéroport international Haneda','Japon','Tokyo'),(22,'PEK','Aéroport international de Pékin-Capitale','Chine','Pékin'),(23,'BER','Aéroport Brandenburg-Willy-Brandt','Allemagne','Berlin'),(24,'BRU','Aéroport de Bruxelles-National','Belgique','Bruxelles'),(25,'MAD','Aéroport Adolfo Suárez Madrid-Barajas','Espagne','Madrid'),(26,'LYS','Aéroport de Lyon-Saint-Exupéry','France','Lyon'),(27,'LHR','Aéroport de Londres-Heathrow','Royaume-Uni','Londres'),(28,'SVO','Aéroport de Moscou-Cheremetievo','Russie','Moscou');
/*!40000 ALTER TABLE `aeroports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appareils`
--

DROP TABLE IF EXISTS `appareils`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `appareils` (
  `num_immatriculation` varchar(45) NOT NULL,
  `type` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`num_immatriculation`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appareils`
--

LOCK TABLES `appareils` WRITE;
/*!40000 ALTER TABLE `appareils` DISABLE KEYS */;
INSERT INTO `appareils` VALUES ('A5ZZ','B772'),('F-GKXO','A320-214'),('F-GSPE','777-228'),('F-GTAH','A321-211'),('F-HEPB','A320-214'),('F-HPJA','A380-861'),('F-HPJB','A380-861'),('N1BC','A333'),('N2YT','B763');
/*!40000 ALTER TABLE `appareils` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `billets`
--

DROP TABLE IF EXISTS `billets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `billets` (
  `num_billet` bigint(16) NOT NULL,
  `prix` decimal(4,0) DEFAULT NULL,
  `ts_emission` datetime DEFAULT NULL,
  `num_depart` varchar(45) DEFAULT NULL,
  `num_passager` int(11) DEFAULT NULL,
  PRIMARY KEY (`num_billet`),
  KEY `num_depart_idx` (`num_depart`),
  KEY `num_client_idx` (`num_passager`),
  CONSTRAINT `num_client` FOREIGN KEY (`num_passager`) REFERENCES `passagers` (`id_passager`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `num_depart` FOREIGN KEY (`num_depart`) REFERENCES `departs` (`num_vol`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billets`
--

LOCK TABLES `billets` WRITE;
/*!40000 ALTER TABLE `billets` DISABLE KEYS */;
INSERT INTO `billets` VALUES (165746583,61,'2018-08-26 08:40:00','AFR7644',1),(1085015469,45,'2018-07-04 11:23:00','AFR7644',2),(1875414696,420,'2018-05-06 15:05:00','AFR348',3),(2489475802,45,'2018-07-07 17:54:00','AFR7644',4),(5302972100,570,'2018-09-06 15:05:00','AFR348',4);
/*!40000 ALTER TABLE `billets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `departs`
--

DROP TABLE IF EXISTS `departs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `departs` (
  `num_vol` varchar(45) DEFAULT NULL,
  `pilote_1` bigint(16) DEFAULT NULL,
  `pilote_2` bigint(16) DEFAULT NULL,
  `equipage_1` bigint(16) DEFAULT NULL,
  `equipage_2` bigint(16) DEFAULT NULL,
  `nbr_places_libres` int(11) DEFAULT NULL,
  `nbr_places_occupees` int(11) DEFAULT NULL,
  `immatriculation_appareil` varchar(45) DEFAULT NULL,
  `id_departs` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id_departs`),
  KEY `pilote_1_idx` (`pilote_1`),
  KEY `pilote_2_idx` (`pilote_2`),
  KEY `equipage_1_idx` (`equipage_1`),
  KEY `equipage_2_idx` (`equipage_2`),
  KEY `immaculation_appareil_idx` (`immatriculation_appareil`),
  KEY `num_vol_idx` (`num_vol`),
  CONSTRAINT `equipage_1` FOREIGN KEY (`equipage_1`) REFERENCES `employes` (`numero_securite_sociale`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `equipage_2` FOREIGN KEY (`equipage_2`) REFERENCES `employes` (`numero_securite_sociale`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `immaculation_appareil` FOREIGN KEY (`immatriculation_appareil`) REFERENCES `appareils` (`num_immatriculation`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `num_vol` FOREIGN KEY (`num_vol`) REFERENCES `vols` (`num_vol`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `pilote_1` FOREIGN KEY (`pilote_1`) REFERENCES `employes` (`numero_securite_sociale`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `pilote_2` FOREIGN KEY (`pilote_2`) REFERENCES `employes` (`numero_securite_sociale`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departs`
--

LOCK TABLES `departs` WRITE;
/*!40000 ALTER TABLE `departs` DISABLE KEYS */;
INSERT INTO `departs` VALUES ('AFR348',191851249560845,163577693139738,174718143121594,292635691720225,23,342,'A5ZZ',1),('AFR7644',275964135451744,182942912944414,293109716948355,282123825733664,6,61,'F-GKXO',2),('DAL405',191851249560845,189145542576748,293109716948355,293109716948355,1,47,'N1BC',3);
/*!40000 ALTER TABLE `departs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employes`
--

DROP TABLE IF EXISTS `employes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `employes` (
  `numero_securite_sociale` bigint(16) NOT NULL,
  `nom` varchar(45) DEFAULT NULL,
  `prenom` varchar(45) DEFAULT NULL,
  `adresse` varchar(45) DEFAULT NULL,
  `ville` varchar(45) DEFAULT NULL,
  `pays` varchar(45) DEFAULT NULL,
  `salaire` decimal(15,0) DEFAULT NULL,
  `type` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`numero_securite_sociale`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employes`
--

LOCK TABLES `employes` WRITE;
/*!40000 ALTER TABLE `employes` DISABLE KEYS */;
INSERT INTO `employes` VALUES (163577693139738,'Quentin','Petit','6 avenue du Bois','Lille','France',4200,'naviguant'),(174718143121594,'David','Bertrand','11 rue du Bout du Chemin','Amiens','France',2900,'naviguant'),(178019734623941,'Grégoire','Pierre','12 rue de Paris','Orléans','France',3000,'au_sol'),(182942912944414,'Aymerick','Jean','23 North Av.','Berlin','Allemagne',5100,'naviguant'),(189145542576748,'Mark','Porter','63-8059 Donec St','New-York','États-Unis',5000,'naviguant'),(191851249560845,'Alexandre','Martin','8 rue Cul de Sac','Rennes','France',6000,'naviguant'),(275964135451744,'Jeanne','Fournier','12 rue Victorien Sardou','Lyon','France',6500,'naviguant'),(282123825733664,'Marie','Dubois','45 cours Lafayette','Lyon','France',2500,'au_sol'),(292108643334472,'Helena','Martinez','4302 Montes, Av.','Madrid','Espagne',3200,'naviguant'),(292635691720225,'Helen','Parker','7895 Sagittis Avenue','Londres','Royaume-Uni',3600,'naviguant'),(293109716948355,'Angele','Perrin','3666 Non, St.','Amsterdam','Pays-Bas',3800,'naviguant');
/*!40000 ALTER TABLE `employes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `liaisons`
--

DROP TABLE IF EXISTS `liaisons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `liaisons` (
  `id_liaison` int(11) NOT NULL AUTO_INCREMENT,
  `aeroport_origine` int(11) DEFAULT NULL,
  `aeroport_destination` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_liaison`),
  KEY `aeroport_origine_idx` (`aeroport_origine`),
  KEY `aeroport_destination_idx` (`aeroport_destination`),
  CONSTRAINT `aeroport_destination` FOREIGN KEY (`aeroport_destination`) REFERENCES `aeroports` (`id_aeroports`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `aeroport_origine` FOREIGN KEY (`aeroport_origine`) REFERENCES `aeroports` (`id_aeroports`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `liaisons`
--

LOCK TABLES `liaisons` WRITE;
/*!40000 ALTER TABLE `liaisons` DISABLE KEYS */;
INSERT INTO `liaisons` VALUES (1,1,20),(2,20,1),(3,1,16),(4,16,1),(5,16,18),(6,18,16),(7,16,20),(8,20,16),(9,26,25),(10,25,26),(11,26,27),(12,27,26),(13,24,1),(14,1,24),(15,23,1),(16,1,23),(17,1,25),(18,25,1);
/*!40000 ALTER TABLE `liaisons` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `naviguants`
--

DROP TABLE IF EXISTS `naviguants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `naviguants` (
  `numero_securite_sociale` bigint(16) NOT NULL,
  `nbr_heures_vol` int(11) DEFAULT NULL,
  `fonction` varchar(45) DEFAULT NULL,
  `num_licence_pilote` bigint(16) DEFAULT NULL,
  PRIMARY KEY (`numero_securite_sociale`),
  CONSTRAINT `num_secu_sociale` FOREIGN KEY (`numero_securite_sociale`) REFERENCES `employes` (`numero_securite_sociale`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `naviguants`
--

LOCK TABLES `naviguants` WRITE;
/*!40000 ALTER TABLE `naviguants` DISABLE KEYS */;
INSERT INTO `naviguants` VALUES (163577693139738,12,'pilote',7045185),(174718143121594,8,'stewart',NULL),(182942912944414,24,'pilote',1128094),(189145542576748,15,'pilote',5884764),(191851249560845,11,'pilote',1316780),(275964135451744,5,'pilote',4926286),(292108643334472,18,'hôtesse',NULL),(292635691720225,7,'hôtesse',NULL),(293109716948355,17,'hôtesse',NULL);
/*!40000 ALTER TABLE `naviguants` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `passagers`
--

DROP TABLE IF EXISTS `passagers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `passagers` (
  `id_passager` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(45) DEFAULT NULL,
  `prenom` varchar(45) DEFAULT NULL,
  `adresse` varchar(45) DEFAULT NULL,
  `ville` varchar(45) DEFAULT NULL,
  `pays` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_passager`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `passagers`
--

LOCK TABLES `passagers` WRITE;
/*!40000 ALTER TABLE `passagers` DISABLE KEYS */;
INSERT INTO `passagers` VALUES (1,'Debouck','Franck','36 avenue Guy de Collongue','Écully','France'),(2,'Raymond','Deubaze','1 allée du Lac','Lyon','France'),(3,'John','Doe','504-4886 Accumsan Ave','New-York','États-Unis'),(4,'Camille','Dupont','14 boulevard Ménilmontant','Paris','France'),(5,'Juan','Rafael','9408 Maecenas Av.','Madrid','Espagne'),(6,'Latifah','Oub','Ap #209-1213 Cursus. Road','Londres','Royaume-Uni');
/*!40000 ALTER TABLE `passagers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vols`
--

DROP TABLE IF EXISTS `vols`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vols` (
  `num_vol` varchar(45) NOT NULL,
  `ts_depart` timestamp NULL DEFAULT NULL,
  `ts_arrivee` timestamp NULL DEFAULT NULL,
  `liaison` int(11) DEFAULT NULL,
  PRIMARY KEY (`num_vol`),
  KEY `liaison_idx` (`liaison`),
  CONSTRAINT `liaison` FOREIGN KEY (`liaison`) REFERENCES `liaisons` (`id_liaison`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vols`
--

LOCK TABLES `vols` WRITE;
/*!40000 ALTER TABLE `vols` DISABLE KEYS */;
INSERT INTO `vols` VALUES ('AFR348','2018-10-18 17:05:00','2018-10-19 00:40:00',1),('AFR7644','2018-10-19 12:15:00','2018-10-19 13:30:00',10),('DAL405','2018-10-18 08:40:00','2018-10-18 13:05:00',18);
/*!40000 ALTER TABLE `vols` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-11-15 18:31:59
