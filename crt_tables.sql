--
-- This script will create the tables required to persist
-- the Text Categorization data
-- Table designs are based on the Text Categorization
-- Physical Data Model


-- create category table
CREATE TABLE `category` (
  `id` int(11) NOT NULL DEFAULT '0' COMMENT 'Primary key for the category table.',
  `name` varchar(64) DEFAULT NULL COMMENT 'Category name.',
  `normalized_frequency` float DEFAULT NULL COMMENT 'Normalized frequency describing how many documents have been assigned to this category.',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Use to hold the Category instances.';

-- create category_term table
CREATE TABLE `category_term` (
  `id` int(11) NOT NULL DEFAULT '0' COMMENT 'Primary key for the category_term table.',
  `category_id` int(11) DEFAULT NULL COMMENT 'Foreign key for the category table.',
  `term_id` int(11) DEFAULT NULL COMMENT 'Foreign key for the term table.',
  `normalized_frequency` float DEFAULT NULL COMMENT 'The normalized frequency of the term given the category.',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Holds the instances of the Category Term association class.';

-- create category_weight_type table
CREATE TABLE `category_weight_type` (
  `id` int(11) NOT NULL DEFAULT '0' COMMENT 'Primary key for the category_weight_type table.',
  `category_weight_type_name` varchar(128) DEFAULT NULL COMMENT 'he name of the category_weight_type.',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Describes the type of category assignment.';

-- create document
CREATE TABLE `document` (
  `id` int(11) NOT NULL COMMENT 'The primary key for the document table.',
  `name` varchar(255) DEFAULT NULL COMMENT 'Document name, most likely taken from the source document title.',
  `type` varchar(50) DEFAULT NULL COMMENT 'Describes if the document is part of the Training, Test or Run set.',
  `document_category_count` int(11) DEFAULT NULL COMMENT 'How many categories were originally assigned to this document.',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Use to hold the Document instances.';

-- create document_audit table
CREATE TABLE `document_audit` (
  `id` int(11) NOT NULL DEFAULT '0',
  `document_id` int(11) DEFAULT NULL,
  `category_weight_type_id` int(11) DEFAULT NULL,
  `true_positive` int(11) DEFAULT NULL,
  `false_positive` int(11) DEFAULT NULL,
  `document_category_count` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- create document_category table
CREATE TABLE `document_category` (
  `id` int(11) NOT NULL DEFAULT '0' COMMENT 'Primary key of the document_category table.',
  `document_id` int(11) DEFAULT NULL COMMENT 'Foreign key to the document table.',
  `category_id` int(11) DEFAULT NULL COMMENT 'Foreign key to the category table.',
  `category_weight` float DEFAULT NULL COMMENT 'The relative weight given to the category assignment.  Ranges from zero, which represents no belief that the assignment is correct, to 1 which represents a complete belief that the assignment is correct.',
  `category_weight_type_id` int(11) DEFAULT NULL COMMENT 'Foreign key to the category_weight_type table (used to distinguish categories that were previously assigned form those assigned buy the text categorization routine).',
  `positive_assignment` int(11) DEFAULT NULL COMMENT 'Number of positive category assignments.',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Holds the Document Category association class instances.';

-- create document_term table
CREATE TABLE `document_term` (
  `id` int(11) NOT NULL DEFAULT '0' COMMENT 'Primary key of the document_term table.',
  `term_id` int(11) DEFAULT NULL COMMENT 'Foreign key to the term table.',
  `document_id` int(11) DEFAULT NULL COMMENT 'Foreign key to the document table.',
  `normalized_frequency` float DEFAULT NULL COMMENT 'The normalized frequency of occurrence of the term in the given document.',
  `tf_idf` float DEFAULT NULL COMMENT 'The term frequency - inverse document frequency figure.',
  `frequency` int(11) DEFAULT NULL COMMENT 'The un-normalized frequency of the term within the document.',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Holds those instances that represent document term vector.';

-- create stop_char table
CREATE TABLE `stop_char` (
  `id` int(11) NOT NULL DEFAULT '8' COMMENT 'Primary key for the stop_char table.',
  `name` varchar(20) DEFAULT NULL COMMENT 'The stop character.',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Used to hold the list of Stop Characters.';

-- create stop_word table
CREATE TABLE `stop_word` (
  `id` int(11) NOT NULL DEFAULT '0' COMMENT 'The primary key for the stop_word table.',
  `name` varchar(255) DEFAULT NULL COMMENT 'The stop word.',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Used to hold the list of Stop Words.';

-- create term table
CREATE TABLE `term` (
  `id` int(11) NOT NULL DEFAULT '0' COMMENT 'Primary key for the term table.',
  `name` varchar(255) DEFAULT NULL COMMENT 'The term.',
  `normalized_frequency` float DEFAULT NULL COMMENT 'The normalized frequency of how many documents this term can be found in.',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Used to hold the Term instances.';