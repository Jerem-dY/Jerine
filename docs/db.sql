-- phpMyAdmin SQL Dump
-- version 4.6.6deb5ubuntu0.5
-- https://www.phpmyadmin.net/
--
-- Client :  localhost:3306
-- Généré le :  Jeu 23 Mars 2023 à 20:42
-- Version du serveur :  10.1.48-MariaDB-0ubuntu0.18.04.1
-- Version de PHP :  7.2.24-0ubuntu0.18.04.17

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `bourdillat`
--

-- --------------------------------------------------------

--
-- Structure de la table `collection`
--

CREATE TABLE `collection` (
  `collection_id` int(11) NOT NULL,
  `collection_name` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `is_main` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'booléen indiquant s''il s''agit de la collection principale d''un utilisateur'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Contenu de la table `collection`
--

INSERT INTO `collection` (`collection_id`, `collection_name`, `is_main`) VALUES
(1, 'documents', 1);

-- --------------------------------------------------------

--
-- Structure de la table `collection_has_document`
--

CREATE TABLE `collection_has_document` (
  `collection_id` int(11) NOT NULL,
  `document_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `document`
--

CREATE TABLE `document` (
  `document_id` int(11) NOT NULL,
  `document_name` varchar(80) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `form`
--

CREATE TABLE `form` (
  `form_id` int(11) NOT NULL,
  `form_chars` varchar(25) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `form_len` smallint(6) AS (CHAR_LENGTH(form_chars)) VIRTUAL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Contenu de la table `form`
--

INSERT INTO `form` (`form_id`, `form_chars`, `form_len`) VALUES
(-1, NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `lemma`
--

CREATE TABLE `lemma` (
  `lemma_id` int(11) NOT NULL,
  `lemma_form` int(11) NOT NULL,
  `pos` enum('ADJ','ADP','ADV','AUX','CCONJ','DET','INTJ','NOUN','NUM','PART','PRON','PROPN','PUNCT','SCONJ','SYM','VERB','X') COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Contenu de la table `lemma`
--

INSERT INTO `lemma` (`lemma_id`, `lemma_form`, `pos`) VALUES
(-1, -1, 'X');

-- --------------------------------------------------------

--
-- Structure de la table `sentence`
--

CREATE TABLE `sentence` (
  `sentence_id` int(11) NOT NULL,
  `type` enum('DEC','INT','EXC') COLLATE utf8_unicode_ci NOT NULL,
  `text_id` int(11) NOT NULL,
  `sentence_doc_ind` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `token`
--

CREATE TABLE `token` (
  `token_id` int(11) NOT NULL,
  `token_sent_ind` int(11) DEFAULT NULL,
  `token_doc_ind` int(11) NOT NULL,
  `token_form` int(11) NOT NULL,
  `lemma` int(11) DEFAULT NULL,
  `sentence` int(11) NOT NULL,
  `deprel` enum('acl','acl:relcl','advcl','advmod','advmod:emph','advmod:lmod','amod','appos','aux','aux:pass','case','cc','cc:preconj','ccomp','clf','compound','compound:lvc','compound:prt','compound:redup','compound:svc','conj','cop','csubj','csubj:outer','csubj:pass','dep','det','det:numgov','det:nummod','det:poss','discourse','dislocated','expl','expl:impers','expl:pass','expl:pv','fixed','flat','flat:foreign','flat:name','goeswith','iobj','list','mark','nmod','nmod:poss','nmod:tmod','nsubj','nsubj:outer','nsubj:pass','nummod','nummod:gov','obj','obl','obl:agent','obl:arg','obl:lmod','obl:tmod','orphan','parataxis','punct','reparandum','root','vocative','xcomp') COLLATE utf8_unicode_ci DEFAULT NULL,
  `head` int(11) DEFAULT NULL,
  `offset` int(11) NOT NULL,
  `spaceafter` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `user`
--

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL,
  `login` varchar(8) COLLATE utf8_unicode_ci NOT NULL,
  `password` char(60) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `fname` varchar(12) COLLATE utf8_unicode_ci NOT NULL,
  `surname` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `documents` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Contenu de la table `user`
--

INSERT INTO `user` (`user_id`, `login`, `password`, `fname`, `surname`, `documents`) VALUES
(1, 'bourdije', '$2y$10$Oi9CULEflMTw4HbX1/yY6umwdQMKWn6ZzMETNrsZKqdAYJCU5Wpi6', 'Jérémy', 'Bourdillat', 1);

-- --------------------------------------------------------

--
-- Structure de la table `user_has_collection`
--

CREATE TABLE `user_has_collection` (
  `user_id` int(11) NOT NULL,
  `collection_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Index pour les tables exportées
--

--
-- Index pour la table `collection`
--
ALTER TABLE `collection`
  ADD PRIMARY KEY (`collection_id`);

--
-- Index pour la table `collection_has_document`
--
ALTER TABLE `collection_has_document`
  ADD PRIMARY KEY (`collection_id`,`document_id`),
  ADD KEY `fk_collection_has_document_document1_idx` (`document_id`),
  ADD KEY `fk_collection_has_document_collection1_idx` (`collection_id`);

--
-- Index pour la table `document`
--
ALTER TABLE `document`
  ADD PRIMARY KEY (`document_id`);

--
-- Index pour la table `form`
--
ALTER TABLE `form`
  ADD PRIMARY KEY (`form_id`),
  ADD UNIQUE KEY `form_chars` (`form_chars`);

--
-- Index pour la table `lemma`
--
ALTER TABLE `lemma`
  ADD PRIMARY KEY (`lemma_id`),
  ADD UNIQUE KEY `lemma_signature` (`lemma_form`,`pos`),
  ADD KEY `lemma_form` (`lemma_form`);

--
-- Index pour la table `sentence`
--
ALTER TABLE `sentence`
  ADD PRIMARY KEY (`sentence_id`,`text_id`),
  ADD UNIQUE KEY `sentence_signature` (`type`,`text_id`,`sentence_doc_ind`),
  ADD KEY `fk_sentence_document1_idx` (`text_id`);

--
-- Index pour la table `token`
--
ALTER TABLE `token`
  ADD PRIMARY KEY (`token_id`,`sentence`),
  ADD KEY `fk_token_sentence1_idx` (`sentence`),
  ADD KEY `fk_token_token1_idx` (`head`),
  ADD KEY `token_form` (`token_form`),
  ADD KEY `token_lemma_fk` (`lemma`);

--
-- Index pour la table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`,`documents`),
  ADD KEY `fk_user_collection1_idx` (`documents`);

--
-- Index pour la table `user_has_collection`
--
ALTER TABLE `user_has_collection`
  ADD PRIMARY KEY (`user_id`,`collection_id`),
  ADD KEY `fk_user_has_collection_collection1_idx` (`collection_id`),
  ADD KEY `fk_user_has_collection_user_idx` (`user_id`);

--
-- AUTO_INCREMENT pour les tables exportées
--

--
-- AUTO_INCREMENT pour la table `collection`
--
ALTER TABLE `collection`
  MODIFY `collection_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT pour la table `form`
--
ALTER TABLE `form`
  MODIFY `form_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `lemma`
--
ALTER TABLE `lemma`
  MODIFY `lemma_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `sentence`
--
ALTER TABLE `sentence`
  MODIFY `sentence_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `token`
--
ALTER TABLE `token`
  MODIFY `token_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `user`
--
ALTER TABLE `user`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- Contraintes pour les tables exportées
--

--
-- Contraintes pour la table `collection_has_document`
--
ALTER TABLE `collection_has_document`
  ADD CONSTRAINT `fk_collection_has_document_collection1` FOREIGN KEY (`collection_id`) REFERENCES `collection` (`collection_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_collection_has_document_document1` FOREIGN KEY (`document_id`) REFERENCES `document` (`document_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `lemma`
--
ALTER TABLE `lemma`
  ADD CONSTRAINT `lemma_ibfk_1` FOREIGN KEY (`lemma_form`) REFERENCES `form` (`form_id`);

--
-- Contraintes pour la table `sentence`
--
ALTER TABLE `sentence`
  ADD CONSTRAINT `fk_sentence_document1` FOREIGN KEY (`text_id`) REFERENCES `document` (`document_id`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Contraintes pour la table `token`
--
ALTER TABLE `token`
  ADD CONSTRAINT `token_ibfk_1` FOREIGN KEY (`sentence`) REFERENCES `sentence` (`sentence_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `token_ibfk_2` FOREIGN KEY (`token_form`) REFERENCES `form` (`form_id`),
  ADD CONSTRAINT `token_lemma_fk` FOREIGN KEY (`lemma`) REFERENCES `lemma` (`lemma_id`);

--
-- Contraintes pour la table `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `fk_user_collection1` FOREIGN KEY (`documents`) REFERENCES `collection` (`collection_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `user_has_collection`
--
ALTER TABLE `user_has_collection`
  ADD CONSTRAINT `fk_user_has_collection_collection1` FOREIGN KEY (`collection_id`) REFERENCES `collection` (`collection_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_user_has_collection_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
